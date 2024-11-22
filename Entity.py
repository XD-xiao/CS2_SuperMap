class Entity:
    id = None
    image_id = None
    address = None
    hp = None
    teamFlag = None
    posX = None
    posY = None
    viewAngles = None
    # csMemory = CSMemory()

    def __init__(self, id, address,csMemory):
        self.id = id
        self.address = address
        self.update(csMemory)

    def update(self,csMemory):
        self.teamFlag = csMemory.getTeamFlag(self.address)
        self.hp = csMemory.getHealth( self.address)
        self.posX, self.posY = csMemory.getPosition(self.address)
        self.viewAngles = csMemory.getViewAngles(self.address)

    def getTeamFlag(self):
        return self.teamFlag

    def getHealth(self):
        return self.hp

    def getPosition(self):
        return self.posX, self.posY

    def getViewAngles(self):
        return self.viewAngles
