from .woocommerce import Woocommerce

def get_payload(url):
    return requests.get(url).json()


def format_payload(data):
    pass


def save_product_to_wc(product):
    pass


def save_category(category):
    category_data = {
        "name": category['name'],
        "image": category['icon_svg_uri'],
        "slug": category['code'],
        "description": "cards from set {set_name}".format(set_name=category['name']),
        "image": category['icon_svg_uri']
    }

    return Woocommerce.post("products/categories", category_data)


def main():
    set_list = get_payload("https://api.scryfall.com/sets/")

    for card_set in set_list:
        print("Getting card from set: {set_name}".format(set_name=card_set['name'])

        saved = save_category(card_set)

        if saved.status_code == 200:
            print("Category created for set: ".format(card_set['name']))

if __name__ == '__main__': main()
