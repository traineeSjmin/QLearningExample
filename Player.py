class Player:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def GetPosition(self):
        return self.position
    
    def MovePlayer(self, dx, dy):
        nx = self.position[0] + dx
        ny = self.position[1] + dy
        self.SetPosition(nx, ny)
    
    def SetPosition(self, x, y):
        self.position = [x,y]