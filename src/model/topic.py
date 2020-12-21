from dataclasses import dataclass


@dataclass
class Topic:
    title: str
    display_id: int
    msg_id: str
    vote_count: str
    started: bool

