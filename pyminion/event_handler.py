from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pyminion.event_registry import EventRegistry


class EventHandler(Protocol):
    def register_events(self, event_registry: "EventRegistry") -> None:
        raise NotImplementedError("register_events is not implemented")
