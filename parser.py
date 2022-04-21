import time

from model import Question
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ProgHubParser(object):
    def __init__(self, driver, lang):
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
                btn_control = self.driver.find_element_by_css_selector('.control button')
                btn_control.click()
                time.sleep(1)

                answer_elems = self.driver.find_elements_by_css_selector('div.answer')
                for answer_elem in answer_elems:
                    answer = [answer_elem.text,
                              False if 'correct' != answer_elem.get_attribute('class').split(' ')[-1] else True]

                    question.answers.append(answer)
                    time.sleep(2)
            except NoSuchElementException:
                print('No control button. Question was visited')

        except NoSuchElementException:
            print('Something went wrong! Refresh the page or return to the main page')







def main():
    driver = webdriver.Chrome()
    parser = ProgHubParser(driver, 'python-3-basic')
    parser.parse()





if __name__ == '__main__':
    main()
