import json
import requests
import datetime

from stockx_wrapper import settings as st


class Stockx:

    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'sec-fetch-dest': 'none',
            'accept': '*/*',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'accept-language': 'en-US'
        }

    def __get(self, url, params=None):
        """
        Perform a http get request.

        :param url: str
        :param params: dict, optional

        :return: dict
            Json format
        """
        response = requests.get(url, headers=self.headers, params=params)
        data = json.loads(response.content)
        return data

    def __post(self, url, params=None, body=None):
        """
        Perform a http post request.

        :param url: str
        :param params: dict, optional
        :param body: dict, optional

        :return:
        """

        response = requests.post(url, headers=self.headers, params=params, json=body)
        data = json.loads(response.content)
        return data

    def get_product_data(self, product_id, country='US', currency='USD', output_keys=None):
        """
        Get product data by product id.

        :param product_id: str
        :param country: str, optional
            Country for focusing market information.
        :param currency: str, optional
            Currency to get. Tested with 'USD' and 'EUR'.
        :param output_keys: list, optional
            List of strings. If not empty, return dict will contain just these keys.

        :return: dict
            Json format. Product info.
        """

        # Format url and get data
        url = f'{st.GET_PRODUCT}/{product_id}'
        params = {
            'includes': 'market',
            'currency': currency,
            'country': country
        }
        data = self.__get(url=url, params=params)
        product = data.get('Product')

        if not product:
            return None

        if not output_keys:
            return product

        return_data = {}

        for key in output_keys:
            return_data[key] = product.get(key)

        return return_data

    def get_product_price_data(self, product_id, start_date='all', end_date=datetime.date.today().strftime('%Y-%m-%d'),
                               intervals=100, country='US', currency='USD'):
        """
        Get product price chart. Average price over time.

        :param product_id: str
        :param start_date: str, optional
            Has to be 'all' or 'YYYY-mm-dd' format.
        :param end_date: str, optional
            Has to be 'YYYY-mm-dd' format.
        :param intervals: str, optional
            Number of rows to get. Time between data returned decreases as this param increases.
        :param country: str, optional
            Country for focusing market information.
        :param currency: str, optional
            Currency to get. Tested with 'USD' and 'EUR'.

        :return: list of dicts

        """

        url = f'{st.GET_PRODUCT}/{product_id}/chart'
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'intervals': intervals,
            'currency': currency,
            'country': country
        }
        data = self.__get(url=url, params=params)

        if not data:
            return None

        return_data = []

        for price, date_interval in zip(data['series'][0]['data'], data['xAxis']['categories']):
            return_data.append({
                'avgPrice': price,
                'dateInterval': date_interval
            })

        return return_data

    def get_product_specific_size(self, product_id, size):
        """
        Get child product from product id with specified size in US size localization.

        :param product_id: str
        :param size: str

        :return: dict
            Json format. Product info with specified size.
        """

        # get parent product
        parent_product = self.get_product_data(product_id)

        # iterate its children until found one that matches asked size
        for child_id, child_data in parent_product['children'].items():
            if child_data['shoeSize'] == size:
                return child_data

        return None

    def search_products(self, product_name):
        """
        Search by product name.

        :param product_name: str

        :return: dict
            First hit
        """

        # Replace spaces to hexadecimal
        product_name = product_name.replace(' ', '%20')

        # Format url and get data
        url = st.SEARCH_PRODUCTS
        params = {
            'page': '1',
            '_search': product_name,
            'dataType': 'product'
        }
        data = self.__get(url=url, params=params)
        products = data.get('Products')

        if products:
            # Return first hit
            return data['Products'][0]

        return None

    def search_products_new_api(self, product_name):
        """
        Uses new API from Algolia. NOT WORKING FOR NOW.

        :param product_name:

        :return:
        """
        # Replace spaces to hexadecimal
        product_name = product_name.replace(' ', '%20')

        body = {
            'params': f'query={product_name}&facets=*&filters='
        }

        data = self.__post(url=st.ALGOLIA_URL, body=body)
        products = data.get('Products')

        if products:
            # Return first hit
            return data['Products'][0]

        return None
