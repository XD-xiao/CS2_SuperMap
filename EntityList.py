import time

from CSMemory import CSMemory
from Entity import Entity


class EntityList:
    list = []

    csMemory = None

    def registerEntity(self):
        self.csMemory = CSMemory()
        for id in range(1, 998):
            entityAddress = self.csMemory.get_entityByid(id)
            try:
                if entityAddress and 0 < self.csMemory.getHealth(entityAddress) <= 100:
                    self.list.append(Entity(id, entityAddress, self.csMemory))
            except Exception as e:
                print(f"Error processing entity with ID {id}: {e}")

    def updateList(self):
        for entity in self.list:
            try:
                entity.update(self.csMemory)
                time.sleep(0.02)
            except Exception as e:
                print(f"Error updating entity at address {entity.address}: {e}")
                continue

    def showList(self):
        try:
            for entity in self.list:
                try:
                    print(entity.address, entity.getTeamFlag(), entity.getHealth(), entity.getPosition(),
                          entity.getViewAngles())
                    self.updateList()
                    time.sleep(0.05)
                except Exception as e:
                    print(f"Error showing entity at address {entity.address}: {e}")
                    continue
            print("-------------------------------------------------------")
        except KeyboardInterrupt:
            print("Exiting...")

    def clearList(self):
        self.list.clear()


if __name__ == "__main__":
    entityList = EntityList()
    entityList.registerEntity()
    while True:
        entityList.showList()
        time.sleep(0.5)
