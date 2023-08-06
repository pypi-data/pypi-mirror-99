from plmbr.pipes import *
from test.tests import check, validate


def test_keep(): (
    (i for i in range(3))
    - keep(lambda i: i > 0)
    > validate(
        lambda i: check(i == 1, i),
        lambda i: check(i == 2, i),
    )
)


def test_batch(): (
    (i for i in range(3))
    - batch(batch_size=2)
    > validate(
        lambda i: check(i == [0, 1]),
        lambda i: check(i == [2]),
    )
)


def test_unbatch():
    def v(l): assert l == [0, 1, 2]
    (
        (i for i in range(3))
        - batch(batch_size=2)
        - unbatch()
        > validate(
            lambda i: check(i == 0),
            lambda i: check(i == 1),
            lambda i: check(i == 2),
        )
    )


def test_drop_fields():
    (
        ({'a': i, 'b': i, 'c': i} for i in range(3))
        - drop_fields('b', 'c')
        > validate(
            lambda o: check(o == {'a': 0}),
            lambda o: check(o == {'a': 1}),
            lambda o: check(o == {'a': 2}),
        )
    )


def test_uniq():
    (
        ({'a': 0, 'b': i // 2, 'c': i} for i in range(3))
        - uniq('a', 'b')
        > validate(
            lambda o: check(o == {'a': 0, 'b': 0, 'c': 0}),
            lambda o: check(o == {'a': 0, 'b': 1, 'c': 2}),
        )
    )


def test_tee():
    (
        [1, 2, 3]
        - tee(
            keep(lambda i: i < 3)
            - to(lambda i: i * 2),

            to(lambda i: i * 10)
        )
        > validate(
            lambda i: check(i == 2),
            lambda i: check(i == 10),
            lambda i: check(i == 4),
            lambda i: check(i == 20),
            lambda i: check(i == 30),
        )
    )


def test_append():
    res = [8]
    (
        range(4)
        - keep(lambda i: i > 1)
        > append(res)
    )
    assert res == [8, 2, 3]
