import logging

from tornado.web import RequestHandler
from http import HTTPStatus
import json


class LocationHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def initialize(self, **kwargs):
        super().initialize()

    async def get(self, *args, **kwargs):
        """
        Retrieve information about a city.
        :param args:
        :param kwargs:
        :return:
        """
        city_name = args[0]
        city_data = await self.application.city_service.get_data_for_name(city_name)
        if city_data is None:
            self.set_status(
                HTTPStatus.BAD_REQUEST,
            )
            logging.warning(f'Requested unknown city "{city_name}"')
            return

        response = {
            'city_name': city_data['city_data']['city'].lower(),
            'current_temperature': city_data['weather_data']['the_temp'],
            'current_weather_description': city_data['weather_data']['weather_state_name'],
            'population': int(city_data['city_data']['population']),
            'bars': int(city_data['city_data']['bars']),
            'city_score': 6.8,
        }

        self.set_status(HTTPStatus.OK)
        self.write(json.dumps(response))
