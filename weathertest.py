import sys
from nws_client import get_weather_by_zip

def main():
    if len(sys.argv) != 2:
        print("Usage: python weathertest.py <ZIPCODE>")
        sys.exit(1)

    zipcode = sys.argv[1]
    weather = get_weather_by_zip(zipcode)

    if weather:
        print(f"Weather for ZIP code {zipcode}:")
        print(weather)
    else:
        print("Could not retrieve weather information.")

if __name__ == "__main__":
    main()