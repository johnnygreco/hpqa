import gc
from typing import Sequence

import torch

__all__ = ["batch_it", "empty_cache"]


def batch_it(sequence: Sequence, number_of_batches: int):
    for i in range(0, len(sequence), number_of_batches):
        yield sequence[i : i + number_of_batches]


def empty_cache(*args):
    for arg in args:
        del arg
    gc.collect()
    torch.cuda.empty_cache()
