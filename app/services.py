import csv
import json
import logging
import tornado.httpclient
import tornado
from tornado import gen


class CityDataService(object):
    """
    Service to deal with the european_cities.csv.
    """
    def __init__(self, source=lambda: open('data/european_cities.csv')):
        self._source = source
        self._cities = []
        self.reload()

    def reload(self):
        # NOTE: We could have an URL endpoint to invoke this whenever we have a new CSV file.
        # That would allow to update data without restarting the service.
        logging.info('Loading cities...')
        cities = []
        # Load everything into memory. Under normal circumstances I'd consider using SQL database
        # like PostgreSQL or MySQL; However in this test project I'd like to both avoid setting up the database
        # layer and complicate the code, and also keep things simple as we're dealing only with a few hundred
        # simple objects - hence the in-memory storage would be used.
        with self._source() as f:
            reader = csv.reader(f, delimiter=',')
            column_names = next(reader)
            for row in reader:
                cities.append(dict(zip(column_names, row)))
        self._cities = cities
        # Index cities by name for the quick access in location_data_handler
        # Normally this would be an index in the database
        self._cities_by_name = {city['city'].lower(): city for city in self._cities}
        logging.info(f'Loaded {len(cities)} cities')

    @property
    def cities(self):
        return self._cities

    def get_by_name(self, name):
        return self._cities_by_name.get(name.lower(), None)


class WeatherService(object):
    """
    Provides information from metaweather.com, caches it for a while.
    """
    def __init__(self, base_url='https://www.metaweather.com/api'):
        self._http_client = tornado.httpclient.AsyncHTTPClient()
        self._base_url = base_url
        self._name_to_weather = {}

    def flush(self):
        """
        Since the data is being updated on a daily basis,
        we cache it and flush on a daily basis as well.
        In case of increased load more sophisticated caching strategies should be considered
        as this would result in a temporary performance degradation.

        Alternative approach was to fetch all the data at once from that third-party service.
        However there's no bulk API available, and the owners are asking not to perform more than a few queries
        per minute, so for 500 cities it would take ~10 hours to download all the weather info.
        """
        self._name_to_weather = {}

    async def raw_location_search(self, query: str):
        response = await self._http_client.fetch(f'{self._base_url}/location/search/?query={query}')
        return json.loads(response.body)

    async def raw_location(self, woeid):
        response = await self._http_client.fetch(f'{self._base_url}/location/{woeid}/')
        return json.loads(response.body)

    async def get_weather(self, name):
        name = name.lower()
        if name not in self._name_to_weather:
            woeid_matches = await self.raw_location_search(query=name)
            if woeid_matches:
                best_woeid = woeid_matches[0]['woeid']
            else:
                self._name_to_weather[name] = None
                logging.warning(f'Unknown location: {name}')
                return None
            weather_data = await self.raw_location(best_woeid)
            if not weather_data['consolidated_weather']:
                logging.error(f'No weather data for name {name} (woeid={best_woeid})')
                self._name_to_weather[name] = None
                return None
            latest_weather = sorted(
                weather_data['consolidated_weather'],
                key=lambda item: item['applicable_date'],
                reverse=True,
            )[0]
            self._name_to_weather[name] = latest_weather
        return self._name_to_weather[name]


class CityService(object):
    def __init__(self, city_data_service: CityDataService, weather_service: WeatherService):
        self._city_data_service = city_data_service
        self._weather_service = weather_service

    async def get_data_for_name(self, name):
        city_data = self._city_data_service.get_by_name(name)
        if city_data is None:
            logging.warning(f'Unknown city {name}')
            return None
        weather_data = await self._weather_service.get_weather(name)
        return {
            'city_data': city_data,
            'weather_data': weather_data,
        }

    async def get_data_for_names(self, names):
        names = list(names)
        results = await gen.multi([
            self.get_data_for_name(name)
            for name in names
        ])
        return {
            name.lower(): value
            for name, value in zip(names, results)
            if value is not None
        }

    async def get_scores(self, names):
        data = await self.get_data_for_names(names)
        enumerated_scored_data = enumerate(sorted([
            (self.score(value), value)
            for value in data.values()
        ], reverse=True), start=1)
        city_data = []
        for city_rank, value in enumerated_scored_data:
            city_score, city_data_value = value
            city_name = city_data_value['city_data']['city'].lower()
            city_data.append({
                'city_name': city_name,
                'city_rank': city_rank,
                'city_score': city_score,
            })
        return city_data

    def score(self, city_data):
        """
        Returns a score for the given city data. The score is quite arbitrary,
        so please consider this as a mock-up.
        """
        return float(city_data['city_data']['museums']) * city_data['weather_data']['the_temp']
