__all__ = [
    'PollData',
    'get_channel_poll_by_id',
    'get_active_channel_polls',
    'active_polls',
    'get_active_channel_poll_count',
    'poll_event_processor_loop',
    'POLL_CHECK_INTERVAL_SECONDS'
]

from asyncio import sleep
from collections import defaultdict, Counter
from datetime import datetime
from typing import List, DefaultDict, Optional, Tuple, Set, Any

from ..channel import Channel

POLL_CHECK_INTERVAL_SECONDS = 2

active_polls: DefaultDict[str, List['PollData']] = defaultdict(list)


class PollData:
    _last_id = 0

    def __init__(self, channel: Channel, owner: str, title: str, duration_seconds: float, *choices: str):
        self.duration_seconds: float = duration_seconds
        self.choices: List[str] = list(choices)
        self.choices_normalized: List[str] = list(map(self._format, choices))
        self.channel: Channel = channel
        self.votes: Counter[int, int] = Counter()
        self.voters: Set[str] = set()
        self.owner = owner
        self.title = title
        self.start_time = datetime.now()

        PollData._last_id += 1
        self.id = PollData._last_id

    @property
    def all_choice_ids(self):
        return {i + 1 for i, _ in enumerate(self.choices)}

    @property
    def done(self):
        return (datetime.now() - self.start_time).total_seconds() > self.duration_seconds

    @property
    def seconds_left(self):
        return max(0, round(self.duration_seconds - (datetime.now() - self.start_time).total_seconds(), 1))

    def choice_to_str(self, choice_id: int, default: Any = None):
        if choice_id - 1 >= len(self.choices):
            return default
        return self.choices[choice_id - 1]

    def _format(self, value: str) -> str:
        return value.lower().strip()

    def is_valid_vote(self, choice_id: int) -> bool:
        return choice_id in self.all_choice_ids

    def add_choice(self, choice: str):
        normalized = self._format(choice)
        if normalized not in self.choices_normalized:
            self.choices.append(choice)
            self.choices_normalized.append(normalized)

    def remove_choice(self, choice: str):
        normalized = self._format(choice)
        if normalized in self.choices_normalized:
            self.choices.remove(choice)
            self.choices_normalized.remove(normalized)

    def has_already_voted(self, username: str):
        return username.lower().strip() in self.voters

    def add_vote(self, voter: str, choice_id: int) -> bool:
        if not self.is_valid_vote(choice_id):
            return False

        self.votes[choice_id] += 1
        self.voters.add(voter.lower().strip())
        return True

    def format_poll_results(self, reverse: bool = True):
        """
        returns a joined string of the poll's choices, ordered by vote

        if reverse is True, then it will order by highest to lowest votes
        else, order from lowest to highest

        :param reverse: if true, results are sorted by high to low vote; if false, low to high
        :return:
        """
        return ' ~ '.join(
            f'[{self.votes[id]} votes] {text}'
            for id, text
            in sorted(
                enumerate(self.choices, start=1),
                key=lambda items: self.votes[items[0]],
                reverse=reverse
            )
        )

    def formatted_choices(self):
        return ' '.join(f'{i}) {v}' for i, v in enumerate(self.choices, start=1))

    async def end(self):
        # poll is removed from active poll from the event loop that calls .end()
        # scroll down to poll_event_processor_loop() to see
        from ..event_util import forward_event, Event
        forward_event(Event.on_poll_ended, self.channel, self, channel=self.channel.name)

    async def start(self):
        active_polls[self.channel_name].append(self)
        from ..event_util import forward_event, Event
        forward_event(Event.on_poll_started, self.channel, self, channel=self.channel.name)

    @property
    def channel_name(self):
        return self.channel.name.lower().strip()

    def __eq__(self, other):
        return isinstance(other, PollData) and other.id == self.id

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'

    def __str__(self):
        return f'<{self.__class__.__name__} title={self.title!r} id={self.id}>'


def get_channel_poll_by_id(channel: str, id: int) -> Optional[PollData]:
    return next(filter(lambda x: x.id == id, active_polls[channel]), None)


def get_active_channel_polls(channel: str) -> Tuple[PollData]:
    return tuple(poll for poll in active_polls[channel] if not poll.done)


def get_active_channel_poll_count(channel: str) -> int:
    return sum(1 for poll in active_polls[channel] if not poll.done)


async def poll_event_processor_loop():
    to_remove = []
    while True:
        for channel_name, polls in active_polls.items():
            for poll in polls:
                if poll.done:
                    to_remove.append((channel_name, poll))

        for channel_name, poll in to_remove:
            await poll.end()
            active_polls[channel_name].remove(poll)

        to_remove.clear()
        await sleep(POLL_CHECK_INTERVAL_SECONDS)
