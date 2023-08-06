import random
from src.parallel import PBarParallel, delayed


def _func(x):
    return x**2


def test_functionality_on_dummy_function():
    prl = PBarParallel(n_jobs=48)
    result = prl(total=1000)(delayed(_func)(i) for i in range(1000))
    prl(desc="doing important stuff")(delayed(_func)(i) for i in range(4))
    for i, r in enumerate(result):
        assert i**2 == r