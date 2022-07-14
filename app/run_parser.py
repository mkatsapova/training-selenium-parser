import time

# "chromedriver_binary" for import path of chromedriver.
# noinspection PyUnresolvedReferences
import chromedriver_binary
from selenium import webdriver

from app.parser import ProgHubParser


def run_parser() -> None:
    driver = webdriver.Chrome()
    try:
        parser = ProgHubParser(driver=driver, lang='python-3-basic')
        parser.parse()
    finally:
        time.sleep(3)
        driver.quit()
