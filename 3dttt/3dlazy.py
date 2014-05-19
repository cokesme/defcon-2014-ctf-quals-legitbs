#!/usr/bin/env python3

# Use the prioritized move list
# Based on the pre-existing 3dttt.py, that's why 90% of the code does nothing
# mal <mal@sec.gd>

import socket

moves = [
        ["1","1","1"],
        ["0","0","0"],
        ["0","0","2"],
        ["0","2","0"],
        ["0","2","2"],
        ["2","0","0"],
        ["2","0","2"],
        ["2","2","0"],
        ["2","2","2"],
        ["0","1","1"],
        ["1","0","1"],
        ["1","1","0"],
        ["1","1","2"],
        ["1","2","1"],
        ["2","1","1"],
        ["0","0","1"],
        ["0","1","0"],
        ["0","1","2"],
        ["0","2","1"],
        ["1","0","0"],
        ["1","0","2"],
        ["1","2","0"],
        ["1","2","2"],
        ["2","0","1"],
        ["2","1","0"],
        ["2","1","2"],
        ["2","2","1"]]

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("3dttt_87277cd86e7cc53d2671888c417f62aa.2014.shallweplayaga.me", 1234))
    s.settimeout(0.01) # almost non-blocking 10ms timeout

    board = [[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]],[[" "," "," "],[" "," "," "],[" "," "," "]]]
    z=" "
    movenum = 0

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
                continue
            if len(dataline) > 0 and dataline[0] in ['0','1','2']:
                board[0][int(dataline[0])][z] = dataline[3]
                board[1][int(dataline[0])][z] = dataline[7]
                board[2][int(dataline[0])][z] = dataline[11]
                continue
            if dataline == "Choose Wisely (x,y,z): ":
                myx,myy,myz = move(board, movenum)
                movenum += 1
                s.sendall((str(myx)+","+str(myy)+","+str(myz)+"\n").encode("ascii"))
                continue
            if dataline[0:11] == "You've won ":
                print(dataline)
                movenum = 0
                continue
            if len(dataline) > 1 and dataline != "  ---+---+---" and dataline[1:9] != " Winning":
                print(dataline)

def showboard(board):
    print('')
    for z in range(0,3):
        print("z=" + str(z) + "     x= " + "0 1 2")
        for y in range(0,3):
            print("z=" + str(z) + " y=" + str(y) + "   |" + str(board[0][y][z]) + " " + str(board[1][y][z]) + " " + str(board[2][y][z]) + "|")



def move(board, movenum):
    x,y,z = moves[movenum][0],moves[movenum][1],moves[movenum][2]
    #print("Moving",x,y,z)
    return x,y,z


if __name__ == '__main__':
    main()

