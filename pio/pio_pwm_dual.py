from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

# We use two pins for side set: both start out as 0
@asm_pio(sideset_init=(PIO.OUT_LOW, PIO.OUT_LOW))
def pwm_bridge():
    pull(noblock) .side(0b00)  # clear A & B
    mov(x, osr)  # keep most recent pull data stashed in X, for recycling by pull
    mov(y, isr)  # ISR must be preloaded with PWM count max
    
    label("loop_a")
    jmp(x_not_y, "skip_a")  # continue if x == y (time's up)
    nop() .side(0b01)       # set a = 1, b = 0
    label("skip_a")
    jmp(y_dec, "loop_a")    # if y == 0, loop again, also y--

    mov(y, isr) [2] .side(0b00)  # reload y and clear a & b
    label("loop_b")
    jmp(x_not_y, "skip_b")
    nop()         .side(0b10)    # set a = 0, b = 1
    label("skip_b")
    jmp(y_dec, "loop_b")


class HBridge:
    def __init__(self, sm_id, base_pin, max_count, count_freq):
        self._sm = StateMachine(sm_id, pwm_bridge, freq=2 * count_freq, sideset_base=Pin(base_pin))

        self._sm.put(max_count)  # to the output FIFO

        # Use exec() to load max count into ISR
        self._sm.exec("pull()")  # pull from the output FIFO to the output shift register (OSR)
        self._sm.exec("mov(isr, osr)")  # copy from the OSR to the ISR (used here as a third scratch register)

        # Start the state machine
        self._sm.active(1)

        # Store the max count for use by #set, below
        self._max_count = max_count

    def set(self, value):
        # Minimum value is -1 (completely turn off), 0 actually still produces narrow pulse
        value = max(value, -1)
        value = min(value, self._max_count)
        self._sm.put(value)


# GPIO 15 (pin 20 on Pico) is LED A, 16 is LED B
pwm = HBridge(sm_id=0, base_pin=15, max_count=180, count_freq=1_500_000)
pwm.set(170)

#while True:
#    for i in range(50):
#        pwm.set(i)
#        sleep(0.01)
#    for i in range(50):
#        pwm.set(50-i)
#        sleep(0.01)
    
