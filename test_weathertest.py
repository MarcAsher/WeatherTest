import unittest
from unittest.mock import patch
import nws_client

class TestWeatherTest(unittest.TestCase):
    @patch('nws_client.requests.get')
    def test_get_lat_lon_from_zip_success(self, mock_get):
        mock_get.return_value.json.return_value = [{
            "lat": "34.0901",
            "lon": "-118.4065"
        }]
        lat, lon = nws_client.get_lat_lon_from_zip("90210")
        self.assertEqual(lat, "34.0901")
        self.assertEqual(lon, "-118.4065")

    @patch('nws_client.requests.get')
    def test_get_lat_lon_from_zip_not_found(self, mock_get):
        mock_get.return_value.json.return_value = []
        lat, lon = nws_client.get_lat_lon_from_zip("00000")
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    @patch('nws_client.requests.get')
    def test_get_weather_by_zip_success(self, mock_get):
        # Mock sequence: ZIP→latlon, points→forecast url, forecast→periods
        def side_effect(url, *args, **kwargs):
            if "nominatim" in url:
                class Resp: 
                    def json(self): return [{"lat": "34.0901", "lon": "-118.4065"}]
                return Resp()
            elif "api.weather.gov/points" in url:
                class Resp: 
                    def json(self): return {"properties": {"forecast": "http://fake/forecast"}}
                    status_code = 200
                return Resp()
            elif "fake/forecast" in url:
                class Resp:
                    def json(self): return {"properties": {"periods": [
                        {"name": "Tonight", "detailedForecast": "Clear and cool."}
                    ]}}
                    status_code = 200
                return Resp()
            else:
                raise ValueError("Unexpected URL: " + url)
        mock_get.side_effect = side_effect
        result = nws_client.get_weather_by_zip("90210")
        self.assertIn("Tonight: Clear and cool.", result)

    @patch('nws_client.requests.get')
    def test_get_weather_by_zip_zip_not_found(self, mock_get):
        mock_get.return_value.json.return_value = []
        result = nws_client.get_weather_by_zip("00000")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()