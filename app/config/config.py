class Config():
    TIMEZONE = "Europe/Amsterdam"
    MEASUREMENT_ORDER_UNIT = 0 # 0: for base order (W for instance), 1: for kilo (kW), 2: for mega (MW)
    DISPLAY_ORDER_UNIT =  0 # Default is kilo

    if DISPLAY_ORDER_UNIT == 0:
        DISPLAY_UNIT = ""
    elif DISPLAY_ORDER_UNIT == 1:
        DISPLAY_UNIT = "k"
    elif DISPLAY_ORDER_UNIT == 2:
        DISPLAY_UNIT = "M"
    elif DISPLAY_ORDER_UNIT == 3:
        DISPLAY_UNIT = "G"
    
    KWH_PRICE = 0.001

    ACTIVE_POWER_SENSORS = [324, 325, 326] # Corresponds to sensor ids (same as in assets/sensors_list.txt)
    APPARENT_POWER_SENSORS = [327, 328, 329]