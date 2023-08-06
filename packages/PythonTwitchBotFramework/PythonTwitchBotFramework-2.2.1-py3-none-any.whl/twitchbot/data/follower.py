from typing import NamedTuple

__all__ = ['Follower']


class Follower(NamedTuple):
    following_id: int
    following: str
    id: int
    name: str
