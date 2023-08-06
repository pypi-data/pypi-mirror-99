# encoding: utf-8
import requests
import os
from .exceptions import (
    OcException, 
    TiException,
    MlException,
    SkyHubException,
    VariavelAmbienteException
)
from .extra import cache, clear_cache
from .models import MercadoLivreToken
import logging
import time

API_BLOQUEADA = '6'


def get_env(env_name):
    '''
    Retorna valor de uma variável de ambiente
    Param: (env_name) String Variável de ambiente ser extraída

    Return: String
    '''
    env_value = os.getenv(env_name)
    if env_value is None:
        raise VariavelAmbienteException(f'{env_name} não configurada')
    return env_value


def req_opencart(url, verb='GET', **kwargs):
    '''
    Faz uma requisição nas apis do Opencart.
    Realiza retry 3x com timeout incremental de 15 segundos
    Param: (url) Url api
    Param: (verb) Verbo ser usado, GET default, POST, PUT, DELETE
    Param: (data) Conteúdo de Json

    Return: (Json) Payload
    '''
    TOKEN = get_env('OPENCART_TOKEN')
    logger = kwargs['logger'] if 'logger' in kwargs\
        else logging.getLogger(__name__)
    retry = kwargs['retry'] if 'retry' in kwargs else 0
    tempo_espera = kwargs['tempo_espera'] if 'tempo_espera' in kwargs\
        else 15
    data = kwargs['data'] if 'data' in kwargs else None
    env = get_env('AMBIENTE')
    headers = {'key': TOKEN, 'content-type': 'application/json'}
    response = requests.request(verb, url, json=data, headers=headers)
    if response.status_code not in (200, 404) and retry < 3:
        logger.info('Erro chamada opencart: ' + str(response.content))
        if env == 'produção':
            time.sleep(tempo_espera)
        retry = retry + 15
        tempo_espera = tempo_espera * 2
        return req_opencart(url, verb=verb,
                            data=data, retry=retry, tempo_espera=tempo_espera)
    try:
        payload = response.json()
        return payload
    except ValueError as e:
        logger.error(e)
        raise OcException(response.text)


def req_tiny(url, verb='GET', **kwargs):
    '''
    Faz uma requisição nas apis do Tiny.
    Realiza retry 3x com timeout incremental de 15 segundos
    Param: (url) Url api
    Param: (verb) Verbo ser usado, GET default, POST, PUT, DELETE

    Return: (Json) Payload
    '''
    logger = kwargs['logger'] if 'logger' in kwargs\
        else logging.getLogger(__name__)
    retry = kwargs['retry'] if 'retry' in kwargs else 0
    tempo_espera = kwargs['tempo_espera'] if 'tempo_espera' in kwargs\
        else 15
    env = get_env('AMBIENTE')

    logger.info('request Tiny ' + verb + ': ' + url)
    response = requests.request(verb, url)
    logger.info('response Tiny: ' + str(response.content))
    try:
        payload = response.json()
    except ValueError:
        raise TiException(response.text)
    if response.status_code == 200 and 'erros' not in payload['retorno']:
        return response.json()
    elif 'erros' in payload['retorno'] \
        and payload['retorno']['codigo_erro'] == API_BLOQUEADA and retry < 3:
        logger.info('(Tiny) Api bloqueada retry em: ' + str(tempo_espera))
        if env == 'produção':
            time.sleep(tempo_espera)
        retry = retry + 1
        tempo_espera = tempo_espera * 2
        return req_tiny(url, retry=retry, tempo_espera=tempo_espera)
    mensagem_erro = ', '.join(map(lambda x: x['erro'],
                                  payload['retorno']['erros']))
    raise TiException(mensagem_erro)


