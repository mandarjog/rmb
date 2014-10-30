import rmb


def test_script():
    rm = rmb.Roomba("/dev/ttyUSB0", verbose=True)
    cmds = [
        "sensors",
        "play",
        "sensors,1",
        "sensors,2",
        "sensors,2",
        "drive_straight,20",
        "sensors,2",
        "drive_stop",
        "sensors,1",
        "sensors,2",
        "drive_straight,-20",
        "sensors,2",
        "sensors,2",
        "sensors,2",
        "drive_stop",
        "drive,20,-50",
        "sensors,2",
        "sensors,2",
        "sensors,1",
        "sensors,2",
        "drive_stop",
    ]
    rm.exec_script(cmds)
