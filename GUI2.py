import tkinter as tk
import paho.mqtt.client as mqtt
from threading import Thread

class Player:
    def __init__(self, type, playerID, spawnX, spawnY):
        self.playerIDObject = None
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.score = 0
        self.canvas = None
        self.client = None
        self.file = None
        self.object = None
        self.type = type
        self.playerID = playerID
        self.topic = "game/"+ type + str(playerID) + "_C"

    def InitializeObject(self, canvas):
        self.canvas = canvas
        if (self.type == "corona"):
            self.file = tk.PhotoImage(file = "bigCResized.png")
        elif (self.type == "toiletPaper"):
            self.file = tk.PhotoImage(file = "tpResized.png")
        elif (self.type == "shoppingCart"):
            self.file = tk.PhotoImage(file = "cartResized.png")
        self.playerIDObject = self.canvas.create_text(self.spawnX,self.spawnY, text=(str(self.playerID)), font=("Courir", 15))
        self.object = self.canvas.create_image(self.spawnX,self.spawnY, anchor = tk.NW, image = self.file)

    def MQTT(self):
        self.client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            client.subscribe(self.topic)
            print(self.type + " " + str(self.playerID) + " subcribed to " + self.topic)

        def on_message(client, userdata, msg):
            message = msg.payload.decode()
            self.Move(message)

        self.client.connect("81.165.114.134", 1883, 60)

        self.client.on_connect = on_connect
        self.client.on_message = on_message

        self.client.loop_forever()

    def Move(self, moveDir):
        global score
        global scoreObject
        if moveDir == "right":
            self.canvas.move(self.object, TPMoveSpeedX, 0)
            self.canvas.move(self.playerIDObject, TPMoveSpeedX, 0)
            print(self.type + str(self.playerID) + " moved right!")
        elif moveDir == "left":
            self.canvas.move(self.object, -TPMoveSpeedX, 0)
            self.canvas.move(self.playerIDObject, -TPMoveSpeedX, 0)
            print(self.type + str(self.playerID) + " moved left!")
        elif moveDir == "up":
            self.canvas.move(self.object, 0, -TPMoveSpeedY)
            self.canvas.move(self.playerIDObject, 0, -TPMoveSpeedY)
            print(self.type + str(self.playerID) + " moved up!")
        elif moveDir == "down":
            self.canvas.move(self.object, 0, TPMoveSpeedY)
            self.canvas.move(self.playerIDObject, 0, TPMoveSpeedY)
            print(self.type + str(self.playerID) + " moved down!")
        elif moveDir == "DIE":
            self.canvas.coords(self.object, self.spawnX, self.spawnY)
            self.canvas.coords(self.playerIDObject, self.spawnX, self.spawnY)
            print(self.type + str(self.playerID) + " died and respawned at x: " + str(self.spawnX) + " and y: " + str(self.spawnY))
        elif moveDir == "POINT":
            self.canvas.coords(self.object, self.spawnX, self.spawnY)
            self.canvas.coords(self.playerIDObject, self.spawnX, self.spawnY)
            score += 1
            self.canvas.itemconfig(scoreObject, text=("Score", score))
            print(self.type + str(self.playerID) + " collected a point and respawned at x: " + str(self.spawnX) + " and y: " + str(self.spawnY))



players = [Player("toiletPaper", 0, 0, 242),Player("toiletPaper", 1, 0, 484) , Player("shoppingCart", 0, 960, 462), Player("corona", 0, 1800, 396)]

TPMoveSpeedX, TPMoveSpeedY = 20, 20

score = 0
scoreObject = None

def GUI():
    window = tk.Tk()
    canvas = tk.Canvas(window, width = 1920, height = 950)
    canvas.pack()

    global score
    global scoreObject
    scoreObject = canvas.create_text(150,50, text=("Score", score), font=("Courir", 40))

    for player in players:
        player.InitializeObject(canvas)

    window.mainloop()


jobGUI = Thread(target = GUI)
jobGUI.start()

for player in players:
    job = Thread(target = player.MQTT)
    job.start()
