# pylint: disable=[no-name-in-module,missing-module-docstring,missing-function-docstring]
from types import GeneratorType
from producer.generator import twenty_digits_code


def test_twenty_digits_code():
    generator = twenty_digits_code()
    assert isinstance(generator, GeneratorType), \
        "twenty_digits_code does not return a generator!"

    code = next(generator)
    assert len(code) == 20, \
        "Generated code must have 20 digits!"
