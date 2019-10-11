import sys


def serial_ports():
    # pregunta si el sistema es windows
    if sys.platform.startswith('win'):
        # puertos de Windows
        ports = ['COM%s' % (i + 1) for i in range(256)]
        # pregunta si el sistema operativo es linux
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # puertos de linux
        ports = glob.glob('/dev/tty[A-Za-z]*')
        # pregunta si el sistema operativo es mac
    elif sys.platform.startswith('darwin'):
        # puertos de mac
        ports = glob.glob('/dev/tty.*')
        # puertos de mac
    else:
        raise EnvironmentError('Unsupported platform')
        # crea un vector para almacenar los puertos
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    return ports


