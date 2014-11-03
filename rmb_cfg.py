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


NOTES = {
    "c": 60,
    "c#": 61,
    "d": 62,
    "d#": 63,
    "e": 64,
    "f": 65,
    "f#": 66,
    "g": 67,
    "g#": 68,
    "a": 69,
    "a#": 70,
    "b": 72,
}
song_pirates = [45, 32, 48, 32, 50, 32, 50, 32, 50, 16,
                52, 64, 53, 32, 53, 32, 53, 16, 55, 32, 52, 32, 52, 32]

song_happy_birthday = (
    "c,0.5,c,0.5,d,c,f,e,1.5,c,0.5,c,0.5,d,c,g,f,1.5"
    "c,0.5,c,0.5,+c,a,f,e,d,a#,0.5,a#,0.5,a,f,g,f",
)
