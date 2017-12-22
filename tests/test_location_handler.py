import numbers
import os
from tornado.testing import AsyncHTTPTestCase
from tornado.escape import json_decode
from tornado.web import Application
from http import HTTPStatus
from app.location_data_handler import LocationHandler
from app.location_comparison_handler import LocationComparisonHandler

os.environ['ASYNC_TEST_TIMEOUT'] = '10'


class TestLocationHandler(AsyncHTTPTestCase):

    def get_app(self):

        return Application([(r"/location-data/([a-zA-Z0-9]*)?", LocationHandler, {}),
                            (r"/location-comparison/cities=\[(\S+)\]", LocationComparisonHandler, {})])

    def test_get_location_data(self):
        """
        Get the location data for a city and check the
        :return:
        """
        for city_name in ['dublin', 'London', 'Copenhagen']:
            response = self.fetch(
                path="/location-data/{}".format(city_name),
                method='GET'
            )
            self.assertEqual(response.code, HTTPStatus.OK)
            self.check_city_response(response, city_name.lower())

    def test_get_bad_location_data(self):
        """
        Try to get the location data for an unknown city. Check to make sure that a BAD_REQUEST is returned.
        :return:
        """
        city_name = 'notarealplace'
        response = self.fetch(
            path="/location-data/{}".format(city_name),
            method='GET'
        )
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST, "Incorrect response for an unknown city")

    def test_compare_cities(self):
        city_names = ['dublIn', 'london', 'lisbon', 'Amsterdam', 'CopenHaGeN']

        response = self.fetch(
            path="/location-comparison/cities=[{}]".format(','.join(city_names)),
            method='GET'
        )
        self.assertEqual(response.code, HTTPStatus.OK)
        self.check_comparison_response(response, city_names)

    #  Checks for responses #

    def check_city_response(self, response, city_name):
        """
        Checks that the response for an individual city contains the relevant information.
        :param response: The raw response from the route
        :param city_name: The name of the requested city
        :return:
        """
        body = json_decode(response.body)
        self.assertEqual(type(body), dict)
        self.assertIsNotNone(body.get('city_name'))
        self.assertIsNotNone(body.get('current_temperature'))
        self.assertIsNotNone(body.get('current_weather_description'))
        self.assertIsNotNone(body.get('population'))
        self.assertIsNotNone(body.get('bars'))
        self.assertIsNotNone(body.get('city_score'))

        self.assertEqual(body.get('city_name'), city_name)

        self.assertIsInstance(body.get('current_temperature'), numbers.Number, "The current temperature is not numeric")
        self.assertIsInstance(body.get('current_weather_description'), str, "The weather description is not a string")
        self.assertIsInstance(body.get('population'), int, "The population is not an integer")
        self.assertIsInstance(body.get('bars'), int, "The number of bars is not an integer")
        self.assertIsInstance(body.get('city_score'), numbers.Number, "The city score is not a number")

    def check_comparison_response(self, response, city_names):
        """
        Various checks on the results of a comparison response. Checks include the correct fields as well as the
        ordering of the ranking.
        :param response: The raw response from the route
        :param city_names: A list if the city names used for comparison
        :return:
        """
        body = json_decode(response.body)

        # General checks for the correct information
        self.assertIsNotNone(body.get('city_data'))
        data = body.get('city_data')
        # Ensure the results contain each city name
        self.assertEqual(len(data), len(city_names), "Incorrect number of cities returned")
        self.assertTrue(set([x.lower() for x in city_names]) <= {x.get('city_name').lower() for x in data},
                        "All cities not included in the results")
        for city_result in data:
            self.assertIsInstance(city_result, dict, "Incorrect type for the city_data entries")
            self.assertTrue({'city_name', 'city_rank', 'city_score'} <= set(city_result.keys()),
                            "Missing entries in a city_data entry")
            self.assertIsInstance(city_result.get('city_rank'), int, "Incorrect type of city_rank")
            self.assertIsInstance(city_result.get('city_score'), numbers.Number, "Incorrect type of city_score")
            self.assertIsInstance(city_result.get('city_name'), str, "Incorrect type of city_name")

        # Get  the ranks and scores for the cities and ensure they are in the right order (low->high for ranks and
        # high->low for scores).
        results = {x.get('city_rank'): x.get('city_score') for x in data}
        ranks = sorted(results.keys())
        scores = sorted(results.values(), reverse=True)
        for entry, score in zip(ranks, scores):
            self.assertEqual(results.get(entry), score, "The city rankings are not in the correct order")
