class timer:

    def __init__(self, interval=1):
        self.load_timer(interval)

    def load_timer(self, interval=1, running=False):
        self.interval = interval
        self.tickable = running
        self.next = 0

    def _tick(self):
        self.next += 1
        if self.next >= self.interval:
            self.next = 0
            self.tick()

    def timer_stop(self):
        self.tickable = False

    def timer_start(self):
        self.tickable = True
        self.next = 0