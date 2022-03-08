import switch.detect
from switch.detect import Detector
from switch.switch import Switch

detector = Detector([
    Switch('SW701', 7990),
    Switch('SW702', 13488),
    Switch('SW703', 18488),
    Switch('SW704', 23439),
    Switch('SW705', 28196),
    Switch('SW706', 32733),
    Switch('SW707', 65535),
])

switch = detector.detect(32731)
print("Switch pressed: {}".format(switch.label))
