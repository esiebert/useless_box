"""Module holding implementation of processors."""

def sum_numbers(body: str) -> int:
    """Sums all the numbers in a string."""
    return sum([int(val) for val in str(body) if val.isnumeric()])
