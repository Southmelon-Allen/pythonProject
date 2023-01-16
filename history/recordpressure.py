
import time
import serial
ser = serial.Serial('/dev/cu.usbmodem1101',9600, timeout=2)
filename= "shuju2.csv"
data = ''
print("start serial")
f = open(filename, 'a')
f.writelines("Time, Temperature-C, Pressure-Pa, Altitude-m,"+"\n")
f.close()

while True:
    data = ser.readline()
    t = time.localtime()
    ct=time.strftime("%Y-%m-%d %H:%M:%S", t)

    print(ct)
    print(data)
    f = open(filename, 'a')
    s=ct+","+data.decode('utf-8')+","+"\n"
    f.writelines(s)
    #f.writelines(':\n')
    #f.writelines(data.decode('utf-8'))
    f.close()
