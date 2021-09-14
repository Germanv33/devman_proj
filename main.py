import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse

def shorten_link(token, url):
    payload = {
      'long_url': url
    }

    headers = {
      'Authorization': f'Bearer {token}'
    }

    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink):
    headers = {
      'Authorization': f'Bearer {token}'
    }

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def get_netloc_and_path(url):
    parsed = urlparse(url)
    return f'{parsed.netloc}{parsed.path}'


def is_link_a_bitlink(token, url):
    headers = {
      'Authorization': f'Bearer {token}'
    }

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{get_netloc_and_path(url)}'
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.getenv('BITLY-API-TOKEN')
    parser = argparse.ArgumentParser(
    description='Сокращение ссылок')
    parser.add_argument('link', help='Ссылка для сокращения или битлинк для получения информации о нем')
    link = parser.parse_args().link
    if is_link_a_bitlink(token, url):
        try:
            print('Кол-во кликов: ', count_clicks(token, get_netloc_and_path(url)))
        except requests.exceptions.HTTPError as error:
            exit('Ошибка в получении количества кликов по битлинку:\n{0}'.format(error))
    else:
        try:
            print('Битлинк: ', shorten_link(token, url))
         except requests.exceptions.HTTPError as error:
            exit('Ошибка в создании битлинка:\n{0}'.format(error))

if __name__ == "__main__":
    main()
