from pymodbus.client.sync import ModbusTcpClient as ModbusClient
class modbus :

    def __init__(self,ip='localhost',port=502):
        self.UNIT = 0x1
        self.client = ModbusClient(ip, port)
    
    def connect(self):
        self.client.connect()
    
    def close(self):
        self.client.close()

    def write_bit(self,address,bit):
        self.client.write_coil(address, bit, unit=self.UNIT)
        while self.client.read_coils(address, 1, unit=self.UNIT).bits[0] != bit:
            self.client.write_coil(address, bit, unit=self.UNIT)

    def write_word(self,address,word):
        self.client.write_register(address, word, unit=self.UNIT)
        while self.client.read_holding_registers(address, 1, unit=self.UNIT).registers[0]!=word:
            self.client.write_register(address, word, unit=self.UNIT)

    def read_bit(self,address):
        return self.client.read_coils(address, 1, unit=self.UNIT).bits[0]

    def read_word(self,address):
        return self.client.read_holding_registers(address, 1, unit=self.UNIT).registers[0]

    def read_input(self,address):
        return self.client.read_discrete_inputs(address, 1, unit=self.UNIT).bits[0]


    # def read_coil(self,address,count):
    #     rr = self.client.read_coils(address, count, unit=self.UNIT)
    #     assert(not rr.isError())     # test that we are not an error

    # def write_coil(self,address,value):
    #     rq = self.client.write_coil(address, value, unit=self.UNIT)
    #     assert(not rq.isError())     # test that we are not an error

    # def write_read_coil(self,address,value,count):
    #     rq = self.client.write_coils(address, value*count, unit=self.UNIT)
    #     rr = self.client.read_coils(address, count, unit=self.UNIT)
    #     assert(not rq.isError())     # test that we are not an error
    #     assert(not rr.isError())     # test that we are not an error   

    # def write_read_coils(self,address,value,count):
    #     rq = self.client.write_coils(address, value*count, unit=self.UNIT)
    #     rr = self.client.read_coils(address, count, unit=self.UNIT)
    #     # print(rr.bits[0])
    #     assert(not rq.isError())     # test that we are not an error
    #     assert(not rr.isError())     # test that we are not an error

    # def read_input(self,address,count):
    #     rr = self.client.read_discrete_inputs(address, count, unit=self.UNIT)
    #     assert(not rr.isError())     # test that we are not an error

    # def write_read_input(self,address,value,count):
    #     rq = self.client.write_register(address, value, unit=self.UNIT)
    #     rr = self.client.read_holding_registers(address, count, unit=self.UNIT)
    #     assert(not rq.isError())     # test that we are not an error
    #     assert(not rr.isError())     # test that we are not an error

    # def write_read_inputs(self,address,value,count):
    #     rq = self.client.write_registers(address, value*count, unit=self.UNIT)
    #     rr = self.client.read_holding_registers(address, count, unit=self.UNIT)
    #     # print(rr.registers[0])
    #     assert(not rq.isError())     # test that we are not an error
    #     assert(not rr.isError())     # test that we are not an error

    # def read_inputs(self,address,count):
    #     rr = self.client.read_input_registers(address, count, unit=self.UNIT)
    #     assert(not rr.isError())     # test that we are not an error

    # def write_read_sim_inputs(self,address,value,count):
    #     arguments = {
    #         'read_address':    address,
    #         'read_count':      count,
    #         'write_address':   address,
    #         'write_registers': value*count,
    #     }
    #     rq = self.client.readwrite_registers(unit=self.UNIT, **arguments)
    #     rr = self.client.read_holding_registers(address, count, unit=self.UNIT)
    #     assert(not rq.isError())     # test that we are not an error
    #     assert(not rr.isError())     # test that we are not an error