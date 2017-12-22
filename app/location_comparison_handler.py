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

    def get(self, *args, **kwargs):
        """
        Retrieves information about multiple cities, rates them and returns a ranking and score for each city.
        :param args:
        :param kwargs:
        :return:
        """
        response = {'city_data': [{'city_name': 'greatplace',
                                   'city_rank': 1,
                                   'city_score': 8.4},
                                  {'city_name': 'okplace',
                                   'city_rank': 2,
                                   'city_score': 5.2},
                                  {'city_name': 'badplace',
                                   'city_rank': 3,
                                   'city_score': 2.2}
                                  ]}

        self.set_status(HTTPStatus.OK)
        self.write(json.dumps(response))
