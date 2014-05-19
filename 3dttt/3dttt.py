#!/usr/bin/env python3

# Basic programmatic interface to 3dttt
# mal <mal@sec.gd>

import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("3dttt_87277cd86e7cc53d2671888c417f62aa.2014.shallweplayaga.me", 1234))
    s.settimeout(0.01) # almost non-blocking 10ms timeout

    board = [[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]]]
    z=" "

    while True:
        data = ""
        reading = True
        while reading:
            try:
                data += s.recv(2048).decode("ascii")
            except socket.timeout:
                reading = False
        for dataline in data.split('\n'):
            if len(dataline) > 18 and dataline[16:18] == "z=":
                z = int(dataline[18])
            if len(dataline) > 0 and dataline[0] in ['0','1','2']:
                board[0][int(dataline[0])][z] = dataline[3]
                board[1][int(dataline[0])][z] = dataline[7]
                board[2][int(dataline[0])][z] = dataline[11]
            if dataline == "Choose Wisely (x,y,z): ":
                myx,myy,myz = move(board)
                s.sendall((str(myx)+","+str(myy)+","+str(myz)+"\n").encode("ascii"))

def showboard(board):
    print('')
    for z in range(0,3):
        print("z=" + str(z) + "     x= " + "0 1 2")
        for y in range(0,3):
            print("z=" + str(z) + " y=" + str(y) + "   |" + str(board[0][y][z]) + " " + str(board[1][y][z]) + " " + str(board[2][y][z]) + "|")



def move(board):
    while True:
        showboard(board)
        xyz = input("Enter desired move as XYZ, each 0-2: ")
        x, y, z = int(xyz[0]), int(xyz[1]), int(xyz[2])
        if not (x < 0 or y < 0 or z < 0 or x > 2 or y > 2 or z > 2):
            break
    print("Moving",x,y,z)
    return x,y,z


if __name__ == '__main__':
    main()

