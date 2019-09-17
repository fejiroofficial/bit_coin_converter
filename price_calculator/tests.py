from django.test import TestCase

# Create your tests here.
import json

from django.test import Client, TestCase

from price_calculator.test_fixture import convert


class BaseConfiguration(TestCase):
    """
    Base configuration file for all tests.
    """

    @classmethod
    def setUpClass(cls):

        # We need to first run setUpClass function that we
        # inherited from TestCase.
        super(BaseConfiguration, cls).setUpClass()

        # Set up test client for all test classes
        # that will inherit from this class.
        cls.client = Client()

    @classmethod
    def query(cls, query: str = None):
        # Method to run all queries and mutations for tests.
        body = dict()
        body['query'] = query
        response = cls.client.post(
            '/graphql/', json.dumps(body), content_type='application/json')
        json_response = json.loads(response.content.decode())
        return json_response


class TestOrders(BaseConfiguration):
    '''Class to test conversion operation
    '''

    def test_bitcoin_conversion(self):
        '''Method to test that conversion was successful
        '''
        response = self.query(convert.format(type="sell"))
        self.assertNotIn('errors', response)
        self.assertIn('data', response)
        self.assertIn('calculatePrice', response['data'])
        self.assertTrue(isinstance(
            response['data']['calculatePrice'], dict))
    
    def test_wrong_transaction_type(self):
        '''Method to test that conversion was unsuccessful
        '''
        response = self.query(convert.format(type="bPP"))
        self.assertIn('errors', response)
        self.assertIn('message', response['errors'][0])
        self.assertEqual(response['errors'][0]['message'], 'This type of transaction must either be a buy or a sell')
