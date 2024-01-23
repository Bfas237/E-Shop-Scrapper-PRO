import os
import json


class SiteConfig:
    def __init__(self, site_name: str = "") -> None:
        self.site_name = site_name

    def initialize_default_config(self):
        default_config = {
            self.site_name: {
                "ey_point": {
                    "type": {"class": "", "html": ""},
                    "data": "",
                    "desc": "used to detect entry point",
                },
                "pt_item": {
                    "type": {"class": "", "html": ""},
                    "data": "",
                    "desc": "used to detect single product",
                },
                "pt_name": {
                    "type": {"class": "", "html": ""},
                    "data": "",
                    "desc": "used to detect product name",
                },
                "pt_image": {
                    "type": {"class": "", "html": ""},
                    "data": "",
                    "desc": "used to detect product image",
                },
                "pt_link": {
                    "type": {"class": "", "html": ""},
                    "data": "",
                    "desc": "used to detect product link",
                },
                "pn_mark": {
                    "type": {"class": "", "html": ""},
                    "data": "",
                    "desc": "used to detect pagination",
                },
                "pn_num": {
                    "type": {"class": "", "html": ""},
                    "data": "",
                    "desc": "used to detect pagination numbering",
                },
                "pt_mark": {
                    "type": {"class": "", "html": ""},
                    "data": "",
                    "desc": "used to determine the number of pages to scrape",
                },
            }
        }
        return default_config

    def init(self):
        config_file = "siteconfig.json"
        
        if not os.path.exists(config_file):
            open(config_file, 'w').write('{}')

        with open(config_file, 'r+') as f:
            try:
                data = json.load(f)
            except Exception as error:
                data = {}

            default_config = self.initialize_default_config()
            data[self.site_name] = default_config[self.site_name]

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    site_config = SiteConfig("WooCommerce")
    site_config.init()
