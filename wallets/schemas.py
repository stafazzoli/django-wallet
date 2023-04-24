from enum import Enum


class RequestKinds(Enum):
    Deposit = 'Deposit'
    Withdraw = 'Withdraw'

    def __str__(self):
        return self.value


class RequestStates(Enum):
    Init = 'Init'
    Pending = 'Pending'
    Succeed = 'Success'
    Failed = 'Failed'

    def __str__(self):
        return self.value


class RequestTransitions:
    Success = 'Success'
    Fail = 'Fail'


transitions = [
    [RequestTransitions.Success, RequestStates.Init, RequestStates.Succeed],
    [RequestTransitions.Fail, RequestStates.Init, RequestStates.Failed],
]
