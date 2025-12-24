from utils import utils  # general utils
from utils import config_wizard  # config wizard
from utils.selenium import selenium  # selenium scripts


###### CONFIG FILES ######
CREDS_LOCATION = "conf/horizontium.conf"
URL_LOCATION = "conf/urls.conf"
##########################


def main():
    """user interface"""

    # check configs
    if not utils.path_exists(URL_LOCATION):
        urls_link = "https://github.com/timrosu/horizontium/blob/main/conf/urls.conf"
        print(
            f"Url dictionary file at {URL_LOCATION} is missing. You can download it from {urls_link}"
        )
    if not utils.path_exists(CREDS_LOCATION):
        print("launching config_wizard...")  # temporary
        # config_wizard()

    # load config
    config = utils.load_config(CREDS_LOCATION)
    url = utils.load_config(URL_LOCATION)

    # launch selenium script
    selenium.main(config, url)


if __name__ == "__main__":
    main()
