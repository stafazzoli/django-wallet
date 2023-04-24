from typing import Callable, Dict, Tuple

from wallets.schemas import RequestStates

transition_callbacks: Dict[Tuple[str, RequestStates], Callable[[str], None]] = {}


def register_transition_callback(enter_trigger: RequestStates | None = None,
                                 exit_trigger: RequestStates | None = None):
    def decorate(func: Callable[[str], None]):
        if enter_trigger:
            transition_callbacks['enter', enter_trigger] = func
        elif exit_trigger:
            transition_callbacks['exit', exit_trigger] = func

        return func

    return decorate
