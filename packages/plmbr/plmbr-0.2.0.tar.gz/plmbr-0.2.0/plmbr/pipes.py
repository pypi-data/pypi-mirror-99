"""
A collection of reusable pipes.
"""
from collections import deque
from plmbr.pipe import Pipe, I, O
from typing import Any, Callable, Dict, Iterator, List, Tuple
import json
from itertools import islice
from tqdm import tqdm
import random
import itertools


def null(it: Iterator[I]) -> Iterator[I]:
    return it


class json_loads(Pipe[str, Dict]):
    def pipe(self, items: Iterator[str]) -> Iterator[Dict]:
        return (json.loads(item) for item in items)


class json_dumps(Pipe[Dict, str]):
    def pipe(self, items: Iterator[Dict]) -> Iterator[str]:
        return (json.dumps(item) for item in items)


class batch(Pipe[I, List[I]]):
    def __init__(self, batch_size=64) -> None:
        self.batch_size = batch_size

    def pipe(self, it: Iterator[I]) -> Iterator[List[I]]:
        return iter(lambda: list(islice(it, self.batch_size)), [])


class unbatch(Pipe[List[I], I]):
    def pipe(self, lists: Iterator[List[I]]) -> Iterator[I]:
        return (item for l in lists for item in l)


class progress(Pipe[I, I]):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def pipe(self, it: Iterator[I]) -> Iterator[I]:
        return iter(tqdm(it, **self.kwargs))


class to(Pipe[I, O]):
    def __init__(self, f: Callable[[I], O]):
        self.f = f

    def pipe(self, items: Iterator[I]) -> Iterator[O]:
        for item in items:
            yield self.f(item)


class keep(Pipe[I, I]):
    def __init__(self, filter):
        self.filter = filter

    def pipe(self, it: Iterator[I]) -> Iterator[I]:
        return filter(self.filter, it)


class drop_fields(Pipe[Dict, Dict]):
    def __init__(self, *fields: str):
        self.fields = fields

    def pipe(self, items: Iterator[Dict]) -> Iterator[Dict]:
        for item in items:
            for field in self.fields:
                del item[field]

            yield item


class uniq(Pipe[Dict, Dict]):
    def __init__(self, *fields: str):
        self.fields = fields
        self.set: set = set()

    def pipe(self, items: Iterator[Dict]) -> Iterator[Dict]:
        for item in items:
            i = frozenset({field: item[field] for field in self.fields}.items())
            if i in self.set:
                continue

            self.set.add(i)
            yield item


class sample(Pipe[Any, Any]):
    def __init__(self, prob, seed=2020):
        self.prob = prob
        self.seed = seed

    def pipe(self, items: Iterator[Dict]) -> Iterator[Dict]:
        random.seed(self.seed)
        for item in items:
            if random.uniform(0, 1) < self.prob:
                yield item


class sample_by(Pipe[Dict, Dict]):
    def __init__(self, prob, key, seed=2020):
        self.prob = prob
        self.key = key
        self.seed = seed

    def pipe(self, items: Iterator[Dict]) -> Iterator[Dict]:
        random.seed(self.seed)
        good, bad = set(), set()
        for item in items:
            key = item[self.key]
            if key in bad:
                continue

            if key in good:
                yield item
                continue

            if random.uniform(0, 1) < self.prob:
                good.add(key)
                yield item

            else:
                bad.add(key)


class window(Pipe):
    def __init__(self, size):
        self.size = size
        self.window = deque([])

    def pipe(self, it: Iterator[I]) -> Iterator[tuple]:
        for e in it:
            self.window.append(e)
            if len(self.window) == self.size:
                yield tuple(self.window)
                self.window.popleft()


class log(Pipe[I, I]):
    def pipe(self, items: Iterator[I]) -> Iterator[I]:
        for item in items:
            print(item)
            yield item


class save(Pipe[I, I]):
    def __init__(self, file) -> None:
        self.file = file

    def pipe(self, items: Iterator[I]):
        with open(self.file, 'w') as f:
            for item in items:
                print(item, file=f)
                yield item


class append(Pipe[I, I]):
    def __init__(self, to) -> None:
        self.to = to

    def pipe(self, items: Iterator[I]):
        for item in items:
            self.to.append(item)
            yield item


class tee(Pipe[I, I]):
    def __init__(self, *pipes) -> None:
        self.pipes = pipes

    def pipe(self, items: Iterator[I]) -> Iterator[I]:
        its = deque(
            pipe.pipe(items)
            for items, pipe
            in zip(itertools.tee(items, len(self.pipes)), self.pipes)
        )

        while its:
            try:
                it = its.popleft()
                yield next(it)
                its.append(it)
            except:
                ...
