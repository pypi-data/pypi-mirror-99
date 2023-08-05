from enum import Enum


class SolverType(str, Enum):
    ATTRIBUTE = "ATTRIBUTE"
    COMPLEX = "COMPLEX"
    CONNECTION = "CONNECTION"
    COMPLEX_CONNECTION = "COMPLEX_CONNECTION"
    FILTER = "FILTER"
