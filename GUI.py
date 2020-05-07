import tkinter as tk
import paho.mqtt.client as mqtt
from threading import Thread

TPMoveSpeedX, TPMoveSpeedY = 100, 100
topic = "TeamOpdracht/1"

playerTP, playerTP2, playerCart, playerBIGC = 1,2,3,4

playerNumber = 0
messageReceived = False
moveDir = " "

def GUI():
  window = tk.Tk()
  canvas = tk.Canvas(window, width = 1800, height = 950)
  canvas.pack()

  tpFile = tk.PhotoImage(file = "tpResized.png")
  playerTPObject = canvas.create_image(50,50, anchor = tk.NW, image = tpFile)
  playerTPObject2 = canvas.create_image(50,300, anchor = tk.NW, image = tpFile)

  cartFile = tk.PhotoImage(file = "cartResized.png")
  playerCartObject = canvas.create_image(300,175, anchor = tk.NW, image = cartFile)

  bigCFile = tk.PhotoImage(file = "bigCResized.png")
  playerBigCObject = canvas.create_image(700,175, anchor = tk.NW, image = bigCFile)

  def MoveObject():
    global messageReceived
    if messageReceived:
      global playerNumber
      if playerNumber == playerTP:
        objectToMove = playerTPObject
      elif playerNumber == playerTP2:
        objectToMove = playerTPObject2
      elif playerNumber == playerCart:
        objectToMove = playerCartObject
      elif playerNumber == playerBIGC:
        objectToMove = playerBigCObject
      else:
        objectToMove = None

      if objectToMove != None:
        global moveDir
        if moveDir == "RIGHT":
          canvas.move(objectToMove, TPMoveSpeedX, 0)
          print("Player " + str(playerNumber) + " moved right!")
        elif moveDir == "LEFT":
          canvas.move(objectToMove, -TPMoveSpeedX, 0)
          print("Player " + str(playerNumber) + " moved left!")
        elif moveDir == "UP":
          canvas.move(objectToMove, 0, -TPMoveSpeedY)
          print("Player " + str(playerNumber) + " moved up!")
        elif moveDir == "DOWN":
          canvas.move(objectToMove, 0, TPMoveSpeedY)
          print("Player " + str(playerNumber) + " moved down!")

      messageReceived = False
      playerNumber = 0

    window.after(100, MoveObject)

  MoveObject()

  window.mainloop()


def MQTT():
  def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    print("Subscibed!")

  def on_message(client, userdata, msg):
    message = msg.payload.decode()
    global playerNumber
    playerNumber = int(message[0])
    print(playerNumber)
    global messageReceived
    messageReceived = True
    global moveDir
    moveDir = message[2:]
    print(moveDir)

  client = mqtt.Client()
  client.connect("broker.mqttdashboard.com",1883,60)

  client.on_connect = on_connect
  client.on_message = on_message

  client.loop_forever()

jobGUI = Thread(target=GUI)
jobMQTT = Thread(target=MQTT)

jobGUI.start()
jobMQTT.start()
