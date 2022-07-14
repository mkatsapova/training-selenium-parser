from typing import Optional

class Question:

    def __init__(self, text: str = '', code: str = '', answers: Optional = None):
        self.text = text
        self.code = code
        self.answers = answers or []



    def __str__(self):
        return f'{self.text} {self.code} {self.answers}'

    def simplify(self) -> dict:
        return {
            'text_question': self.text,
            'code_question': self.code,
            'answers_to_the_question': self.answers
        }
