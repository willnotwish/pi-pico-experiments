class Detector:
    def __init__(self, switches, adc):
        self.switches = switches
        self.adc = adc

    def detect(self):
        value = self.adc.read_u16()
        for index, switch in enumerate(self.switches):
            if value < switch.threshold:
                return switch

        return None
