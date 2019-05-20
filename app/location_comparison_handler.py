from tornado.web import RequestHandler
from http import HTTPStatus
import json


class LocationComparisonHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def initialize(self, **kwargs):
        super().initialize()

    async def get(self, *args, **kwargs):
        """
        Retrieves information about multiple cities, rates them and returns a ranking and score for each city.
        :param args:
        :param kwargs:
        :return:
        """
        city_data = await self.application.city_service.get_scores(args[0].split(','))
        response = {'city_data': city_data}

        self.set_status(HTTPStatus.OK)
        self.write(json.dumps(response))
