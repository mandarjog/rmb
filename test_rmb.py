import rmb
import serial.tools.list_ports


def test_script():
    comp = serial.tools.list_ports.comports()
    ll = [l for l in comp if "UART" in l[1] or "UART" in l[2]]
    if len(ll) > 0:
        dev = ll[0][0]
        print "Found ", dev
    else:
        print "No suitable serial port available"
        return -1

    rm = rmb.Roomba(dev, verbose=True)
    cmds = [
        "sensors",
        "play,1",
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
        "drive,-20,-100",
        "sensors,1",
        "sensors,2",
        "drive_stop",
        "play,1",
    ]
    rm.exec_script(cmds, pause_time=2.4)
