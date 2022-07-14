import datetime
import json
import time
from typing import TYPE_CHECKING

from app.models import Question
from app.settings import RESULTS_FOLDER_PATH
from selenium.common.exceptions import NoSuchElementException

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver


class ProgHubParser(object):
    def __init__(self, driver: 'WebDriver', lang: str):
        self.driver = driver
        self.lang = lang

    def parse(self):
        self.go_to_tests_page()
        self.parse_question_page()


    def go_to_tests_page(self):
        self.driver.get('https://proghub.dev/tests')

        btn_cookie = self.driver.find_element_by_css_selector('div.cookie__notification_btn a')
        btn_cookie.click()

        self.driver.refresh()

        test_card_elems = self.driver.find_elements_by_tag_name('div.testCard>a')

        for elem in test_card_elems:
            lang_link = elem.get_attribute('href')

            # if first part of link at this page is different than initial link
            if self.lang in lang_link:
                language = lang_link.split('/')[-1]

                self.driver.get('https://proghub.dev/t/' + language)
                btn_question_example = self.driver.find_element_by_css_selector('a.btn')
                btn_question_example.click()

                time.sleep(1)
                break

    def parse_question_page(self):
        question = Question()
        self.fill_question_text(question)
        self.fill_question_code(question)
        self.fill_question_answer(question)
        self.save_to_json(question)

        print(question)

    def fill_question_text(self, question):
        self.driver.refresh()
        try:
            question_text_elm = self.driver.find_element_by_css_selector('h1.title>span')
            question.text = question_text_elm.text

        except NoSuchElementException:
            print('Question text missing')

    def fill_question_code(self, question):
        try:
            code_elm = self.driver.find_element_by_css_selector('div.code')
            question.code = code_elm.text
            time.sleep(1)
        except NoSuchElementException:
            pass

    def fill_question_answer(self, question):
        self.driver.refresh()
        try:
            btn_answer = self.driver.find_element_by_css_selector('div.answer')
            btn_answer.click()
            time.sleep(1)

            try:
                btn_control = self.driver.find_element_by_css_selector('.btn.btn-primary')
                btn_control.click()
                time.sleep(3)

                answer_elems = self.driver.find_elements_by_css_selector('div.answer')
                for answer_elem in answer_elems:
                    answer = [answer_elem.text,
                              True if 'correct' == answer_elem.get_attribute('class').split(' ')[-1] else False]
                    # if response code error is '500' - all answers are False

                    question.answers.append(answer)
                    time.sleep(0)
            except NoSuchElementException:
                print('No control button. Question was visited')

        except NoSuchElementException:
            print('Something went wrong! Refresh the page or return to the main page')

    # noinspection PyMethodMayBeStatic
    def save_to_json(self, question: Question):
        path = RESULTS_FOLDER_PATH.joinpath(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json')

        with open(path, mode='w', encoding='utf-8') as write_file:
            json.dump(question.simplify(), write_file, indent=4, ensure_ascii=False)
