# THIS FILE WAS GENERATED. DO NOT MODIFY!

class GURPS_CHAR:

    FORMAT = "24sIIIIIIIII"

    def __init__(self, NAME:str, ST:int, DX:int, IQ:int, HT:int, HP:int, WILL:int, PER:int, SPD:int, MOV:int):
        self.NAME = NAME
        self.ST = ST
        self.DX = DX
        self.IQ = IQ
        self.HT = HT
        self.HP = HP
        self.WILL = WILL
        self.PER = PER
        self.SPD = SPD
        self.MOV = MOV


    def __str__(self) -> str:
        return f"NAME: {self.NAME} ST: {self.ST} DX: {self.DX} IQ: {self.IQ} HT: {self.HT} HP: {self.HP} WILL: {self.WILL} PER: {self.PER} SPD: {self.SPD} MOV: {self.MOV} "