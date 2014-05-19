#!/usr/bin/env python3

# Attempt for zombies
# I discovered after the CTF was over that the server was using only x for the
# decision of whether a pistol would work or not, while I used sqrt(x^2+y^2).
# This caused mine to use the rifle when it wasn't needed, causing the rifle to
# run out of ammo.
# mal <mal@sec.gd>

import socket, math
from time import sleep

g = 9.8

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("zombies_8977dda19ee030d0ea35e97ad2439319.2014.shallweplayaga.me", 20689))
s.settimeout(0.1) # non-blocking-ish

s.sendall("2\n3\n".encode("ascii"))
velocity = {"r": 975, "p": 375}
pistolammo = True

x=y=px=py=zx=zy=angle=0
mode = ""
weapon=lastweapon="p"
time = 0

shots = {"r": 0, "p": 0}

while True:
    data = ""
    reading = True
    while reading:
        try:
            data += s.recv(1024).decode("ascii")
        except socket.timeout:
            reading = False
    for dataline in data.split('\n'):
        if len(dataline) == 0: continue
        print("RECV:",dataline)
        if dataline.startswith("The zombie is stalking a puppy "):
            words = dataline.split(" ")
            if words[6] == "across":
                mode = "hillside"
                px = int(words[14][:-1])
                py = int(words[19][:-1])
                zx = int(words[28][:-1])
                zy = int(words[33][:-1])
            else:
                mode = "normal"
                zx = int(words[6][:-1])
                zy = int(words[11][:-1])
            print("Info: px=" + str(px) + " py=" + str(py) + " zx=" + str(zx) + " zy=" + str(zy) + " dx=" + str(x-zx) + " dy=" + str(y-zy))
            continue

        if dataline == "Enter your shot details:":
            baddistance = math.sqrt(pow(max(px,zx),2)+pow(max(py,zy),2)) # Base this only on X and decide after we have the target X
            if baddistance <= 50 and pistolammo:
                weapon = "p"
            else:
                weapon = "r"
            if mode == "hillside":
                if lastweapon != weapon:
                    sleep(2.1)
                    delay = 2
                else:
                    delay = 1 #+ baddistance/velocity[weapon]
                x = px-((px-zx)*(delay/time))
                y = py-((py-zy)*(delay/time))
            else:
                x = zx
                y = zy

            angle = math.degrees(math.atan((pow(velocity[weapon],2)-math.sqrt(pow(velocity[weapon],4)-g*(g*pow(x,2)+2*y*pow(velocity[weapon],2))))/(g*x)))
            print("Info: weapon="+weapon,"angle="+str(angle),"px="+str(px),"py="+str(py),"zx="+str(zx),"zy="+str(zy),"dx="+str(x-zx),"dy="+str(y-zy))
            s.sendall((weapon + "," + str(angle) + "," + str(x) + "," + str(y) + "\n").encode("ascii"))
            print("Send:", weapon + "," + str(angle) + "," + str(x) + "," + str(y))
            shots[weapon] += 1
            print("Info: Shots fired: " + str(shots))
            continue

        if dataline.startswith("Sorry, you missed by "):
            print("Info: dd=" + str(baddistance/velocity[weapon]), ", off by", float(dataline.split(" ")[4])*(time/math.sqrt(pow(px-zx,2)+pow(py-zy,2))), "seconds")

        if dataline == "--------------------------":
            lastweapon = weapon
            x=y=px=py=zx=zy=0
            continue

        if dataline.startswith("You have ") and dataline.endswith("seconds before the zombie eats the puppy!"):
            time = int(dataline.split(" ")[2])
            continue


