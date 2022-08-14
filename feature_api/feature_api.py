from datetime import datetime, date, timedelta
import requests

FEATURES_API_URL = "https://api.predicthq.com/v1/features"
ACCESS_TOKEN = ''

class FeatureAPI:

    def __init__(self, lat, lon, start, end, rank_threshold=30, DATE_FORMAT="%Y-%m-%d"):
        self.__lat = lat
        self.__lon = lon
        self.__start = start
        self.__end = end
        self.__rank_threshold = rank_threshold
        self.__DATE_FORMAT = DATE_FORMAT

    def get_date_groups(self):
        def _split_dates(s, e):
            capacity = timedelta(days=90)
            interval = 1 + int((e - s) / capacity)
            for i in range(interval):
                yield s + capacity * i
            yield e

        dates = list(_split_dates(self.start, self.end))
        for i, (d1, d2) in enumerate(zip(dates, dates[1:])):
            if d2 != dates[-1]:
                d2 -= timedelta(days=1)
            yield d1.strftime(self.DATE_FORMAT), d2.strftime(self.DATE_FORMAT)

    def get_features_api_severe_weather_events(self, SEVERE_WEATHER_FEATURES):
        start = datetime.strptime(self.start, self.DATE_FORMAT).date()
        end = datetime.strptime(self.end, self.DATE_FORMAT).date()

        print("Querying Features API...")
        result = []
        for gte, lte in self.get_date_groups(self.start, self.end):
            print(f"{gte} -> {lte}")
            request_data = {
                "location": {"geo": {"lat": self.lat, "lon": self.lon, "radius": "1m"}},
                "active": {"gte": gte, "lte": lte},
            }
            for feature in SEVERE_WEATHER_FEATURES:
                request_data[feature] = {
                                        'stats': ['max'],
                                        'phq_rank': { 
                                            'gte': self.rank_threshold
                                        }
                                    }

            try:
                response = requests.post(
                    f"{FEATURES_API_URL}",
                    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
                    json=request_data,
                ).json()
            except Exception as e:
                print(e)
                return {}, f"{e}"

            for day in response["results"]:
                features = {'date': day["date"]}
                features.update({f: day[f]["stats"]["max"] for f in SEVERE_WEATHER_FEATURES})
                result.append(features)
        return result, None


    def get_features_api_data(self, radius, ATTENDED_FEATURES, HOLIDAY_FEATURES):
        start = datetime.strptime(self.start, self.DATE_FORMAT).date()
        end = datetime.strptime(self.end, self.DATE_FORMAT).date()

        print("Querying Features API...")
        result = []
        for gte, lte in self.get_date_groups(start, end):
            print(f"{gte} -> {lte}")
            request_data = {
                "location": {"geo": {"lat": self.lat, "lon": self.lon, "radius": f"{radius}m"}},
                "active": {"gte": gte, "lte": lte},
            }
            for feature in ATTENDED_FEATURES:
                request_data[feature] = {
                                        'stats': ['sum'], 
                                        'phq_rank': { 
                                            'gte': self.rank_threshold
                                        }
                                    }
                
            for feature in HOLIDAY_FEATURES:
                request_data[feature] = True

            try:
                response = requests.post(
                    f"{FEATURES_API_URL}",
                    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
                    json=request_data,
                ).json()
            except Exception as e:
                return {}, f"{e}"
            
            for day in response["results"]:
                features = {'date': day["date"]}
                features.update({f: day[f]["stats"]["sum"] for f in ATTENDED_FEATURES})
                features.update({f: sum(day[f]["rank_levels"].values()) for f in HOLIDAY_FEATURES})
                result.append(features)
        return result, None