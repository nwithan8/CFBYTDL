from classes.cli.choice import Choice


class MultipleChoiceQuestionAndAnswers:
    def __init__(self, question: str, options: list[Choice], answers: list[int]):
        self.question = question
        self.answers = answers
        self.options = options

    def validate(self) -> bool:
        if len(self.answers) > len(self.options):
            return False

        if len(self.answers) <= 0:
            return False

        for answer in self.answers:
            if answer < 0 or answer >= len(self.options):
                return False

        return True

    @property
    def selected_choices(self) -> list[Choice]:
        return [self.options[i] for i in self.answers]
