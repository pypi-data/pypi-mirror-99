import os
import requests_mock
import pytest
from libmp.api import __get_token__, __refresh_token__, req_mercado_livre
import json

PFX_JSON = 'test/json'
URL_REFRESH_TOKEN = 'http://mock-mltoken.com.br/oauth/token?grant_type=refresh_token'
URL_OC = 'http://mock-oc.com.br/api.php'


class TestApiMercadoLivre:

    contador = 0

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        monkeypatch.setenv('MERCADOLIVRE_URL_REFRESH_TOKEN',
                           URL_REFRESH_TOKEN)
        monkeypatch.setenv('MERCADOLIVRE_SECRET',
                           'secret')
        monkeypatch.setenv('MERCADOLIVRE_CLIENT_ID',
                           '1')
        monkeypatch.setenv('AMBIENTE', 'test')
        monkeypatch.setenv('URL_OC_BASE', URL_OC)
        monkeypatch.setenv('OPENCART_TOKEN', '123')
        yield
        os.remove('libmp.cache')

    def test_get_token(self, monkeypatch):

        with requests_mock.Mocker() as m:
            m.get('http://mock-oc.com.br/api.php/token/mercadolivre',
                    text=open(f'{PFX_JSON}/body_token.json').read())
            token = __get_token__()
            assert token.access_token == 'A'
            assert token.refresh_token == 'B'

            token = __get_token__()
            assert token.access_token == 'A'
            assert token.refresh_token == 'B'
            assert m.call_count == 1

    def test_token_refresh(self, monkeypatch):
        with requests_mock.Mocker() as m:
            m.post(f'{URL_REFRESH_TOKEN}&client_id=1&client_secret=secret&refresh_token=B',
                  text=open(f'{PFX_JSON}/body_refresh_token.json').read())
            m.get(f'{URL_OC}/token/mercadolivre',
                  text=open(f'{PFX_JSON}/body_token.json').read())
            m.put(f'{URL_OC}/token/mercadolivre', text='1')
            __refresh_token__()
            assert m.call_count == 3
            body_request = json.loads(m._adapter.request_history[2].text)
            assert body_request['access_token'] == 'Bearer C'
            assert body_request['refresh_token'] == 'D'

    def test_token_expirado(self, monkeypatch):
        with requests_mock.Mocker() as m:
            m.get(f'{URL_OC}/token/mercadolivre',
                  text=open(f'{PFX_JSON}/body_token.json').read())
            token = __get_token__()
            assert token.access_token == 'A'
            assert token.refresh_token == 'B'
            assert m.call_count == 1

            # Alterado a api esperado que retorne o valor cacheado
            m.get(f'{URL_OC}/token/mercadolivre',
                  text=open(f'{PFX_JSON}/body_token_alterado.json').read())
            token = __get_token__()
            assert token.access_token == 'A'
            assert token.refresh_token == 'B'
            assert m.call_count == 1


            m.post(f'{URL_REFRESH_TOKEN}&client_id=1&client_secret=secret&refresh_token=B',
                  text=open(f'{PFX_JSON}/body_refresh_token.json').read())
            m.put(f'{URL_OC}/token/mercadolivre', text='1')
            __refresh_token__()
            token = __get_token__()
            assert token.access_token == 'Z'
            assert token.refresh_token == 'X'
            assert m.call_count == 4

    def __mock_response__(self, request, context):
        if self.contador == 0 and '/chamada-teste' in request.path:
            self.contador = 1
            context.status_code = 401
            return open(f'{PFX_JSON}/body_ml.json').read()
        else:
            context.status_code = 200
            return open(f'{PFX_JSON}/body_ml.json').read()

    def test_req_mercadolivre(self, monkeypatch):
        # Garantir que tenha cache e que mesmo assim limpe o cache
        with requests_mock.Mocker() as m:
            # mock get token
            m.get(f'{URL_OC}/token/mercadolivre',
                  text=open(f'{PFX_JSON}/body_token.json').read())
            # request mercado livre
            m.get(f'http://mock-ml.com.br/chamada-teste',
                  text=self.__mock_response__)

            # mock __refresh_token__
            m.post(f'{URL_REFRESH_TOKEN}&client_id=1&client_secret=secret&refresh_token=B',
                  text=open(f'{PFX_JSON}/body_refresh_token.json').read())
            m.get(f'{URL_OC}/token/mercadolivre',
                  text=open(f'{PFX_JSON}/body_token.json').read())
            m.put(f'{URL_OC}/token/mercadolivre', text='1')
            response = req_mercado_livre('http://mock-ml.com.br/chamada-teste')
            assert response['status'] is True
            assert response['id'] == "MLID1010"

