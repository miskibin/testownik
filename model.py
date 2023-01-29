from pathlib import Path
from miskibin import get_logger
import codecs
import numpy as np
import os
from typing import Generator


class TestCase:
    def __init__(
        self, logger, question: str, answers: list, correct_answer: int
    ) -> None:
        self.logger = logger
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self._tried = 0
        self._correct_anwsered = 0

    def print_question(self, given_answer: int = None) -> None:
        self.logger.info(f"{self.question}\n")
        if given_answer == None:
            self.logger.info(
                "\n".join([f"{i+1}. {answer}" for i, answer in enumerate(self.answers)])
            )
        else:
            for i, answer in enumerate(self.answers):
                if i == self.correct_answer:
                    self.logger.info(f'{i+1}. {answer} {"✔️"}')
                elif i == given_answer:
                    self.logger.error(f'{i+1}. {answer} {"❌"}')
                else:
                    self.logger.debug(f"{i+1}. {answer}")

    def __str__(self) -> str:
        data = f"{self.question}\n\n"
        data += "\n".join([f"{i+1}. {answer}" for i, answer in enumerate(self.answers)])
        return data

    def asdict(self) -> dict:
        return {
            "question": self.question,
            "answers": self.answers,
            "correct_answer": self.correct_answer,
            "_tried": self._tried,
            "_correct_anwsered": self._correct_anwsered,
        }

    @property
    def is_mastered(self) -> bool:
        try:
            return self._correct_anwsered / self._tried > 0.7 and self._tried > 1
        except ZeroDivisionError:
            return False


class Model:
    def __init__(self, number_of_questions=None, data_dir: Path = Path(".")) -> None:

        self.logger = get_logger("Model", lvl="DEBUG", format="%(message)s")
        self.number_of_questions = number_of_questions
        self.data_file = data_dir / "combined.txt"
        self.questions: list[TestCase] = self.load_questions()
        self.question_generator = self.question_generator()

    @property
    def correct_answers(self) -> int:
        return sum([q._correct_anwsered for q in self.questions])

    @property
    def mastered_questions(self):
        return sum(int(q.is_mastered) for q in self.questions)

    def load_questions(self) -> list:
        questions = []
        self.logger.debug(f"Loading question from {self.data_file}")
        answers = []
        with codecs.open(self.data_file, "r", "utf-8") as f:
            question = ""
            correct_answer = ""
            for line in f:
                if line.startswith("X"):
                    correct_answer = self.__parse_correct_answer(line.strip())
                elif line.strip() == "":
                    questions.append(
                        TestCase(self.logger, question, answers, correct_answer)
                    )
                    question = ""
                    answers = []
                    correct_answer = ""
                elif question == "":
                    question = line.strip()
                else:
                    answers.append(line.strip()[3:])
        # random choice of questions
        if self.number_of_questions:
            questions = np.random.choice(questions, self.number_of_questions)
        return questions

    def __parse_correct_answer(self, correct_answer: str) -> int:
        # get index of 1
        idx = correct_answer.index("1") - 1
        return idx

    def end_screen(self) -> None:
        total, correct = 0, 0
        for q in self.questions:
            total += q._tried
            correct += q._correct_anwsered
        self.logger.warning(f"Total answers: {total} Correct answers: {correct}")
        input("Press Enter to exit. . .")

    def console_test(self):
        for question in self.question_generator:
            # clear screen
            os.system("cls" if os.name == "nt" else "clear")
            question.print_question()
            submitted_answer = input("Your answer: ")
            while not submitted_answer.isdigit():
                submitted_answer = input("type 1,2,3 etc.: ")
            question._tried += 1
            os.system("cls" if os.name == "nt" else "clear")
            if int(submitted_answer) - 1 == question.correct_answer:
                question._correct_anwsered += 1
                self.logger.info(
                    f'CORRECT {"😃"}  {"✔️"} {question._correct_anwsered} / {question._tried}'
                )

            else:
                self.logger.error(
                    f'WRONG {"😞"} {"❌"} {question._correct_anwsered} / {question._tried}'
                )
            question.print_question(int(submitted_answer) - 1)
            print(
                f"### Number of mastered questions: {self.mastered_questions()} / {len(self.questions)} ###\n"
            )
            input("Press Enter to continue. . .")
        self.end_screen()

    def question_generator(self) -> Generator[TestCase, None, None]:
        while True:
            idx = np.random.randint(0, len(self.questions))
            if self.mastered_questions >= len(self.questions):
                break
            while self.questions[idx].is_mastered:
                idx = np.random.randint(0, len(self.questions))
            yield self.questions[idx]


if __name__ == "__main__":
    m = Model()
    m.console_test()
