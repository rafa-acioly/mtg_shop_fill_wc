import sys
from woocommerce import API
import requests


cli = API(
    url="http://localhost:8888/wordpress",
    consumer_key="ck_11091e59c50bfefdc54856cb57c24ab439c7718f",
    consumer_secret="cs_90ec825e81bdea4bc93fe2ccbd578632a11f472a",
    wp_api=True,
    version="wc/v2"
)


def get_payload(url):
    return requests.get(url).json()


def format_payload(data, category):
    # TODO: Preencher o campo "attributes" no payload com as condições default da carta
    if 'card_faces' in data:
        images = []
        name = ""
        for i, face in enumerate(data['card_faces']):
            images.append({
                "src": face['images_uri']['normal'], "position": i
            })
            name += "{face} / ".format(face=face['name'])
        name = name.strip(" /")
    else:
        images = [{
            "src": data['images_uri']['normal'],
            "position": 0
        }]
        name = data['name']

    return {
        "name": name,
        "sku": "{card_set}{number}".format(card_set=data['set'], number=data['collector_number'])
        "type": "simple",
        "in_stock": False,
        "regular_price": "0.00",
        "description": "",
        "short_description": "",
        "dimensions": {
            "length": "10",
            "width": "10",
            "height": "5"
        }
        "categories": [
            {
                "id": category['id']
            },
        ],
        "images": images
    }


def save_product(cards, category):
    for card in cards:
        payload = format_payload(card, category)
        saved = cli.post("products", payload)

        if saved.status_code == 201:
            card_data = saved.json()
            print("Card saved on ecomm: {name}".format(name=card_data['name']))
        else:
            print("---Error trying to save card: {err}".format(err=saved.text))


def save_category(category):
    category_data = {
        "name": category['name'],
        "slug": category['code'],
        "description": "cards from set {name}".format(name=category['name'])
    }

    return cli.post("products/categories", category_data)


def main():
    set_list = get_payload("https://api.scryfall.com/sets/")

    for card_set in set_list['data']:

        saved = save_category(card_set)

        if not saved.status_code == 201:
            print("Error: {err}".format(err=saved.text))
            continue

        wc_category = saved.json()
        print("Category saved with id:{id} for set: {card_set}".format(
            id=wc_category['id'],
            card_set=wc_category['name'])
        )

        cards_payload = get_payload(card_set['search_uri'])
        save_product(cards_payload['data'], wc_category)

        while cards_payload['has_more']:
            save_product(cards_payload['data'], wc_category)
            cards_payload = get_payload(cards_payload['next_page'])


if __name__ == '__main__': main()
