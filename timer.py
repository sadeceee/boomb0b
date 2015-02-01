class timer:

    def __init__(self, interval = 1, running = 1):

        self.load_timer(interval)

    def load_timer(self, interval = 1, running = 0):

        self._interval = interval
        self._tickable = running
        self._next = 0

    def _tick(self):
        self._next += 1
        if self._next >= self._interval:
            self._next = 0
            self.tick()

    def timer_stop(self):
        self._tickable = 0

    def timer_start(self):
        self._tickable = 1
        self._next = 0