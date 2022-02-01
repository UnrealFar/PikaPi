
class Trade:
    """A PikaPi trade between two users."""
    def __init__(self, payload: dict):
        self.acc1 = payload.pop("acc1", None)
        self.acc2 = payload.pop("acc2", None)

