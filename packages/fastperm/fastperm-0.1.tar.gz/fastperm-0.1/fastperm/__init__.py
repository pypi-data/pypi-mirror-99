import attr
import math
import numpy as np

from typing          import Dict, Optional
from numbers         import Integral
from collections.abc import Sized, Iterable, Iterator
from numpy.random    import RandomState

@attr.s
class ChunkedRange:
    n:          int                   = attr.ib(validator=lambda i, a, x: x >= 1) # type: ignore
    chunk_size: int                   = attr.ib(default=2 ** 20, validator=lambda i, a, x: x >= 1)
    chunks:     Dict[int, np.ndarray] = attr.ib(init=False, default={})

    def __len__(self) -> int:
        return self.n

    def _get_chunk(self, chunk_index: int) -> np.ndarray:
        chunk: Optional[np.ndarray] = self.chunks.get(chunk_index)

        if chunk is None:
            chunk = np.arange(self.chunk_size * chunk_index, min(self.chunk_size * (chunk_index + 1), self.n),
                dtype=np.uint64)
            self.chunks[chunk_index] = chunk

        return chunk

    def __getitem__(self, i: int) -> np.uint64:
        if not (0 <= i < self.n):
            raise IndexError()

        chunk_index = i // self.chunk_size
        return self._get_chunk(chunk_index)[i - self.chunk_size * chunk_index]

    def __setitem__(self, i: int, x: Integral) -> None:
        if not (0 <= i < self.n):
            raise IndexError()

        chunk_index = i // self.chunk_size
        self._get_chunk(chunk_index)[i - self.chunk_size * chunk_index] = x

@attr.s
class Permutation(Sized, Iterable[np.uint64]):
    n:  int         = attr.ib(validator=lambda i, a, x: x >= 1) # type: ignore
    rs: RandomState = attr.ib(default=np.random.RandomState())
    i:  int         = attr.ib(init=False, default=0)

    def __attrs_post_init__(self) -> None:
        self.perm = ChunkedRange(self.n)

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[np.uint64]:
        return self

    def __next__(self) -> np.uint64:
        if self.i >= self.n:
            raise StopIteration()

        j = self.rs.randint(self.i, self.n)
        self.perm[self.i], self.perm[j], self.i = self.perm[j], self.perm[self.i], self.i + 1
        return self.perm[self.i - 1]
