from __future__ import annotations

from classes.cli.question_answer import QuestionAndAnswers


def send_message(message: str) -> None:
    print(message)


def ask_question(prompt: str) -> str:
    return input(f"{prompt} ")


def ask_yes_or_no_question(prompt: str) -> bool:
    prompt = f"{prompt} [y/n]: "
    answer = ask_question(prompt=prompt)
    if answer.lower().startswith('y'):
        return True
    return False


def process_choice(choice: str, choices: list) -> str | None:
    try:
        choice = int(choice)
        if choice < 1 or choice > len(choices):
            raise ValueError
        return choices[choice - 1]
    except ValueError:
        return None


def _ask_for_all_choices(prompt: str, choices: list) -> str:
    for index, choice in enumerate(choices):
        prompt += f"\n{index + 1}) {choice}"
    prompt += "\nChoice:"
    return ask_question(prompt=prompt)


def ask_multiple_choices(prompt: str, choices: list) -> list[str]:
    answer = _ask_for_all_choices(prompt=prompt, choices=choices)
    selections = [process_choice(choice=selection.strip(), choices=choices) for selection in answer.split(',')]
    if not all(selections):
        return ask_multiple_choices(prompt=prompt, choices=choices)
    return selections


def ask_specific_number_range_of_choices(prompt: str, choices: list, lower_number: int = 1,
                                         higher_number: int = None) -> list[str | None] | None | list[str]:
    if lower_number > len(choices):
        raise ValueError(f"Number of choices is smaller than number of requested choices.")
    if higher_number < lower_number:
        raise ValueError(f"Higher number is smaller than lower number.")
    if higher_number is None:
        prompt = f"{prompt} (Choose {lower_number} or more, separated by , ): "
    elif higher_number == lower_number:
        prompt = f"{prompt} (Choose {lower_number}, separated by , ): "
    elif lower_number == 1:
        prompt = f"{prompt} (Choose up to {higher_number}, separated by , ): "
    selections = ask_multiple_choices(prompt=prompt, choices=choices)
    if higher_number and len(selections) > higher_number:
        print(f"Number of selected choices is larger than {higher_number}.")
        return None
    if lower_number and len(selections) < lower_number:
        print(f"Number of selected choices is smaller than {lower_number}.")
        return None
    return selections


def ask_specific_number_of_choices(prompt: str, choices: list, number: int = None) -> list[str | None] | None | list[str]:
    return ask_specific_number_range_of_choices(prompt=prompt, choices=choices, lower_number=number, higher_number=number)


def confirm_answer(answer: str) -> bool:
    return ask_yes_or_no_question(prompt=f"Is '{answer}' correct?")


def confirm_choices(choices: list) -> bool:
    return ask_yes_or_no_question(prompt=f"Is '{', '.join(choices)}' correct?")


class CommandLine:
    def __init__(self):
        self._answers = {}

    def ask_question(self, prompt: str, y_n: bool = False, confirm: bool = False) -> None:
        if y_n:
            answer = ask_yes_or_no_question(prompt=prompt)
        else:
            answer = ask_question(prompt=prompt)
        if not answer:
            self.ask_question(prompt=prompt, y_n=y_n, confirm=confirm)
        elif confirm and not confirm_answer(answer=answer):
            self.ask_question(prompt=prompt, y_n=y_n, confirm=confirm)
        else:
            self._answers[len(self._answers.keys())] = QuestionAndAnswers(question=prompt, answers=[answer])

    def ask_choices(self, prompt: str, choices: list, least_number_selections: int = 1,
                    most_number_selections: int = None, confirm: bool = False) -> None:
        answer = ask_specific_number_range_of_choices(prompt=prompt, choices=choices,
                                                      lower_number=least_number_selections,
                                                      higher_number=most_number_selections)
        if not answer:
            self.ask_choices(prompt=prompt, choices=choices, least_number_selections=least_number_selections,
                             most_number_selections=most_number_selections, confirm=confirm)
        elif confirm and not confirm_choices(choices=answer):
            self.ask_choices(prompt=prompt, choices=choices, least_number_selections=least_number_selections,
                             most_number_selections=most_number_selections, confirm=confirm)
        else:
            self._answers[len(self._answers.keys())] = QuestionAndAnswers(question=prompt, answers=answer)

    def get_answers(self, question_number: int) -> list[str] | None:
        question_number -= 1
        if question_number not in self._answers.keys():
            return None
        return self._answers[question_number].answers

    def get_choices(self, question_number: int) -> list[str] | None:
        return self.get_answers(question_number=question_number)

    @property
    def all_answers(self) -> list[list[str] | None]:
        return [self.get_answers(question_number=question_number) for question_number in self._answers]

    def get_question(self, question_number: int) -> str | None:
        question_number -= 1
        if question_number not in self._answers.keys():
            return None
        return self._answers[question_number].question

    @property
    def all_questions(self) -> list[str]:
        return [self.get_question(question_number=question_number) for question_number in self._answers]
