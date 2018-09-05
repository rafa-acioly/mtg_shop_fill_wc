from woocommerce import API
import requests


class Woocommerce:

    def __init__(self):
        self.cli = API(
            url="http://localhost:8888/wordpress",
            consumer_key="ck_11091e59c50bfefdc54856cb57c24ab439c7718f",
            consumer_secret="cs_90ec825e81bdea4bc93fe2ccbd578632a11f472a",
            wp_api=True,
            version="wc/v2"
        )


    @staticmethod
    def post(path, payload):
        return self.cli.post(path, payload)
