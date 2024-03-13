import pyvisa
import numpy
import time

class Source:  
    def __init__(self, instrument, name=None):
        self.instrument = instrument
        self.name = name  # Nombre para identificar en depuracion
        self.modo = "2W"
        self.id = ""
        self.type = ""
            
        instrument.write("*IDN?")
        time.sleep(0.05)
        self.id = instrument.read()
        print("ID: {}".format(self.id))

        if "DP711" in self.id:
            self.type = "DP711"
        elif "DP811" in self.id:
            self.type = "DP811"

    # turn on channel
    def turn_on_channel(self, channel: int):
        if self.type == "DP811":
            self.instrument.write(":OUTPUT CH{:n},ON".format(channel))
            return self.instrument.query(":OUTP? CH{}".format(channel))
        elif self.type == "DP711":
            self.instrument.write(":OUTP:STAT CH{:n},ON".format(channel))
            return self.instrument.query(":OUTP:STAT? CH{}".format(channel))
        else:
            print("Command or instrument not supported:", self.type, "Turn on channel")

    # turn off channel
    def turn_off_channel(self, channel: int):
        if self.type == "DP811":
            self.instrument.write(":OUTPUT CH{:n},OFF".format(channel))
            return self.instrument.query(":OUTP? CH{}".format(channel))
        elif self.type == "DP711":
            self.instrument.write(":OUTP:STAT CH{:n},OFF".format(channel))
            return self.instrument.query(":OUTP:STAT? CH{}".format(channel))
        else:
            print("Command or instrument not supported:", self.type, "Turn off channel")

    # apply voltage & current
    def apply_voltage_current(self, channel: int, voltage: float, current: float):
        if self.type == "DP811" or self.type == "DP711":
            self.instrument.write(":APPL CH{},{},{}".format(channel, voltage, current))
            return self.instrument.query(":APPL? CH{}".format(channel))
        else:
            print("Command or instrument not supported:", self.type, "Apply voltage, current")

    # measure everything (in order returns: voltage, current and power)
    def measure_all(self, channel: int):
        if self.type == "DP811" or self.type == "DP711":
            measurement = self.instrument.query(":MEASURE:ALL?").split(",")
            measurement[-1] = measurement[-1][:-1]
            voltage = measurement[0]
            current = measurement[1]
            potencia = measurement[2]
            return float(voltage), float(current), float(potencia)
        else:
            print("Command or instrument not supported:", self.type, "Measure all")

    def sensing_mode(self, sensing = False):
        if self.type == "DP811":
            if sensing == False:
                self.modo = "2W"
                self.instrument.write("OUTP:SENS CH1, OFF")
                return self.instrument.query("OUTP:SENS? CH1")
            elif sensing == True:
                self.modo = "4W"
                self.instrument.write("OUTP:SENS CH1, ON")
                return self.instrument.query("OUTP:SENS? CH1")
        else:
            print("Command or instrument not supported:", self.type, "Set sensing mode")


# functions for the electronic load
class Load:
    def __init__(self, instrument, name=None):
        self.load = instrument
        self.name = name  # Nombre para identificar en depuracion

    # set function : RES, CURR, VOLT, POW
    def set_function(self, funcion: str):
        self.load.write(":SOUR:FUNC {}".format(funcion))
        return self.load.query(":SOUR:FUNC?")

    # turn on load
    def turn_on_load(self):
        self.load.write(":SOUR:INP:STAT 1")
        return self.load.query(":SOUR:INP:STAT?")

    # turn off load
    def turn_off_load(self):
        self.load.write(":SOUR:INP:STAT 0")
        return self.load.query(":SOUR:INP:STAT?")

    # set current only if you are on CC
    def set_current(self, current: float):
        self.load.write(":SOUR:CURR:LEV:IMM {}".format(current))
        return self.load.query(":SOUR:CURR:LEV:IMM?")

    # set voltage only if you are on CV
    def set_voltage(self, voltage: float):
        self.load.write(":SOUR:VOLT:LEV:IMM {}".format(voltage))
        return self.load.query(":SOUR:VOLT:LEV:IMM?")

    # set resistance only if you are on CR
    def set_resistance(self, resistance: float):
        self.load.write(":SOUR:RES:LEV:IMM {}".format(resistance))
        return self.load.query(":SOUR:RES:LEV:IMM?")

    # set resistance only if you are on CP (need to verify function)
    def set_power(self, power: float):
        self.load.write(":SOUR:POW:LEV:IMM {}".format(power))
        return self.load.query(":SOUR:POW:LEV:IMM?")
        
    # Set range to be 4 A (low range) or 40 A (high range)
    def set_range(self, current: int):
        self.load.write(":SOUR:CURR:RANG {}".format(current))
        return self.load.query("SOUR:CURR:RANG?")
        
    # Changes the load mode to CV
    def set_mode(self, mode: str):
        self.load.write(":SOUR:FUNC {}".format(mode))
        return self.load.query(":SOUR:FUNC?")
    
    # Set sensor terminals    
    def remote_sense(self,state):
        if state:
            self.load.write("SENS ON")
        else:
            self.load.write("SENS OFF")

    # Measure CURR
    def measure_current(self):
        return float(self.load.query("MEAS:CURR:DC?"))
        
    # Measure VOLT
    def measure_voltage(self):
        return float(self.load.query("MEAS:VOLT:DC?"))
        
        # measure everything (in order returns: voltage, current and power)
    def measure_all(self):
        voltage = self.measure_voltage()
        current = self.measure_current()
        return voltage, current


        
        
