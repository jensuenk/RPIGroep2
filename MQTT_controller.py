import paho.mqtt.client as paho
import array
import numpy as np
import time
from threading import Thread

toiletPapers = []
coronas = []
shoppingCart = [960,462]
jumpHeight = 22
xMoveSpeed = 20
rightBorder = 1800
botomBorder = 950
shoppingBorderLeft = 700
shoppingBorderRight = 1100

checker = 1

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
        #525
        topic = msg.topic[5:]
        print(topic)
        if topic == "init":
                numberOfToiletPaper = str(msg.payload)
                numberOfCoronas =str(msg.payload)
                print("Topic: "+topic +" number of carts: "+numberOfToiletPaper[2]+" number of coronas: " + numberOfCoronas[5])
                global toiletPapers
                global coronas 
                global checker
                checker = 1         
                toiletPapers = [[0] * int(numberOfToiletPaper[2]) for i in range(int(numberOfToiletPaper[2]))]
                coronas = [[0] * int(numberOfCoronas[5]) for i in range(int(numberOfCoronas[5]))]
                for x in range(int(numberOfToiletPaper[2])):                        
                        toiletPapers[x] = [0,242+x*242]
                        print("toilet paper added")
                
                for x in range(int(numberOfCoronas[5])):
                        coronas[x] = [1800,396+x*66]
                        print("corona added")  

                
                               
        else:                
                if topic == "moveEverything":      
                        for x in range(len(coronas)):
                                print("move corona")
                                moveCorona(x,-1,0)
                        for t in range(len(toiletPapers)):
                                moveToiletPaper(t,1,0)
                i = 0
                while i < 5 :
                        if topic == "toiletPaper"+str(i):
                                if str(msg.payload).find("UP") == -1:
                                        print("in toiletPaper"+str(i))
                                        if str(msg.payload).find("UP") == -1:
                                                if str(msg.payload).find("DOWN") == -1:
                                                        if str(msg.payload).find("LEFT") == -1:
                                                                print("right")
                                                                moveToiletPaper(i,1,0)
                                                        else:
                                                                print("left")
                                                                moveToiletPaper(i,-1,0)
                                                else:
                                                        print("down")
                                                        moveToiletPaper(i,0,1)
                                elif str(msg.payload).find("DIE") == -1 and str(msg.payload).find("POINT") == -1 :
                                        print("UP")
                                        moveToiletPaper(i,0,-1)
                        i+=1                

                i = 0
                while i < 5 :
                        if topic == "corona"+str(i):
                                if str(msg.payload).find("UP") == -1:
                                        print("in corona"+str(i))
                                        if str(msg.payload).find("UP") == -1:
                                                if str(msg.payload).find("DOWN") == -1:
                                                        if str(msg.payload).find("LEFT") == -1:
                                                                print("right")
                                                                moveCorona(i,1,0)
                                                        else:
                                                                print("left")
                                                                moveCorona(i,-1,0)
                                                else:
                                                        print("down")
                                                        moveCorona(i,0,1)
                                elif str(msg.payload).find("DIE") == -1 and str(msg.payload).find("POINT") == -1 :
                                        print("UP")
                                        moveCorona(i,0,-1)
                        i+=1                                
                if topic[(len(topic)-4):] != "life":
                         checkForCollision()

                if topic == "shoppingCart0":
                                if str(msg.payload).find("UP") == -1:
                                        print("in shopping"+str(i))
                                        if str(msg.payload).find("UP") == -1:
                                                if str(msg.payload).find("DOWN") == -1:
                                                        if str(msg.payload).find("LEFT") == -1:
                                                                print("right")
                                                                moveShoppingcart(1,0)
                                                        else:
                                                                print("left")
                                                                moveShoppingcart(-1,0)
                                                else:
                                                        print("down")
                                                        moveShoppingcart(0,1)
                                elif str(msg.payload).find("DIE") == -1 and str(msg.payload).find("POINT") == -1 :
                                        print("UP")
                                        moveShoppingcart(0,-1)
        
        print("Coronas matrix:")
        print(np.matrix(coronas))
        print("ToiletPapers matrix:")
        print(np.matrix(toiletPapers))
        print("shoppingcart")
        print(np.matrix(shoppingCart))

def moveCorona(corona,x,y):
        global coronas
        print(str(coronas[0])) 
        print("Previous coordinates: " + str(coronas[corona]))
        if (coronas[corona][0]+(x*xMoveSpeed)) < 0 or (coronas[corona][0]+(x*xMoveSpeed)) > rightBorder or (coronas[corona][1]+(y * jumpHeight)) < 0 or coronas[corona][1]+(y * jumpHeight) > botomBorder :
                print("test")
                client.publish("game/corona"+str(corona)+"_C" , "DIE" , qos=2)
                if corona == 0:
                        coronas[corona] = [1800,396]
                else:
                        coronas[corona] = [0,484] 
        else:
                coronas[corona] = [coronas[corona][0]+(x*xMoveSpeed) , coronas[corona][1]+(y * jumpHeight)]
                print("New coordinates: " + str(coronas[corona]))
                if x > 0 and y==0:
                        client.publish("game/corona"+str(corona)+"_C" , "right" , qos=2)
                if x < 0 and y==0:
                        client.publish("game/corona"+str(corona)+"_C"  , "left" , qos=2)
                if y > 0 and x==0:
                        client.publish("game/corona"+str(corona)+"_C"  , "down" , qos=2)
                if y < 0 and x==0:
                        client.publish("game/corona"+str(corona)+"_C"  , "up" , qos=2)        
        client.publish("Game/coronasCoor" , str(coronas) , qos=2)

