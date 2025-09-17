import requests

def get_lat_lon_from_zip(zipcode):
    # Use the public API to convert ZIP code to lat/lon
    url = f"https://nominatim.openstreetmap.org/search?postalcode={zipcode}&country=us&format=json"
    resp = requests.get(url, headers={"User-Agent": "weathertest"})
    data = resp.json()
    if data:
        return data[0]["lat"], data[0]["lon"]
    return None, None

def get_weather_by_zip(zipcode):
    lat, lon = get_lat_lon_from_zip(zipcode)
    if not lat or not lon:
        return None

    # Get NWS gridpoint info
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    points_resp = requests.get(points_url)
    if points_resp.status_code != 200:
        return None
    forecast_url = points_resp.json().get("properties", {}).get("forecast")
    if not forecast_url:
        return None

    forecast_resp = requests.get(forecast_url)
    if forecast_resp.status_code != 200:
        return None

    periods = forecast_resp.json().get("properties", {}).get("periods", [])
    if periods:
        today = periods[0]
        return f"{today['name']}: {today['detailedForecast']}"
    return None