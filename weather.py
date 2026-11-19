
import argparse
import requests


# API headers
HEADERS = {
    "User-Agent": "MWCC"
}


# FUNCTION 1: Get city coordinates
def get_coordinates(city):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError("Location not found.")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    return lat, lon


# FUNCTION 2: Get NOAA forecast endpoint
def get_noaa_endpoint(lat, lon):

    url = f"https://api.weather.gov/points/{lat},{lon}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    forecast_url = data["properties"]["forecast"]

    return forecast_url


# FUNCTION 3: Get NOAA weather forecast
def get_noaa_forecast(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    periods = data["properties"]["periods"]

    return periods


# FUNCTION 4: Main application
def main():

    parser = argparse.ArgumentParser(
        description="NOAA Weather Forecast Application"
    )

    parser.add_argument(
        "-l",
        "--location",
        required=True,
        help="City and State (example: Gardner, MA)"
    )

    options = parser.add_mutually_exclusive_group()

    options.add_argument(
        "-d",
        "--detailed",
        action="store_true",
        help="Display detailed weather forecast"
    )

    options.add_argument(
        "-w",
        "--week",
        action="store_true",
        help="Display weekly weather forecast"
    )

    options.add_argument(
        "-a",
        "--average",
        action="store_true",
        help="Calculate average temperature"
    )

    args = parser.parse_args()

    try:

        # STEP 1: Get coordinates
        lat, lon = get_coordinates(args.location)

        # STEP 2: Get NOAA endpoint
        forecast_url = get_noaa_endpoint(lat, lon)

        # STEP 3: Get weather forecast
        periods = get_noaa_forecast(forecast_url)

        if not periods:
            raise ValueError("No forecast information available.")

        print("\n" + "=" * 50)
        print("             NOAA WEATHER REPORT")
        print("=" * 50)

        print(f"Location: {args.location}")

        # OPTION A: Average temperature
        if args.average:

            temperatures = [
                period["temperature"]
                for period in periods
                if period.get("temperature") is not None
            ]

            if not temperatures:
                raise ValueError("No temperature data available.")

            average = sum(temperatures) / len(temperatures)

            unit = next(
                period["temperatureUnit"]
                for period in periods
                if period.get("temperature") is not None
            )

            print("\nAVERAGE TEMPERATURE")
            print("-" * 50)
            print(f"Temperatures: {temperatures}")
            print(f"Average: {average:.1f}°{unit}")

        # OPTION B: Weekly forecast
        elif args.week:

            print("\nSEVEN-DAY FORECAST")
            print("-" * 50)

            for period in periods[:14]:

                print(f"\n{period['name']}")
                print(
                    f"Temperature: {period['temperature']}°"
                    f"{period['temperatureUnit']}"
                )
                print(f"Forecast: {period['shortForecast']}")

        # OPTION C: Detailed forecast
        elif args.detailed:

            current = periods[0]

            print("\nCURRENT DETAILED FORECAST")
            print("-" * 50)

            print(f"Period: {current['name']}")
            print(
                f"Temperature: {current['temperature']}°"
                f"{current['temperatureUnit']}"
            )
            print(f"Short Forecast: {current['shortForecast']}")
            print(f"Detailed Forecast: {current['detailedForecast']}")

        # DEFAULT: Short forecast
        else:

            current = periods[0]

            print("\nCURRENT WEATHER")
            print("-" * 50)

            print(f"Period: {current['name']}")
            print(
                f"Temperature: {current['temperature']}°"
                f"{current['temperatureUnit']}"
            )
            print(f"Forecast: {current['shortForecast']}")

        print("\n" + "=" * 50)

    except requests.exceptions.RequestException as error:

        print(f"\nAPI Error: {error}")

    except (KeyError, IndexError, ValueError, TypeError) as error:

        print(f"\nApplication Error: {error}")


if __name__ == "__main__":
    main()
