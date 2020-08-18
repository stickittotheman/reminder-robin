from dataclasses import dataclass


@dataclass
class Role:
    name: str

    def __init__(self, inc_name):
        self.name = inc_name

