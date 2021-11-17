class QuestionAndAnswers:
    def __init__(self, question: str, answers: list[str]):
        self.question = question
        self.answers = answers

    def __str__(self):
        return self.question

    def __repr__(self):
        return self.question

    def __eq__(self, other):
        return self.question == other.question and self.answers == other.answers

    def __hash__(self):
        return hash(self.question)

    def get_choice(self, choice_number: int):
        if choice_number < 1 or choice_number > len(self.answers):
            raise ValueError("Choice number must be between 1 and {}".format(len(self.answers)))
        return self.answers[choice_number - 1]

    def get_first_choice(self):
        return self.get_choice(1)

    def get_last_choice(self):
        return self.get_choice(len(self.answers))
