from random import randint

def generateUID() -> str:
    return "".join([chr(randint(0x20, 0x7E)) for i in range(16)])