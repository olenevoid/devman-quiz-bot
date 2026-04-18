import argparse
import re

QUESTION_PATTERN = re.compile(r"^Вопрос (\d+):")
ANSWER_PATTERN = re.compile(r"^Ответ:")
SKIP_PATTERN = re.compile(r"^(Комментарий|Источник|Автор|Зачет):")


def parse_quiz_file(filename):
    with open(filename, encoding="koi8-r") as file:
        content = file.read()

    content = content.replace("\r\n", "\n").replace("\r", "\n")

    questions = []
    current_question = None
    current_answer = None
    current_key = None

    for line in content.split("\n"):
        q_match = QUESTION_PATTERN.match(line)
        a_match = ANSWER_PATTERN.match(line)

        if q_match:
            if current_question is not None and current_answer is not None:
                questions.append(
                    {
                        "question": current_question.strip(),
                        "answer": current_answer.strip(),
                    }
                )
            current_question = line[q_match.end() :].strip()
            current_answer = None
            current_key = "question"
        elif a_match:
            current_answer = line[a_match.end() :].strip()
            current_key = "answer"
        elif SKIP_PATTERN.match(line):
            current_key = None
        elif current_key == "question":
            current_question += "\n" + line
        elif current_key == "answer":
            current_answer += "\n" + line

    if current_question is not None and current_answer is not None:
        questions.append(
            {
                "question": current_question.strip(),
                "answer": current_answer.strip(),
            }
        )

    return questions


def main():
    parser = argparse.ArgumentParser(
        description="Parse a quiz txt file into Q&A pairs"
    )
    parser.add_argument("filename", help="Path to the quiz txt file")
    args = parser.parse_args()

    quiz = parse_quiz_file(args.filename)
    for item in quiz:
        print(f"Q: {item['question']}")
        print(f"A: {item['answer']}")
        print()


if __name__ == "__main__":
    main()
