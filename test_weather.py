
import unittest
from unittest.mock import patch, Mock

import weather


class TestWeather(unittest.TestCase):

    # TEST 1: Coordinates
    @patch("weather.requests.get")
    def test_get_coordinates(self, mock_get):

        mock_response = Mock()

        mock_response.json.return_value = [
            {
                "lat": "42.5751",
                "lon": "-71.9981"
            }
        ]

        mock_get.return_value = mock_response

        lat, lon = weather.get_coordinates("Gardner, MA")

        self.assertEqual(lat, 42.5751)
        self.assertEqual(lon, -71.9981)

    # TEST 2: NOAA endpoint
    @patch("weather.requests.get")
    def test_get_noaa_endpoint(self, mock_get):

        mock_response = Mock()

        mock_response.json.return_value = {
            "properties": {
                "forecast": "https://api.weather.gov/test"
            }
        }

        mock_get.return_value = mock_response

        result = weather.get_noaa_endpoint(
            42.5751,
            -71.9981
        )

        self.assertEqual(
            result,
            "https://api.weather.gov/test"
        )

    # TEST 3: NOAA forecast
    @patch("weather.requests.get")
    def test_get_noaa_forecast(self, mock_get):

        mock_response = Mock()

        mock_response.json.return_value = {
            "properties": {
                "periods": [
                    {
                        "name": "Tonight",
                        "temperature": 48,
                        "temperatureUnit": "F",
                        "shortForecast": "Partly Cloudy"
                    }
                ]
            }
        }

        mock_get.return_value = mock_response

        result = weather.get_noaa_forecast(
            "https://api.weather.gov/test"
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["temperature"], 48)


if __name__ == "__main__":
    unittest.main()
