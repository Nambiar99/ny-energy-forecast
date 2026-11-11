import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

MODEL_DIR = PROJECT_ROOT / "models"

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta, timezone
import pandas as pd
import requests
import numpy as np
os.environ["KERAS_BACKEND"] = "torch"
import keras
from pathlib import Path
import joblib
import openmeteo_requests
import requests_cache
from retry_requests import retry

lag, horizon, batch = 24, 24, 128
features =  ['Demand', 'temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 'precipitation', 'wind_speed_10m', 'surface_pressure', 'hour_sin', 'hour_cos', 'day_sin', 'day_cos', 'month_sin', 'month_cos', 'is_weekend']
features_to_scale = ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 'precipitation', 'wind_speed_10m', 'surface_pressure']
targets = ['Demand']


def fetch_EIA_data(hours):
	API_KEY = os.getenv("EIA_API_KEY")
	url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
	now = datetime.now(timezone.utc)
	end_date = now.strftime("%Y-%m-%dT%H")
	start_date = (now - timedelta(hours=hours)).strftime("%Y-%m-%dT%H")
	base_params = [
	("api_key", API_KEY),
	("frequency", "hourly"),
	("data[0]", "value"),
	("facets[respondent][]", "NY"),
	("start", start_date),
	("end", end_date),
	("sort[0][column]", "period"),
	("sort[0][direction]", "asc")
		]

	all_rows = []
	offset = 0
	page_size = 5000
	total = None
	
	while total is None or offset < total:
		params = base_params + [
			("offset", offset),
			("length", page_size)
		]
		response = requests.get(url, params=params)
		response.raise_for_status()
		result = response.json()["response"]
		rows = result["data"]

		if total is None:
			total = int(result["total"])
			print(f"Total rows available: {total}")

		if not rows:
			break

		all_rows.extend(rows)
		offset += len(rows)

	df = pd.DataFrame(all_rows)
	df["value"] = pd.to_numeric(df["value"])
	df = df.pivot(index=["period", "respondent", "respondent-name"], columns="type-name", values="value").reset_index()
	df.columns.name = None
	df = df.drop(columns=["respondent-name"])
	df = df.rename(columns={"period": "Time"})
	df["Time"] = pd.to_datetime(df["Time"], format="%Y-%m-%dT%H")
	return df


def fetch_weather_data(hours):
	now = datetime.now(timezone.utc)
	end_date = now.strftime("%Y-%m-%dT%H:00")
	start_date = (now - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:00")
	params = {
		"latitude": 40.7128,
		"longitude": -74.0060,
		"start_hour": start_date,
		"end_hour": end_date,
		"hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "wind_speed_10m", "surface_pressure"],
	}
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

	responses = openmeteo.weather_api(url, params = params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation: {response.Elevation()} m asl")
	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
	hourly_surface_pressure = hourly.Variables(5).ValuesAsNumpy()

	hourly_data = {
		"date": pd.date_range(
			start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
			end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = hourly.Interval()),
			inclusive = "left"
		)
	}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["apparent_temperature"] = hourly_apparent_temperature
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["surface_pressure"] = hourly_surface_pressure

	df = pd.DataFrame(data = hourly_data)
	df = df.rename(columns={"date": "Time"})
	df["Time"] = pd.to_datetime(df["Time"])
	df["Time"] = df["Time"].dt.tz_localize(None)
	return df

def make_features(df):
	df["hour_sin"] = np.sin(2 * np.pi * df["Time"].dt.hour / 24)
	df["hour_cos"] = np.cos(2 * np.pi * df["Time"].dt.hour / 24)
	df["day_sin"] = np.sin(2 * np.pi * df["Time"].dt.dayofweek / 7)
	df["day_cos"] = np.cos(2 * np.pi * df["Time"].dt.dayofweek / 7)
	df["month_sin"] = np.sin(2 * np.pi * df["Time"].dt.month / 12)
	df["month_cos"] = np.cos(2 * np.pi * df["Time"].dt.month / 12)
	df["is_weekend"] = (df["Time"].dt.dayofweek > 4).astype(int)
	df["lag1"] = df["Demand"].shift(1)
	df["lag24"] = df["Demand"].shift(24)
	df["lag48"] = df["Demand"].shift(48)
	df["lag168"] = df["Demand"].shift(168)
	df["rolling_mean24"] = df["Demand"].rolling(window=24).mean()
	df["rolling_std24"] = df["Demand"].rolling(window=24).std()
	return df

def forecast():
	energy = fetch_EIA_data(2*lag)
	weather = fetch_weather_data(2*lag)
	merged_df = pd.merge(energy, weather, on="Time", how="inner")
	merged_df = merged_df.iloc[:-1]
	merged_w_feats = make_features(merged_df)
	to_model = merged_w_feats.tail(lag).copy()

	start_time = to_model["Time"].max()
	new_time = pd.date_range(start=start_time + pd.Timedelta(hours=1), periods=24, freq="1h")
	next_24h = pd.DataFrame({"Time": new_time})

	trial_data = to_model.copy()
	plot_data = trial_data.copy()

	target_scaler = joblib.load(MODEL_DIR / f'target_scaler_lag_{lag}_h_{horizon}_b_{batch}.pkl')
	feats_scaler = joblib.load(MODEL_DIR / f'feats_scaler_lag_{lag}_h_{horizon}_b_{batch}.pkl')
	model = keras.models.load_model(MODEL_DIR / f'model_lag_{lag}_h_{horizon}_b_{batch}.keras')

	trial_data[features_to_scale] = feats_scaler.transform(trial_data[features_to_scale])
	trial_data["Demand"] = target_scaler.transform(trial_data[["Demand"]])
	x = trial_data[features].values[None, :, :]
	pred_scaled = model.predict(x)
	pred = target_scaler.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()
	next_24h["Demand"] = pred
	return plot_data, next_24h, lag, horizon
