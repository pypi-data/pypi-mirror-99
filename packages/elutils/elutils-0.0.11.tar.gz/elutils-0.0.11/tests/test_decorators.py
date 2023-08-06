import os
import unittest
from unittest.mock import MagicMock
import requests
from elutils.decorators import *
from elutils.osio import list_files



class TestDecorators(unittest.TestCase):

    # Sample function calling an external API and gives different results based on the args
    @staticmethod
    @cache_decayable_data(datetime.timedelta(hours=12))
    def get_exchange_rate_from_ECB(base_currency='USD'):
        url = f'https://api.exchangeratesapi.io/latest?base={base_currency.upper()}'
        print(f'Getting rates from ECB with base {base_currency}')
        resp = requests.get(url)
        print(f'Got rates from ECB with base {base_currency}')
        return resp.json()

    def setUp(self) -> None:
        '''Delete any cache files before running any test'''
        for file in list_files('./',filter='.decay.p'):
            os.remove(file)


    def test_buffer_function_that_takes_arg(self):
        '''Functions that take args are not expected to give back the same result.
        If the results is the same something is wrong'''
        result_1 = self.get_exchange_rate_from_ECB('USD')
        result_2 = self.get_exchange_rate_from_ECB("EUR")

        self.assertNotEqual(result_1,result_2)


    def test_cache_function_with_no_arg(self):

        # make sure no cached files in the test folder
        self.assertEqual(0,len(list_files('./',filter='.decay.p')))

        # both will default to USD
        result_1 = self.get_exchange_rate_from_ECB()
        requests.get = MagicMock()
        result_2 = self.get_exchange_rate_from_ECB()
        # assert that request was not called after it was mocked out
        requests.get.assert_not_called()

        self.assertEqual(result_1,result_2)