def moveToiletPaper(toiletPaper,x,y):
        global toiletPapers
        print("Previous coordinates: " + str(toiletPapers[toiletPaper]))
        if toiletPapers[toiletPaper][0]+(x*xMoveSpeed) < 0 or toiletPapers[toiletPaper][0]+(x*xMoveSpeed) > rightBorder or toiletPapers[toiletPaper][1]+(y * jumpHeight) < 0 or toiletPapers[toiletPaper][1]+(y * jumpHeight) > botomBorder:
                print("test")
                if 0 or toiletPapers[toiletPaper][0]+(x*xMoveSpeed) > rightBorder:
                        client.publish("game/toiletPaper"+str(toiletPaper)+"_C" , "DIE" , qos=2)
                        if toiletPaper == 0:
                                toiletPapers[toiletPaper] = [0,242]
                        else:
                                toiletPapers[toiletPaper] = [0,484] 


        else:
                toiletPapers[toiletPaper] = [toiletPapers[toiletPaper][0]+(x*xMoveSpeed) , toiletPapers[toiletPaper][1]+(y * jumpHeight)]
                print("New coordinates: " + str(toiletPapers[toiletPaper])) 
                client.publish("Game/toiletPaperCoor" , str(toiletPapers) , qos=2)
                if x > 0 and y==0:
                        client.publish("game/toiletPaper"+str(toiletPaper)+"_C" , "right" , qos=2)
                if x < 0 and y==0:
                        client.publish("game/toiletPaper"+str(toiletPaper)+"_C" , "left" , qos=2)
                if y > 0 and x==0:
                        client.publish("game/toiletPaper"+str(toiletPaper)+"_C" , "down" , qos=2)
                if y < 0 and x==0:
                        client.publish("game/toiletPaper"+str(toiletPaper)+"_C" , "up" , qos=2)

def moveShoppingcart(x,y):
        global shoppingCart
        print("Previous coordinates shoppingCart: " + str(shoppingCart))
        if shoppingCart[0]+(x*xMoveSpeed) < shoppingBorderLeft or shoppingCart[0]+(x*xMoveSpeed) > shoppingBorderRight  or shoppingCart[1]+(y * jumpHeight) < 0 or shoppingCart[1]+(y * jumpHeight) > botomBorder:
                print("cart border hit")
        else:
                shoppingCart[0] = shoppingCart[0] + (x*xMoveSpeed)
                shoppingCart[1] = shoppingCart[1] + (y*jumpHeight)
                print("New coordinates shoppingCart: " + str(shoppingCart))
                if x > 0 and y==0:
                        client.publish("game/shoppingCart0_C" , "right" , qos=2)
                if x < 0 and y==0:
                        client.publish("game/shoppingCart0_C" , "left" , qos=2)
                if y > 0 and x==0:
                        client.publish("game/shoppingCart0_C" , "down" , qos=2)
                if y < 0 and x==0:
                        client.publish("game/shoppingCart0_C" , "up" , qos=2)

def checkForCollision():
        print("check for collision")
        for c in range(len(coronas)):
                for t in range(len(toiletPapers)):
                        print(str(coronas[c]) + " t: " + str(toiletPapers[t]))
                        #if str(coronas[c]) == str(toiletPapers[t]):
                        #102*78
                        #wc 102
                        if coronas[c][0] > toiletPapers[t][0]-50 and coronas[c][0] < toiletPapers[t][0]+50 and coronas[c][1] > toiletPapers[t][1]-60 and coronas[c][1] < toiletPapers[t][1]+60:
                                print("Collision corona and toiletpaper detected")
                                client.publish("game/toiletPaper"+str(t)+"_C" , "DIE" , qos=2)
                                if(t==0):
                                        toiletPapers[t] = [0,242]
                                else:
                                       toiletPapers[t] = [0,484]  
                                #
        for t in range(len(toiletPapers)):
                print(str(t) + "  :  " + str(shoppingCart))
                #if str(toiletPapers[t]) == str(shoppingCart):
                if shoppingCart[0] > toiletPapers[t][0]-70 and shoppingCart[0] < toiletPapers[t][0]+70 and shoppingCart[1] > toiletPapers[t][1]-70 and shoppingCart[1] < toiletPapers[t][1]+70:
                        print("collision toiletpaper and shoppingcart detected")
                        client.publish("game/toiletPaper"+str(t)+"_C" , "POINT" , qos=2)
                                #toiletPapers[t] = [-50,-50]
                        if(t==0):
                                toiletPapers[t] = [0,242]
                        else:
                                toiletPapers[t] = [0,484] 

def moveEverything():
        global checker
        print(checker)
        while checker == 1:
                time.sleep(0.5)
                client.publish("game/moveEverything" , "MOVE", qos=2)
                print("test")
        


job = Thread(target=moveEverything)
job.start()

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("81.165.114.134", 1883)
client.subscribe("game/#", qos=2)

client.loop_forever()

