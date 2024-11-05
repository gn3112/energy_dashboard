from app.config.config import Config

config = Config()

def convert_unit(value):
    conversion_factors = [1, 10**3, 10**6, 10**9]

    # Calculate the conversion factor
    conversion_factor = conversion_factors[config.MEASUREMENT_ORDER_UNIT] / conversion_factors[config.DISPLAY_ORDER_UNIT]

    # Convert the measurement value
    display_value = value * conversion_factor

    return display_value