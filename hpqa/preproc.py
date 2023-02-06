import re
import string
from pathlib import Path

from hpqa.constants import DATA_PATH

__all__ = ["read_book", "get_book_chapters"]

num_chapters_in_book = [17, 18, 22, 37, 38, 30, 36]


def read_book(title_path):
    with open(title_path, "r") as current_file:
        text = current_file.read()
        text = text.replace("\n", "").replace("\u2014", "-")
        text = re.sub("P\s?a\s?g\s?e\s? \|\s+\d+\s?Harry Potter and [\w\s]+\s?-\s?J.K. Rowling", " ", text)
        text = re.sub("\.\.\.", " ", text)
        text = re.sub("\s\s+", " ", text)
        text = re.sub("\t", " ", text)
        text = text.strip("/").strip()
    return text


def get_book_chapters(book_number, data_path=DATA_PATH):
    start_i = 0 if book_number == 1 else sum(num_chapters_in_book[: book_number - 1])
    end_i = start_i + num_chapters_in_book[book_number - 1]

    book = read_book(data_path / f"Book{book_number}.txt")

    with open(data_path / "chapter_names.txt", "r") as f:
        chapter_names = [line.strip() for line in f.readlines()]

    chapter_spans = {}
    for c in chapter_names[start_i:end_i]:
        s = re.search(c.upper(), book)
        chapter_spans[c.upper()] = s.span()

    assert len(chapter_spans) == num_chapters_in_book[book_number - 1]

    start_spans = [s[1] for s in chapter_spans.values()]
    end_spans = [s[0] for s in chapter_spans.values()][1:] + [len(book)]

    for c, s, e in zip(chapter_spans.keys(), start_spans, end_spans):
        chapter_spans[c] = (s, e)

    chapters = {}
    for c, span in chapter_spans.items():
        chapters[c] = book[span[0] : span[1]].strip().strip(string.digits).strip()

    chapters["WIKIPEDIA"] = read_book(data_path / f"wikipedia_book_{book_number}.txt")

    return chapters
