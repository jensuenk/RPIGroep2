#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)

# Variables
topic = "Game"
clientId = "clientId-FhKqeekghi"
player = "toiletPaper"
playerNumber = 1
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
	client.publish("Game/" + player + str(playerNumber), "UP")
	
def buttonRight(channel):
	global player
	global playerNumber
	print("[Debug] Left button")
	if not hasNumber:
		print("[Debug] No player/ number assigned")
		requestPlayer()
		return
	#print("[Debug] Sending message: " + player + " " + str(playerNumber) + " - " + "DOWN")
	client.publish("Game/" + player + str(playerNumber), "DOWN")
	

def requestPlayer():
	# Todo: Ask console for a player and number
	# client.publish("requestplayer")
	# client.publish("requestnumber")
	print("[Debug] Requesting player")

# Called when received a message from the broker to assign a player and number
def assignPlayer(str, number):
	global player
	global playerReceived
	global leds
	player = playerReceived
	playerNumber = playerNumberReceived
	
	GPIO.output(list(leds), GPIO.LOW)
	if player == "toiletPaper":
		print("[Debug] Console assigned to TOILETPAPAER")
		GPIO.output(leds[2], GPIO.HIGH)
	elif player == "corona":
		print("[Debug] Console assigned to CORONA")
		GPIO.output(leds[0], GPIO.HIGH)
	elif player == "shoppingCar":
		print("[Debug] Console assigned to SHOPPINGCAR")
		GPIO.output(leds[1], GPIO.HIGH)
	showNumber(playerNumberReceived)
	print("[Debug] Playing with number: " + str(playerNumberReceived))
	
def showNumber(number):
	digit = digitBitmap[number]
	GPIO.output(list(segmentPins.values()), GPIO.LOW)

	for segmentMask,segmentPin in segmentMasks.items():
		if digit & segmentPin == segmentPin:
			GPIO.output(segmentPins[segmentMask], GPIO.HIGH)

def on_connect(client, userdata, flags, rc):
	global topic
	print("[Debug] Connected with result code " + str(rc))
	client.subscribe(topic)

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

client = mqtt.Client(clientId)
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.mqttdashboard.com", port=1883, keepalive=60, bind_address="")

rc = 0
while rc == 0:
	rc = client.loop()
print("rc: " + str(rc))
    
    
GPIO.remove_event_detect(buttonLeftPin)
GPIO.remove_event_detect(buttonRightPin)
GPIO.cleanup()