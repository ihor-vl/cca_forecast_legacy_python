from datetime import datetime
from collections import defaultdict
from typing import NamedTuple, Optional

import requests

URL = "https://e75urw7oieiszbzws4gevjwvze0baaet.lambda-url.eu-west-2.on.aws/"


def get_weather_data(url):

    response = requests.get(url)
    response.raise_for_status()

    weather_data = response.json()

    return weather_data


class ForecastValues(NamedTuple):
    morning_average_temperature: Optional[float]
    morning_chance_of_rain: Optional[float]
    afternoon_average_temperature: Optional[float]
    afternoon_chance_of_rain: Optional[float]
    night_average_temperature: Optional[float]
    night_chance_of_rain: Optional[float]
    high_temperature: float
    low_temperature: float


def get_average_values(entries) -> ForecastValues:
    all_temps = [entry["average_temperature"] for entry in entries]

    (morning_temps, morning_rains, afternoon_temps,
     afternoon_rains, evening_temps, evening_rains) = [], [], [], [], [], []

    for entry in entries:
        entry_time = datetime.fromisoformat(entry["date_time"].replace('Z', '+00:00'))
        # collect morning period entries
        if 6 <= entry_time.hour < 12:
            morning_temps.append(entry["average_temperature"])
            morning_rains.append(entry["probability_of_rain"])
        # collection afternoon period entries
        elif 12 <= entry_time.hour < 18:
            afternoon_temps.append(entry["average_temperature"])
            afternoon_rains.append(entry["probability_of_rain"])
        elif 18 <= entry_time.hour < 22:
            evening_temps.append(entry["average_temperature"])
            evening_rains.append(entry["probability_of_rain"])

    return ForecastValues(
        morning_average_temperature=sum(morning_temps) / len(morning_temps) if morning_temps else None,
        morning_chance_of_rain=sum(morning_rains) / len(morning_rains) if morning_rains else None,
        afternoon_average_temperature=sum(afternoon_temps) / len(afternoon_temps) if afternoon_temps else None,
        afternoon_chance_of_rain=sum(afternoon_rains) / len(afternoon_rains) if afternoon_rains else None,
        night_average_temperature=sum(evening_temps) / len(evening_temps) if evening_temps else None,
        night_chance_of_rain=sum(evening_rains) / len(evening_rains) if evening_rains else None,
        high_temperature=max(all_temps),
        low_temperature=min(all_temps)
    )


def main():
    weather_data = get_weather_data(URL)

    grouped_by_day = defaultdict(list)
    summaries = {}
    # Group entries by day
    for entry in weather_data:
        entry_time = datetime.fromisoformat(entry["date_time"].replace('Z', '+00:00'))
        day_key = entry_time.date()
        grouped_by_day[day_key].append(entry)
    # Process each day
    for day, entries in grouped_by_day.items():
        forecast_values = get_average_values(entries)
        summaries[day] = forecast_values

        summary = ["Day: " + day.strftime("%A %B %d").replace(" 0", " ") + "\n\n",
                   "Morning Average Temperature: ", "Insufficient forecast data" if not forecast_values.morning_average_temperature else str(round(
                       forecast_values.morning_average_temperature)) + "\n",
                   "Morning Chance Of Rain: ", "Insufficient forecast data" if not forecast_values.morning_chance_of_rain else str(round(
                       forecast_values.morning_chance_of_rain, 2)) + "\n",
                   "Afternoon Average Temperature: ", "Insufficient forecast data" if not forecast_values.afternoon_average_temperature else str(round(
                       forecast_values.afternoon_average_temperature)) + "\n",
                   "Afternoon Chance Of Rain: ", "Insufficient forecast data" if not forecast_values.afternoon_chance_of_rain else str(round(
                       forecast_values.afternoon_chance_of_rain, 2)) + "\n",
                   "High Temperature: " + str(forecast_values.high_temperature) + "\n",
                   "Low Temperature: " + str(forecast_values.low_temperature) + "\n"]

        print("".join(summary))
        return "".join(summary)


if __name__ == "__main__":
    main()
