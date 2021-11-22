class QuestionAndAnswer:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

    def __str__(self):
        return self.question

    def __repr__(self):
        return self.question

    def __eq__(self, other):
        return self.question == other.question and self.answer == other.answer

    def __hash__(self):
        return hash(self.question)
