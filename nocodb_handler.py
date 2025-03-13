import http.client
import json
import pandas as pd

conn = http.client.HTTPSConnection("app.nocodb.com")

api_key = 'uBkdyj-aTVaqzWzh9ha093CNF6l12OydGKxm-E8E'

headers = { 'xc-token': api_key }

conn.request("GET", "/api/v2/tables/m0eezxhvn1pgb4r/records?offset=0&limit=25&where=&viewId=vwvabzwoemhigxbg", headers=headers)

res = conn.getresponse()
data = res.read()


# Decode and parse the JSON response
json_data = json.loads(data.decode("utf-8"))

# Extract records from the JSON response
records = json_data.get("list", [])

# Convert records to a pandas DataFrame
df = pd.DataFrame(records)

# Display the DataFrame
print(df)