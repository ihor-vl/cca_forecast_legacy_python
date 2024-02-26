from datetime import datetime
from collections import defaultdict
import requests


def main():
    url = "https://e75urw7oieiszbzws4gevjwvze0baaet.lambda-url.eu-west-2.on.aws/"

    response = requests.get(url)
    response.raise_for_status()

    weather_data = response.json()

    grouped_by_day = defaultdict(list)
    summaries = {}
    # Group entries by day
    for entry in weather_data:
        entry_time = datetime.fromisoformat(entry["date_time"].replace('Z', '+00:00'))
        day_key = entry_time.date()
        grouped_by_day[day_key].append(entry)
    # Process each day
    for day, entries in grouped_by_day.items():
        morning_temps, morning_rains, afternoon_temps, afternoon_rains = [], [], [], []
        all_temps = [entry["average_temperature"] for entry in entries]

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

        summary = ["Day: " + day.strftime("%A %B %d").replace(" 0", " ") + "\n\n",
                   "Morning Average Temperature: ", "Insufficient forecast data" if not morning_temps else str(round(
                       sum(morning_temps) / len(morning_temps))) + "\n",
                   "Morning Chance Of Rain: ", "Insufficient forecast data" if not morning_rains else str(round(
                       sum(morning_rains) / len(morning_rains), 2)) + "\n",
                   "Afternoon Average Temperature: ", "Insufficient forecast data" if not afternoon_temps else str(round(
                       sum(afternoon_temps) / len(afternoon_temps))) + "\n",
                   "Afternoon Chance Of Rain: ", "Insufficient forecast data" if not afternoon_rains else str(round(
                       sum(afternoon_rains) / len(afternoon_rains), 2)) + "\n",
                   "High Temperature: " + str(max(all_temps)) + "\n",
                   "Low Temperature: " + str(min(all_temps)) + "\n"]

        print("".join(summary))
        return "".join(summary)


if __name__ == "__main__":
    main()