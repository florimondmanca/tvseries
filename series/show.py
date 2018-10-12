from dataclasses import dataclass


@dataclass
class Show:
    """
    Class to represent the details of a show

    """

    id: int
    title: str
    small_logo_path: str
