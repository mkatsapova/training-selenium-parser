class Question(object):

    def __init__(self, text='', code='', answers=None):
        self.text = text
        self.code = code
        self.answers = answers if answers else []

    def __str__(self):
        return f'{self.text} {self.code} {self.answers}'

    # def append_json(self):
    #     all_questions_list = []
    #     all_questions_list.append(
    #         {
    #             'text_question': self.text,
    #             'code_question': self.code,
    #             'answers_to_the_question': self.answers
    #         }
    #     )
    #
    #     with open('result.json', 'w') as write_file:
    #         json.dump(all_questions_list, write_file, indent=4, ensure_ascii=False)
