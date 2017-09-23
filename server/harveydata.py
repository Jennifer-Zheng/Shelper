import requests

response = requests.get("https://api.harveyneeds.org/api-docs/swagger-v1.json")
print(response.status_code)
