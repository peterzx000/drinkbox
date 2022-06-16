import modbus.modbus_tcp_client as modbus_tcp_client
import time
client = modbus_tcp_client.modbus('172.31.1.87',502)
# client = modbus_tcp_client.modbus('192.168.125.5',502)
client.connect()
count = 0
while True:
    count += 1
    try:
        # case = input('case\n') 
        case = 8
    except:
        print('case fail')
        continue
    client.write_word(37,int(case))
    if int(case)==6:
        try:
            location = [round(float(i),2) for i in input('location\n').split()]
            location2 = [round(float(i),2) for i in input('location2\n').split()]
        except:
            print('location fail')
            continue
        for i in range(len(location)):
            j = location[i]
            if j<0:
                client.write_bit(20+i,1)
                location[i] = j*(-1)
            else:
                client.write_bit(20+i,0)
            client.write_word(25+i*2,j*100/100)
            client.write_word(25+i*2+1,j*100%100)
        for i in range(len(location2)):
            j = location2[i]
            if j<0:
                client.write_bit(11+i,1)
                location2[i] = j*(-1)
            else:
                client.write_bit(11+i,0)
            client.write_word(39+i*2,j*100/100)
            client.write_word(39+i*2+1,j*100%100)
    elif int(case)==1:
        print('home')
    elif int(case)==8:
        # client.write_word(6,100)
        client.write_word(8,200)
        client.write_bit(6,1)
    else:
        try:
            location = [round(float(i),2) for i in input('location\n').split()]
        except:
            print('location fail')
            continue
        for i in range(len(location)):
            j = location[i]
            if j<0:
                client.write_bit(20+i,1)
                j = j*(-1)
                location[i] = j
            else:
                client.write_bit(20+i,0)
            client.write_word(25+i*2,int(int(j*100)/100))
            client.write_word(25+i*2+1,int(j*100)%100)
    time.sleep(0.5)
    client.write_bit(4,1)
    time.sleep(0.1)
    client.write_bit(4,0)
    time.sleep(1)
    print(time.time())
    print(count)
    # while client.read_input(0)==True:
    #     time.sleep(1)