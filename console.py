#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)

# Variables
# toiletPaper - corona - shoppingCar
player = "toiletPaper"
# 0 - 1 - 2 - ...
playerNumber = 0
hasNumber = True

# Buttons
buttonLeftPin = 19
buttonRightPin = 26
GPIO.setup(buttonLeftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonRightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Leds
leds = [16,20,21]
GPIO.setup(list(leds), GPIO.OUT)
GPIO.output(list(leds), GPIO.LOW)
 
 # 7 Segment
digitBitmap = { -1: 0b00000000, 0: 0b00111111, 1: 0b00000110, 2: 0b01011011, 3: 0b01001111, 4: 0b01100110, 5: 0b01101101, 6: 0b01111101, 7: 0b00000111, 8: 0b01111111, 9: 0b01101111 }
segmentMasks = { 'a': 0b00000001, 'b': 0b00000010, 'c': 0b00000100, 'd': 0b00001000, 'e': 0b00010000, 'f': 0b00100000, 'g': 0b01000000 }
segmentPins = { 'a': 4, 'b': 17, 'c': 27, 'd': 22, 'e': 5, 'f': 6, 'g': 13}
GPIO.setup(list(segmentPins.values()), GPIO.OUT)
GPIO.output(list(segmentPins.values()), GPIO.LOW)

def buttonLeft(channel):
	global hasNumber
	print("[Debug] Right button")
	if not hasNumber:
		print("[Debug] No player/ number assigned")
		requestPlayer()
		return
	#print("[Debug] Sending message: " + player + " " + str(playerNumber) + " - " + "UP")
	client.publish("game/" + player + str(playerNumber), "RIGHT")
	
def buttonRight(channel):
	global player
	global playerNumber
	print("[Debug] Left button")
	if not hasNumber:
		print("[Debug] No player/ number assigned")
		requestPlayer()
		return
	#print("[Debug] Sending message: " + player + " " + str(playerNumber) + " - " + "DOWN")
	client.publish("game/" + player + str(playerNumber), "LEFT")
	

def requestPlayer():
	# Todo: Ask console for a player and number
	# client.publish("requestplayer")
	# client.publish("requestnumber")
	print("[Debug] Requesting player")

# Called when received a message from the broker to assign a player and number
def assignPlayer(playerReceived, playerNumberReceived):
	global player
	global playerNumber
	player = playerReceived
	playerNumber = playerNumberReceived
	
	showNumber(playerNumber)
	print("[Debug] Playing with number: " + str(playerNumber))
	showLed()
	
def showNumber(number):
	digit = digitBitmap[number]
	GPIO.output(list(segmentPins.values()), GPIO.LOW)

	for segmentMask,segmentPin in segmentMasks.items():
		if digit & segmentPin == segmentPin:
			GPIO.output(segmentPins[segmentMask], GPIO.HIGH)
	
def showLed():
	global player
	global leds
	GPIO.output(list(leds), GPIO.LOW)
	if player == "corona":
		print("[Debug] Console assigned to CORONA")
		GPIO.output(leds[0], GPIO.HIGH)
	elif player == "shoppingCar":
		print("[Debug] Console assigned to SHOPPINGCAR")
		GPIO.output(leds[1], GPIO.HIGH)
	elif player == "toiletPaper":
		print("[Debug] Console assigned to TOILETPAPAER")
		GPIO.output(leds[2], GPIO.HIGH)

def on_connect(client, userdata, flags, rc):
	global topic
	print("[Debug] Connected with result code " + str(rc))
	client.subscribe("game/#")

def on_message(client, userdata, msg):
	message = str(msg.payload.decode("utf-8"))
	print("[Debug] received message: " + message)
	# Todo:
	# Check message when received and take action
	#if "" in message:
	#if "playerassign" in message:
	# 	assignPlayer(..., ...)

GPIO.add_event_detect(buttonLeftPin, GPIO.RISING, callback=buttonLeft, bouncetime=100)
GPIO.add_event_detect(buttonRightPin, GPIO.RISING, callback=buttonRight, bouncetime=100)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.mqttdashboard.com", port=1883, keepalive=60, bind_address="")
#client.subscribe("game/assignPlayer")


assignPlayer(player, playerNumber)

rc = 0
while rc == 0:
	rc = client.loop()
print("rc: " + str(rc))
    
    
GPIO.remove_event_detect(buttonLeftPin)
GPIO.remove_event_detect(buttonRightPin)
GPIO.cleanup()