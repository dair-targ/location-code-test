import unittest

import tornado
from tornado.testing import AsyncTestCase, gen_test

from app.services import CityDataService, WeatherService
from io import StringIO


class TestCityDataService(unittest.TestCase):
    def test_reload(self):
        service = CityDataService(lambda: StringIO('''index,city,country,population,bars,museums,public_transport,crime_rate,average_hotel_cost
            1,Moscow,Russia,8297000,1659,1936,4,9,258
            2,LONDON,UK,7074000,12733,707,9,1,286'''))
        self.assertEqual(2, len(service.cities))


class TestWeatherService(AsyncTestCase):
    @gen_test
    async def test_location_search(self):
        service = WeatherService()
        response = await service.raw_location_search('London')
        self.assertIn('woeid', response[0])
