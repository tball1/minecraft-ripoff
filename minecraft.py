from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
land = []

def saveWorld(filename="myworld.world"):
    print("Saving..")
    s = ""
    try:
        open(filename,"a+").close()
    except:
        print("File permissions error!")
        return

    for block in land:
        x,y,z = block.x,block.y,block.z
        idname = block.idname
        s = s + str(x) + " " + str(y) + " " + str(z) +" " + str(idname) +"\n"

    with open(filename,"w+") as file:
        file.write(s)
        file.flush()

    print("Done?")

def loadWorld(filename="myworld.world"):
    with open(filename,"r+") as file:
        content = file.read()
        lines = content.split("\n")
        for line in lines:
            if line == "":
                continue
            data = line.split(" ")

            x,y,z = data[0],data[1],data[2]
            x = float(x)
            y = float(y)
            z = float(z)
            name = data[3]
            name = name.replace("\n","")

            if name == "Grass":
                grass = Grass()
                grass.position = (x,y,z)
                land.append(grass)
                    
            if name == "Stone":
                stone = Stone()
                stone.position = (x,y,z)
                land.append(stone)
                
            if name == "Bedrock":
                bedrock = Bedrock()
                bedrock.position = (x,y,z)
                land.append(bedrock)

    file.close()




class Player(FirstPersonController):
    def __init__(self):
        super().__init__()

        self.gravity = 1
        self .y = 10
        self.flying = False
        self.flyspeed = 5
        self.selected = 0
        self.select_max = 3


    def update(self):
        super().update()

        if held_keys["space"] and self.flying:
            self.y = self.y + 1 * time.dt * self.flyspeed
        if held_keys["shift"] and self.flying:
            self.y = self.y - 1 * time.dt * self.flyspeed

        if held_keys["space"] and self.flying == False:
            self.y = 2 #I dont know a better way of doing it haha

    def input(self,key):
        if key == "=":
            self.selected = self.selected + 1
            if self.selected >= self.select_max or 0 > self.selected:
                self.selected = 0


        if key == "-":
            self.selected = self.selected - 1
            if self.selected >= self.select_max or 0 > self.selected:
                self.selected = 0
            

        if key == "f":
            self.flying = not self.flying
            if self.flying:
                self.gravity = 0
            else:
                self.gravity = 1

        if key == "/":
            for block in land:
                if block.breakable:
                    block.remove_node()

        if key == ";":
            saveWorld()
        
        if key == "l":

            for block in land:
                block.remove_node()
            #otherwise the world may not load in correctly
            loadWorld()

            

creds = Text(text="Crappy minecraft ripoff",y=.5,x=-.85,color=color.black)
player = Player()

#Our base Block class
class Block(Button):
    def __init__(self):
        super().__init__()
        self.model = "cube"
        self.parent = scene
        self.scale = 1
        self.color = color.yellow
        self.texture = "white_cube"
        self.breakable = True
        self.level = 0

    def input(self,key):
        global newblock

        if self.hovered and key == "right mouse down":
            if player.selected == 0:
                newblock = Grass()
            elif player.selected == 1:
                newblock = Stone()
            elif player.selected == 2:
                newblock = Sand()

            land.append(newblock)
            newblock.position = self.position + mouse.normal

            print(str(newblock.position))

        if self.hovered and key == "left mouse down":
            if self.breakable:
                self.remove_node()

        if self.hovered and key == "enter":
            self.breakable = not self.breakable


    def detectlevel(self):
        return
        if self.level == 0:
            self.color = color.black
        else:
            self.color = color.green


#Blocks
class Grass(Block):
    def __init__(self):
        super().__init__()
        self.idname = "Grass"
        self.color = color.green

        #Add free to use texture

class Stone(Block):
    def __init__(self):
        super().__init__()
        self.idname = "Stone"
        self.color = color.gray

        #Add free to use texture

class Bedrock(Block):
    def __init__(self):
        super().__init__()
        self.color = color.black
        self.idname = "Bedrock"
        self.breakable = False

        #Add free to use texture

class Sand(Block):
    def __init__(self):
        super().__init__()
        self.color = color.yellow

        #Add physics here & free to use texture



b = Bedrock()
b.position = (0,0,0)
land.append(b)

Sky()
app.run()