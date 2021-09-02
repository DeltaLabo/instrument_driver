import pyvisa
import numpy
import time


# functions for power supply
class Fuente:  # Esta clase describe cada neurona
    def __init__(self, instrument, name=None):
        self.instrument = instrument
        self.name = name  # Nombre para identificar en depuracion
        self.delay_enable = False
        self.modo = "2W"

        instrument.write("*IDN?")
        time.sleep(0.02)
        id = instrument.read()

        if "SPD1305X" in id:
            instrument.write_termination = '\n'
            instrument.read_termination = '\n'
            self.delay_enable = True

    # turn on channel
    def encender_canal(self, channel: int):
        if self.delay_enable:
            self.instrument.write("OUTP CH{:n},ON".format(channel))
            time.sleep(0.02)
            return "ON"
        else:
            self.instrument.write(":OUTPUT CH{:n},ON".format(channel))
            return self.instrument.query(":OUTP? CH{}".format(channel))

    # turn off channel
    def apagar_canal(self, channel: int):
        if self.delay_enable:
            self.instrument.write("OUTP CH{:n},OFF".format(channel))
            time.sleep(0.02)
            return "OFF"
        self.instrument.write(":OUTPUT CH{:n},OFF".format(channel))
        return self.instrument.query(":OUTP? CH{}".format(channel))

    # apply voltage & current
    def aplicar_voltaje_corriente(self, channel: int, voltaje: float, corriente: float):
        if self.delay_enable:
            self.instrument.write("CH{}:VOLT {}".format(channel, voltaje))
            time.sleep(0.02)
            self.instrument.write("CH{}:CURR {}".format(channel, corriente))
            time.sleep(0.02)
            self.instrument.write("CH{}:VOLT?".format(channel))
            time.sleep(0.02)
            voltMeas = self.instrument.read()
            time.sleep(0.02)
            self.instrument.write("CH{}:CURR?".format(channel))
            time.sleep(0.02)
            currMeas = self.instrument.read()
            time.sleep(0.02)
            return "CH1:30V/5A," + voltMeas + "," + currMeas
        else:
            self.instrument.write(":APPLY CH{},{},{}".format(channel, voltaje, corriente))
            return self.instrument.query("APPLY? CH{}".format(channel))

    # measure everything (in order returns: voltage, current and power)
    def medir_todo(self, channel: int):
        if self.delay_enable:
            self.instrument.write("MEAS:VOLT? CH1")
            time.sleep(0.02)
            voltaje = float(self.instrument.read())
            time.sleep(0.02)
            self.instrument.write("MEAS:CURR? CH1")
            time.sleep(0.02)
            corriente = float(self.instrument.read())
            time.sleep(0.02)
            self.instrument.write("MEAS:POWE? CH1")
            time.sleep(0.02)
            potencia = float(self.instrument.read())
            time.sleep(0.02)
            return voltaje, corriente, potencia
        else:
            medicion = self.instrument.query(":MEASURE:ALL?").split(",")
            medicion[-1] = medicion[-1][:-1]
            voltaje = medicion[0]
            corriente = medicion[1]
            potencia = medicion[2]
            return float(voltaje), float(corriente), float(potencia)

    def toggle_4w(self):
        if self.delay_enable:
            if self.modo == "2W":
                self.modo = "4W"
                self.instrument.write("MODE:SET {}".format(self.modo))
                time.sleep(0.5)
                return "4W"
            elif self.modo == "4W":
                self.modo = "2W"
                self.instrument.write("MODE:SET {}".format(self.modo))
                time.sleep(0.5)
                return "2W"


# functions for the electronic load
class Carga:  # Esta clase describe cada neurona
    def __init__(self, instrument, name=None):
        self.carga = instrument
        self.name = name  # Nombre para identificar en depuracion

    # set function : RES, CURR, VOLT, POW
    def fijar_funcion(self, funcion: str):
        self.carga.write(":SOUR:FUNC {}".format(funcion))
        return self.carga.query(":SOUR:FUNC?")

    # turn on load
    def encender_carga(self):
        self.carga.write(":SOUR:INP:STAT 1")
        return self.carga.query(":SOUR:INP:STAT?")

    # turn off load
    def apagar_carga(self):
        self.carga.write(":SOUR:INP:STAT 0")
        return self.carga.query(":SOUR:INP:STAT?")

    # set current only if you are on CC
    def fijar_corriente(self, corriente: float):
        self.carga.write(":SOUR:CURR:LEV:IMM {}".format(corriente))
        return self.carga.query(":SOUR:CURR:LEV:IMM?")

    # set voltage only if you are on CV
    def fijar_voltaje(self, voltaje: float):
        self.carga.write(":SOUR:VOLT:LEV:IMM {}".format(voltaje))
        return self.carga.query(":SOUR:VOLT:LEV:IMM?")

    # set resistance only if you are on CR
    def fijar_resistencia(self, resistencia: float):
        self.carga.write(":SOUR:RES:LEV:IMM {}".format(resistencia))
        return self.carga.query(":SOUR:RES:LEV:IMM?")

    # set resistance only if you are on CP (need to verify function)
    def fijar_potencia(self, resistencia: float):
        self.carga.write(":SOUR:POW:LEV:IMM {}".format(resistencia))
        return self.carga.query(":SOUR:POW:LEV:IMM?")
