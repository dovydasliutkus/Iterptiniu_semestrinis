import serial

def stm_init(portsel,baudratesel):
    global stm
    stm = serial.Serial(
        port=portsel,
        baudrate=baudratesel,
        timeout=0,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE
        )

def stm_readline():
    data = stm.read(100)
    data = data.decode('utf8')
    return data

def stm_writeline(command):
    if stm.is_open == True:
        stm.write(command.encode())
    else:
        stm.open()
        stm.write(command.encode())
        
