"""Generates URL for imgproxy image processing server"""

__version__ = '0.3'

import hmac
import hashlib
import base64


class ImgProxy:
    def __init__(self, key, salt, server_url):
        self._key = bytes.fromhex(key)
        self._salt = bytes.fromhex(salt)
        self.server_url = server_url

    def generate(self, url, processing_options, extension):
        b64_url = base64.urlsafe_b64encode(
            str.encode(url)).rstrip(b'=').decode()

        processing_options_str = ""
        for command in processing_options:
            processing_options_str += f"{command}:{processing_options[command]}/"

        print(processing_options_str)
        path = f'/{processing_options_str}/{b64_url}'
        if extension is not None:
            path += f'.{extension}'

        sha256_hmac = hmac.new(self._key, self._salt +
                               str.encode(path), digestmod=hashlib.sha256)

        protection = base64.urlsafe_b64encode(
            sha256_hmac.digest()).rstrip(b'=').decode()

        return f'{self.server_url}/{protection}{path}'
