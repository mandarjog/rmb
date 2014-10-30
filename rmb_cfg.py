from collections import namedtuple

# sensor data and format per SCI doc
SCONFIG = {
    3: {"class": namedtuple("s3", "charging_state,voltage,"
                                  "current,temperature,charge,capacity"),
        "fmt": "!BHhbHH"},
    2: {"class": namedtuple("s2", "remote_control_command,buttons,"
                                  "distance,angle"),
        "fmt": "!BBhh"},
    1: {"class": namedtuple("s1", "bumps_wheeldrops,wall,cliff_left,"
                                  "cliff_front_left,cliff_front_right,"
                                  "cliff_right,virtual_wall,motor_overcurrents,"
                                  "dirt_detector_left,dirt_detector_right"),
        "fmt": "!BBBBBBBBBB"}
}


OPCODE = {
    "start": 128,
    "safe": 131,
    "full": 132,
    "power": 133,
    "spot": 134,
    "clean": 135,
    "max": 136,
    "drive": 137,
    "motors": 138,
    "leds": 139,
    "song": 140,
    "play": 141,
    "sensors": 142
}

RADIUS = {
    "turn":
    {"clockwise": -1,
     "counterclockwise": 1},
    "straight": 32768,
    "max": 2000
}
