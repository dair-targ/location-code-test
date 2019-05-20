import tornado.web

from app.location_data_handler import LocationHandler
from app.location_comparison_handler import LocationComparisonHandler
from app.services import CityDataService, WeatherService, CityService


class LocationCodeApplication(tornado.web.Application):
    """
    A specific application that holds both the URL mapping specific for location-code-test
    and also holds links to background services like in-memory representation of european_cities.csv
    or the weather data.

    In tornado application is straightforwardly available in all the handlers,
    so we would be able to access all those background services easily.
    """
    def __init__(self):
        self.city_data_service = CityDataService()
        self.weather_service = WeatherService()
        self.city_service = CityService(
            self.city_data_service,
            self.weather_service,
        )

        super(LocationCodeApplication, self).__init__([
            (r"/location-data/([a-zA-Z0-9]*)?", LocationHandler, {}),
            (r"/location-comparison/cities=\[(\S+)\]", LocationComparisonHandler, {}),
        ])

    def run_daily(self):
        self.weather_service.flush()

