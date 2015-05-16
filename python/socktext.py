#!/usr/bin/env python2

import socket

class socktext:
    def __init__(self, sock, lineend="\n"):
        self.s = sock
        self.lineend = lineend
        self.chaf = ""

    def recv_until(self, term):
        alldata = self.chaf
        self.chaf = ""
        try:
            while alldata.find(term) == -1:
                data = self.s.recv(4096)
                if not data:
                    raise EOFError
                alldata += data
            indx = alldata.find(term) + len(term)
            alldata, chaf = alldata[:indx], alldata[indx:]
        except:
            print alldata
            raise IndexError
        return alldata

    def recv_line(s):
        return recv_until(s, "\n")

    def recv_line_until(s, term):
        global chaf
        alldata = chaf
        chaf = ""
        try:
            while alldata.find(term) == -1 or alldata.find("\n", alldata.find(term)) == -1:
                data = s.recv(4096)
                if not data:
                    raise EOFError
                alldata += data
            indx = alldata.find("\n", alldata.find(term)) + 1
            alldata, chaf = alldata[:indx], alldata[indx:]
        except:
            print alldata
            raise IndexError
        return alldata

    def recv_everything(s):  # Rely on timeouts to grab all available data
        alldata = ""
        try:
            data = s.recv(4096)
            while data:
                alldata += data
                data = s.recv(4096)
        except timeout:
            pass
        return alldata



while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR, PORT))
    s.settimeout(1.0)  # IMPORTANT FOR THE more_recv FUNCTION. 0.5 works nicely for me -duck
    print recv_line_until(s, "maxbet:")
    print "+endmb"

    playing = True
    while playing:
        try:
            purse = recv_line_until(s, "purse")
            dealer = recv_line_until(s, "plays")
            print "p+", purse, "d+", dealer
            print "b+", recv_until(s, "bet")
            purse = int(purse.split(":")[1].strip())
            
            c1, c2 = map(int, dealer.split(":")[1].split())
            print purse, c1, c2
            if c2-c1 > 10:
                bet = int(purse*3/4)
            else:
                bet = 1

            time.sleep(random.randrange(5, 40)/10.0)
            s.send(str(bet) + "\n")
            recv_line_until(s, "next card is")
        except IndexError:
            print "we lost"
            playing = False
            s.close()

