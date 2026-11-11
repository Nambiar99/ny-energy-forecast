import json
import requests
import pandas as pd
import os

API_KEY = "2INKygIhcpBYvgctY2q8KLlIOGthBWTykYIKnYF4"

url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"



base_params = [
	("api_key", API_KEY),
	("frequency", "hourly"),
	("data[0]", "value"),
	("facets[respondent][]", "NY"),
	("start", "2022-01-01T00"),
	("end", "2025-12-31T23"),
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
	print(f"Downloaded {len(all_rows)} / {total}")

df = pd.DataFrame(all_rows)
df["value"] = pd.to_numeric(df["value"])
df.to_csv("test_NY_3_years.csv", index=False)

