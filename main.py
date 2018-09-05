import sys
from woocommerce import API
import requests


def get_payload(url):
    return requests.get(url).json()


def format_payload(data, category):
    pass


def save_product(product):
    pass


def save_category(category):
    cli = API(
        url="http://localhost:8888/wordpress",
        consumer_key="ck_11091e59c50bfefdc54856cb57c24ab439c7718f",
        consumer_secret="cs_90ec825e81bdea4bc93fe2ccbd578632a11f472a",
        wp_api=True,
        version="wc/v2"
    )

    category_data = {
        "name": category['name'],
        "slug": category['code'],
        "description": "cards from set {set_name}".format(set_name=category['name'])
    }

    return cli.post("products/categories", category_data)


def main():
    set_list = get_payload("https://api.scryfall.com/sets/")

    for card_set in set_list['data']:

        saved = save_category(card_set)

        if saved.status_code == 201:
            response = saved.json()
            print("Category saved with id:{id} for set: {card_set}".format(
                id=response['id'],
                card_set=response['name'])
            )
        else:
            print(saved.text)
            sys.exit()

if __name__ == '__main__': main()
