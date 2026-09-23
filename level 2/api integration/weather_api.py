'''
 from http.client import responses


Description: Write a Python script that interacts with
an external API to fetch and display data (e.g.,
weather, cryptocurrency prices).

This  API Integration
Uses the requests library to make GET requests to an API.
Parse and display the fetched data in a user-friendly
format.

 Errors such as failed requests or invalid
responses are handled 

'''


import requests

# Open-Meteo API - no API key required
url = "https://api.open-meteo.com/v1/forecast"

# Location: Accra, Ghana
params = {
    "latitude": 5.6037,
    "longitude": -0.1870,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
}

try:
    # Send GET request to the API
    response = requests.get(url, params=params, timeout=10)

    # Check if the request was successful
    response.raise_for_status()

    # Convert the response into JSON
    data = response.json()

    # Check that the expected data exists
    if "current" not in data:
        print("Error: The API returned an unexpected response.")
    else:
        weather = data["current"]

        print("\n===== ACCRA WEATHER =====")
        print(f"Temperature: {weather['temperature_2m']}°C")
        print(f"Humidity: {weather['relative_humidity_2m']}%")
        print(f"Wind Speed: {weather['wind_speed_10m']} km/h")
        print("==========================")

except requests.exceptions.Timeout:
    print("Error: The request timed out. Please try again.")

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the API. Check your internet connection.")

except requests.exceptions.HTTPError as error:
    print(f"Error: API request failed: {error}")

except ValueError:
    print("Error: The API returned invalid JSON data.")

except requests.exceptions.RequestException as error:
    print(f"An unexpected request error occurred: {error}")

except KeyError:
    print("Error: Some expected weather data was missing.")