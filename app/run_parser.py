import time

# "chromedriver_binary" for import path of chromedriver.
# noinspection PyUnresolvedReferences
import chromedriver_binary
from app.parser import ProgHubParser
from selenium import webdriver


def run_parser() -> None:
    driver = webdriver.Chrome()
    try:
        parser = ProgHubParser(driver=driver, lang='python-3-basic')
        parser.parse()
    finally:
        time.sleep(3)
        driver.quit()
