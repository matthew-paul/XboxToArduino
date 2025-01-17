import serial

from PythonCode.arduinoUtil import arduino_port

arduinoPort = arduino_port()
print(f'Name: {arduinoPort.name}')

ser = serial.Serial()
ser.baudrate = 115200
ser.port = arduinoPort.device
ser.open()

ser.write('F10'.encode())

print(f'opened Arduino port: {ser.port}')

ser.close()