def req_skyhub(url, verb='GET', **kwargs):
    '''
    Faz uma requisição nas apis do Skyhub.
    Realiza retry 3x com timeout incremental de 15 segundos
    Param: (url) Url api
    Param: (verb) Verbo ser usado, GET default, POST, PUT, DELETE
    Param: (data) Conteúdo de Json

    Return: (Json) Payload
    '''
    logger = kwargs['logger'] if 'logger' in kwargs\
        else logging.getLogger(__name__)
    retry = kwargs['retry'] if 'retry' in kwargs else 0
    tempo_espera = kwargs['tempo_espera'] if 'tempo_espera' in kwargs\
        else 15
    data = kwargs['data'] if 'data' in kwargs else None
    env = get_env('AMBIENTE')
    TOKEN = get_env('SKYHUB_TOKEN')
    EMAIL = get_env('SKYHUB_EMAIL')

    logger.info('request Skyhub' + verb + ': ' + url)
    headers = {'X-Api-Key': TOKEN, 'X-User-Email': EMAIL,
               'content-type': 'application/json'}
    response = requests.request(verb, url, json=data, headers=headers)
    logger.info('response Skyhub: ' + str(response.content))
    if response.status_code == 204:
        return True
    elif response.status_code in [500, 400] and retry < 3:
        logger.info('(Skyhub) Api bloqueada retry em: ' + str(tempo_espera))
        if env == 'produção':
            time.sleep(tempo_espera)
        retry = retry + 1
        tempo_espera = tempo_espera * 2
        return req_skyhub(url, verb=verb, retry=retry, tempo_espera=tempo_espera)
    raise SkyHubException(response.text)

@cache
def __get_token__():
    ambiente = get_env('AMBIENTE')
    if ambiente.lower() == 'test' or ambiente.lower() == 'teste':
        return MercadoLivreToken('a', 'b')
    url_base = get_env('URL_OC_BASE')
    response = req_opencart(f'{url_base}/token/mercadolivre')
    if 'access_token' not in response:
        raise Exception('Favor configurar token \
            do Mercado Livre na api do Opencart!')
    return MercadoLivreToken(response['access_token'],
                      response['refresh_token'])


def __refresh_token__():
    token = __get_token__()
    url_refresh = get_env('MERCADOLIVRE_URL_REFRESH_TOKEN')
    client_id = get_env('MERCADOLIVRE_CLIENT_ID')
    secret = get_env('MERCADOLIVRE_SECRET')
    url = url_refresh + '&client_id={0}&client_secret={1}&refresh_token={2}'.format(
        client_id, secret, token.refresh_token
    )
    response = requests.post(url)
    if response.status_code == 200:
        body = response.json()
        access_token = 'Bearer ' + body['access_token']
        refresh_token = body['refresh_token']

        url_base = get_env('URL_OC_BASE')
        url = f'{url_base}/token/mercadolivre'
        body = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        req_opencart(url, 'PUT', data=body)
        clear_cache('__get_token__-()')
    else:
        raise Exception('Não foi possível refresh no token do Mercado Livre')


def req_mercado_livre(url, verb='GET', **kwargs):
    TOKEN = __get_token__().access_token

    logger, retry, tempo_espera, data, env, headers =\
        __params_req_ml__(url, verb, kwargs, TOKEN)

    # request
    response = requests.request(verb, url, json=data, headers=headers)
    logger.info(f'response Mercado Livre: {response.text}')
    if response.status_code == 401:
        __refresh_token__()
        return req_mercado_livre(url, verb=verb,
                                 data=data,
                                 retry=retry,
                                 tempo_espera=tempo_espera)
    if response.status_code not in (200, 404, 400) and retry < 3:
        logger.info('Erro chamada Mercado Livre: ' + str(response.content))
        if env == 'produção':
            time.sleep(tempo_espera)
        retry = retry + 15
        tempo_espera = tempo_espera * 2
        return req_mercado_livre(url, verb=verb,
                            data=data, retry=retry, tempo_espera=tempo_espera)
    try:
        payload = response.text
        if verb == 'GET':
            payload = response.json()
            if 'error' in payload and len(payload['cause']) > 0:
                raise MlException(payload['cause'][0]['message'])
            return payload
        return payload
    except ValueError as e:
        logger.error(e)
        raise MlException(response.text)

def __params_req_ml__(url, verb, kwargs, TOKEN):
    logger = kwargs['logger'] if 'logger' in kwargs\
        else logging.getLogger(__name__)
    retry = kwargs['retry'] if 'retry' in kwargs else 0
    tempo_espera = kwargs['tempo_espera'] if 'tempo_espera' in kwargs\
        else 15
    data = kwargs['data'] if 'data' in kwargs else None
    env = get_env('AMBIENTE')
    headers = {'Authorization': TOKEN, 'content-type': 'application/json'}
    logger.info('request Mercado Livre ' + verb + ': ' + url)
    return logger,retry,tempo_espera,data,env,headers


def convert_api_response_to_object(columns, registers):
    response = list()
    for register in registers:
        object = dict()
        i = 0
        for column in columns:
            object[column] = register[i]
            i += 1
        response.append(object)
    return response