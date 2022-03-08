class Detector:
    def __init__(self, switches):
        self.switches = switches

    def detect(self, value):
        # print("Attempting to detect value: {}".format(value))
        # print("Switches: {}".format(self.switches))

        for index, switch in enumerate(self.switches):
            if value < switch.threshold:
                return switch

        return self.switches[len(self.switches)]


