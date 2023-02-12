from typing import Sequence

__all__ = ["batch_it"]


def batch_it(sequence: Sequence, number_of_batches: int):
    for i in range(0, len(sequence), number_of_batches):
        yield sequence[i : i + number_of_batches]
