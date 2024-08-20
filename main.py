import sys
import time
import math
import os
import tty
import termios
import select

# Torque in foot/pounds
torque = 100
rpm = 10000
cylinders = 2
# Bore and Stroke are in Millimeters - mm
bore = 108   
stroke = 75
bore_cm = bore / 10
stroke_cm = stroke / 10
gasket_thickness = 0

def horsepower_calc(torque, rpm):
    return int(torque * (rpm / 5252))
horsepower = horsepower_calc(torque, rpm)

def displacement_calc(bore, stroke, cylinders):
    bore_cm, stroke_cm = bore / 10, stroke / 10
    return 0.7854 * bore_cm * bore_cm * stroke_cm * cylinders
displacement = displacement_calc(bore, stroke, cylinders)

def crank_stroke(bore_cm, displacement, cylinders):
    return displacement / (cylinders * (math.pi / 4) * (bore_cm ** 2))
stroke = crank_stroke(bore_cm, displacement, cylinders)

#def compression_ratio_calc(displacement, compressed_volume):
#    return (displacement + compressed_volume) / compressed_volume
#compression_ratio = compression_ratio_calc(displacement, compressed_volume)

def get_input_non_blocking():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

running = True

while running == True:
    user_input = get_input_non_blocking()
    if user_input == "esc":
        break
    elif user_input == "-":
        torque -= 1
    elif horsepower > 50:
        os.system('clear')
        print(horsepower)
        time.sleep(1)
        running = True
    else:
        running = False
