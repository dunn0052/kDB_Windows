# THIS FILE WAS GENERATED. DO NOT MODIFY!

class DCC_CHAR:

    FORMAT = "24s24sBBBBBBBBBBBBBB3I8I198sI"

    def __init__(self, data:tuple):
        if len(data) != 29:
            return None
        
        self.NAME = str(data[0], encoding='UTF-8').rstrip('\00')
        self.OCCUPATION = str(data[1], encoding='UTF-8').rstrip('\00')
        self.ALIGNMENT = data[2]
        self.ARMOR_CLASS = data[3]
        self.HIT_POINTS = data[4]
        self.REFLEX = data[5]
        self.FORTITUDE = data[6]
        self.WILL = data[7]
        self.STRENGTH = data[8]
        self.AGILITY = data[9]
        self.STAMINA = data[10]
        self.PERSONALITY = data[11]
        self.INTELLIGENCE = data[12]
        self.LUCK = data[13]
        self.SPEED = data[14]
        self.INITIATIVE = data[15]
        self.WEAPONS = data[16:18]
        self.EQUIPMENT = data[19:26]
        self.NOTES = str(data[27], encoding='UTF-8').rstrip('\00')
        self.XP = data[28]


    def __str__(self) -> str:
        return f"NAME: {self.NAME} OCCUPATION: {self.OCCUPATION} ALIGNMENT: {self.ALIGNMENT} ARMOR_CLASS: {self.ARMOR_CLASS} HIT_POINTS: {self.HIT_POINTS} REFLEX: {self.REFLEX} FORTITUDE: {self.FORTITUDE} WILL: {self.WILL} STRENGTH: {self.STRENGTH} AGILITY: {self.AGILITY} STAMINA: {self.STAMINA} PERSONALITY: {self.PERSONALITY} INTELLIGENCE: {self.INTELLIGENCE} LUCK: {self.LUCK} SPEED: {self.SPEED} INITIATIVE: {self.INITIATIVE} WEAPONS: {self.WEAPONS} EQUIPMENT: {self.EQUIPMENT} NOTES: {self.NOTES} XP: {self.XP} "