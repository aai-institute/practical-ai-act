from enum import IntEnum


class SalaryBand(IntEnum):
    """
    Salary bands we consider as sensible ranges for observed incomes.

    Since salaries are always positive, these values are right-bounds,
    i.e., the actual "entry level" salary band (see below) would range
    from 0$-35000$.
    """

    ENTRY_LEVEL = 35000
    LOWER_MID_RANGE = 55000
    MID_RANGE = 85000
    UPPER_MID_RANGE = 120000


RANDOM_STATE = 25
