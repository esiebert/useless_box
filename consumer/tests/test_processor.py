# pylint: disable=[missing-module-docstring,missing-function-docstring]
import pytest
from consumer.processor import sum_numbers


@pytest.mark.parametrize('code, expected', [
    ("<_q*M'2c.eN8Esg>{", 10),
    ("CPEBin9St6MpaRe82iaj", 25),
    ("JhaURRtFWXLYQfewFCJE", 0),
    ("1234567890", 45),
    ("", 0),
], ids=[
    "Alphanumeric + symbols",
    "Alphanumeric",
    "Alphabetic",
    "Numeric",
    "Empty",
])
def test_sum_numbers(code, expected, mocker):
    # Disable processing time for this test
    mocker.patch('consumer.processor.randint', return_value=0)
    result = sum_numbers(code)
    assert result == expected, \
        "Incorrect summation result!"
