from machine import ADC
from adc_sub import ADC_substitute

pin_battery = 34  # The battery measurement input pin (ADC1_6)

# Battery
battery = ADC_substitute(pin_battery)  # Replace with ADC(pin_battery) if using the built-in ADC

# Calibration values
ip1 = 1450  # Measured value when the battery is fully discharged
ip2 = 2400  # Measured value when the battery is fully charged
bp1 = 10     # Battery percentage when fully discharged
bp2 = 100   # Battery percentage when fully charged

# Calculate the slope and intercept for linear interpolation
alpha = (bp2 - bp1) / (ip2 - ip1)
beta = bp1 - alpha * ip1

def get_battery_percentage():
    ip = battery.read_adc()  # Replace with battery.read_voltage() if using the built-in ADC
    # Uncomment the line below for debugging or calibration
    # print("Raw ADC Reading:", ip)

    # Calculate the battery percentage based on the measured input value
    bp = alpha * ip + beta
    bp = int(max(0, min(bp, 100)))  # Ensure the value is within the valid range

    return bp

# Example of using the battery percentage
battery_percentage = get_battery_percentage()
print("Battery Percentage:", battery_percentage)