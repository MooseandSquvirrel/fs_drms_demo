class Room():
    def __init__(self, number, occupants, status, reason, closed, closure_ids):
        self.number = number
        self.occupants = occupants
        self.status = status
        self.reason = reason
        self.closed = closed
        self.closure_ids = closure_ids
