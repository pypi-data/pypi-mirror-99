"""Module to test SwxApiClient"""

from os import environ
import unittest
import pytest
import openapi_client
from openapi_client.swx_api_client import SwxApiClient
from openapi_client.api import collections_api
from openapi_client.model.collection_request import CollectionRequest
from openapi_client.model.collection_update_request import CollectionUpdateRequest
from openapi_client.api import models_api
from openapi_client.model.model_request import ModelRequest
from openapi_client.model.model_update_request import ModelUpdateRequest


CONFIGURATION = openapi_client.Configuration(
    host=environ.get('swx_host', None)
)
if environ.get('verify_ssl', True) in ['False', 'false']:
    CONFIGURATION.verify_ssl = False


def get_swxclient(
        client_id=environ.get('client_id', None),
        client_secret=environ.get('client_secret', None),
        scope=environ.get('scope', None),
        defer_auth=False
):
    """Create and return an instance of API client"""
    return SwxApiClient(
        configuration=CONFIGURATION,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        defer_auth=defer_auth
    )

def get_api_instance(api_name):
    """Create and return an instance of required API class"""
    if api_name == 'collections':
        return collections_api.CollectionsApi(api_client=get_swxclient())
    elif api_name == 'models':
        return models_api.ModelsApi(api_client=get_swxclient())
    else:
        return None

class PositiveSwxApiClientTestClass(unittest.TestCase):
    """Class that tests positive test cases for SwxApiClient"""

    @pytest.mark.run(order=1)
    def test_implicit_do_auth(self):
        """Testing SwxApiClient implicit do_auth()"""
        try:
            # Create an instance of API client
            swxclient = get_swxclient()
            print(swxclient.default_headers)
            assert  swxclient.default_headers['Authorization'] != None
        except Exception as error:
            raise Exception('While executing test_do_auth(): {}'
                            .format(error))

    @pytest.mark.run(order=2)
    def test_explicit_do_auth(self):
        """Testing SwxApiClient explicit do_auth()"""
        try:
            # Create an instance of API client
            swxclient = get_swxclient(defer_auth=True)
            print(swxclient.default_headers)
            assert 'Authorization' not in swxclient.default_headers
            swxclient.do_auth()
            assert  swxclient.default_headers['Authorization'] != None
        except Exception as error:
            raise Exception('While executing test_do_auth(): {}'
                            .format(error))

    @pytest.mark.run(order=3)
    def test_list_collections(self):
        """Testing list collections request"""
        # Get an instance of the collections API class
        collection_api = get_api_instance('collections')

        # Get a list of existing collections for a given space
        space = "testspace123"
        try:
            api_response = collection_api.list_collections(space)
            print(api_response)
            assert api_response is not None
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->list_collections: %s\n" % e)

    @pytest.mark.run(order=4)
    def test_add_collection(self):
        """Testing add collection request"""
        # Get an instance of the collections API class
        collection_api = get_api_instance('collections')

        # Create a collection
        space = "testspace123"
        collection_request = CollectionRequest(
            name="test_collection_1",
            description="My collection"
        )
        try:
            api_response = collection_api.add_collection(space, collection_request)
            print(api_response)
            assert api_response is not None
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->add_collection: %s\n" % e)

    @pytest.mark.run(order=5)
    def test_update_collection(self):
        """Testing update collection request"""
        # Get an instance of the collections API class
        collection_api = get_api_instance('collections')

        # Update a collection
        space = "testspace123"
        collection_name = "test_collection_1"
        collection_update_request = CollectionUpdateRequest(
            description="My test collection"
        )
        try:
            api_response = collection_api.update_collection(
                space,
                collection_name,
                collection_update_request
            )
            print(api_response)
            assert api_response is not None
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->update_collection: %s\n" % e)

    @pytest.mark.run(order=6)
    def test_delete_collection(self):
        """Testing delete collection request"""
        # Get an instance of the collections API class
        collection_api = get_api_instance('collections')

        # Delete an existing collection
        space = "testspace123"
        collection_name = "test_collection_1"
        try:
            api_response = collection_api.delete_collection(space, collection_name)
            print(api_response)
            assert api_response is None
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->delete_collection: %s\n" % e)

    @pytest.mark.run(order=7)
    def test_list_models(self):
        """Testing list models request"""
        # Get an instance of the models API class
        model_api = get_api_instance('models')

        # Get a list of all existing models in a given collection
        space = "testspace123"
        collection_name = "testcoll1"
        try:
            api_response = model_api.list_models(space, collection_name)
            print(api_response)
            assert api_response is not None
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->list_models: %s\n" % e)

    @pytest.mark.run(order=8)
    def test_add_model(self):
        """Testing add model request"""
        # Get an instance of the models API class
        model_api = get_api_instance('models')

        # Create a model in a given collection and space
        space = "testspace123"
        collection_name = "testcoll1"
        model_request = ModelRequest(
            name="test_model_01",
            description="My model"
        )
        try:
            api_response = model_api.add_model(space, collection_name, model_request)
            print(api_response)
            assert api_response is not None
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->add_model: %s\n" % e)

    @pytest.mark.run(order=9)
    def test_update_model(self):
        """Testing update model request"""
        # Get an instance of the models API class
        model_api = get_api_instance('models')

        # Update a model of a given collection and space
        space = "testspace123"
        collection_name = "testcoll1"
        model_name = "test_model_01"
        model_update_request = ModelUpdateRequest(
            description="My test model"
        )
        try:
            api_response = model_api.update_model(
                space,
                collection_name,
                model_name,
                model_update_request
            )
            print(api_response)
            assert api_response is not None
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->update_model: %s\n" % e)

    @pytest.mark.run(order=10)
    def test_delete_model(self):
        """Testing delete model request"""
        # Get an instance of the models API class
        model_api = get_api_instance('models')

        # Delete a model from a given collection and space
        space = "testspace123"
        collection_name = "testcoll1"
        model_name = "test_model_01"
        try:
            api_response = model_api.delete_model(space, collection_name, model_name)
            print(api_response)
            assert api_response is None
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->delete_model: %s\n" % e)


class NegativeSwxApiClientTestClass(unittest.TestCase):
    """Class that tests negative test cases for SwxApiClient"""

    def test_do_auth_error1(self):
        """Testing SwxApiClient do_auth() error"""
        exception = False
        try:
            # Create an instance of API client with incorrect client_id
            get_swxclient(client_id='test')
        except Exception as error:
            print(error)
            exception = True

        self.assertEqual(exception, True)

    def test_do_auth_error2(self):
        """Testing SwxApiClient do_auth() error"""
        expected_error_msg = 'While initializing SwxApiClient: ' \
            'Cannot initialize SwxApiClient with [client_id, client_secret, scope]={}'.format(
                [environ.get('client_id', None), None, environ.get('scope', None)])
        try:
            # Instantiate API client without passing all parameters
            # client_secret not passed here
            SwxApiClient(
                configuration=CONFIGURATION,
                client_id=environ.get('client_id', None),
                scope=environ.get('scope', None)
            )
        except Exception as error:
            print(error)
            assert '{}'.format(error) == expected_error_msg
