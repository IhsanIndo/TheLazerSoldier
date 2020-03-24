import os
import sys
import time
import keyboard
import random

map = dict()
problema = str()
PlocX = int()
PlocY = int()
PlocYold = int()
PlocXold = int()
kalah = bool()
tujuanPosTembak = [0, 0]
posListrik = []
posCelah = []
posDinamitAmbil = []
posDinamit = []
dinamitInt = 0
lazerInt = 100
waktuMusuhBeraksi = 0
dbg_mode = False
dbg_enabled = False
# ----- Start FPS Counter -----
FPS = int()
FPScount = int()
waktuDetikFPS = int()
wdfl = int()
# -----  End FPS Counter  -----


def pickupChecker(posDinamitAmbil, PlocY, PlocX, dinamit, posListrik):
    for a in posDinamitAmbil:
        if [PlocY, PlocX] == a:
            dinamit += 1
            posDinamitAmbil.remove(a)

    return [posDinamitAmbil, dinamit, posListrik]


def musuhAktif(pM, pP):   # AI Musuh v2
    print(pM)
    # Mirip AI nya Pacman
    # pM = Y-X-Yold-Xold-chaseMode   pP = Y-X-Yold-Xold
    for posm in pM:
    #if True:
            return posm


class Musuh:
    datas = []

    def __init__(self):
        pass

    def add(self, posY, posX, posYo, posXo, chsM): # Y X Yold Xold chaseMode
        self.datas.append([posY, posX, posYo, posXo, chsM])

    def kill(self, pos):
        self.datas.remove(pos)

    def active(self, view):
        pnum = 0
        for pM in self.datas:

            # Set random directions for enemy
            rand = random.randint(0, 4)
            # Y kebawah
            if rand == 0 and (pM[0]+1) != 24:
                pM[0] += 1

            # Y keatas
            if rand == 1 and (pM[0]-1) >= 0:
                pM[0] -= 1

            # X kekanan
            if rand == 2 and (pM[1]+1) != 119:
                pM[1] += 1

            # X kekiri
            if rand == 3 and (pM[1]-1) >= 0:
                pM[0] -= 1

            if pM[0] == 0 or pM[0] == -1:
                pM[0] = 1

            if pM[1] == 0 or pM[1] == -1:
                pM[1] = 1

            # set new values into datas
            self.datas[pnum] = pM

            pnum += 1

    def bind(self, view):
        num = 0
        for pM in self.datas:
            view[pM[0]][pM[1]] = "M"
            view[pM[2]][pM[3]] = " "
            self.datas[num][2] = pM[0]
            self.datas[num][3] = pM[1]
            num += 1
        return view

musuh = Musuh()


def bindPlayer(x, y, xo, yo):
    map[yo][xo] = " "
    map[y][x] = "@"
    yo = y
    xo = x
    return [xo, yo]


def cekKontrol(PlocY, PlocX, kalah, lazerInt, dinamit, posDinamit, musuh):

    # Pergerakan Player

    if keyboard.is_pressed("w"):
        if not PlocY == 0:
            if map[PlocY-1][PlocX] != "#":
                PlocY -= 1
            elif map[PlocY-1][PlocX] == "M":
                kalah = True
    
    elif keyboard.is_pressed("s"):
        if not PlocY == 24:
            if map[PlocY+1][PlocX] != "#":
                PlocY += 1
            elif map[PlocY+1][PlocX] == "M":
                kalah = True
    
    elif keyboard.is_pressed("d"):
        if not PlocX == 119:
            if map[PlocY][PlocX+1] != "#":
                PlocX += 1
            elif map[PlocY][PlocX+1] == "M":
                kalah = True
    
    elif keyboard.is_pressed("a"):
        if not PlocX == 0:
            if map[PlocY][PlocX-1] != "#":
                PlocX -= 1
            elif map[PlocY][PlocX-1] == "M":
                kalah = True

    # Tembakan

    if not lazerInt <= 0:
        if keyboard.is_pressed("right") or keyboard.is_pressed("f"):
            for a in range(PlocX + 1, 119):
                if a == 119:
                    tujuanPosTembak[0] = 119
                    tujuanPosTembak[1] = PlocY
                    break
                if map[PlocY][a] == "#":
                    tujuanPosTembak[0] = a
                    tujuanPosTembak[1] = PlocY
                    break
                elif map[PlocY][a] == "M":
                    musuh.kill([PlocY, a, PlocY, a])
                    map[PlocY][a] = " "
                    tujuanPosTembak[0] = a - 1
                    tujuanPosTembak[1] = PlocY
                    break
            for a in range(PlocX + 1, tujuanPosTembak[0]):
                map[PlocY][a] = "─"
            lazerInt -= 1

        elif keyboard.is_pressed("left"):
            c = list()
            for b in range(0, PlocX):
                c.append(b)
            c = list(reversed(c))
            for a in c:
                if map[PlocY][a] == "#":
                    tujuanPosTembak[0] = a + 1
                    tujuanPosTembak[1] = PlocY
                    break
                elif map[PlocY][a] == "M":
                    musuh.kill([PlocY, a, PlocY, a])
                    map[PlocY][a] = " "
                    tujuanPosTembak[0] = a + 1
                    tujuanPosTembak[1] = PlocY
                    break
            for a in range(tujuanPosTembak[0], PlocX):
                map[PlocY][a] = "─"
            lazerInt -= 1

        elif keyboard.is_pressed("up"):
            c = list()
            
            for b in range(0, PlocY):
                c.append(b)
            
            c = list(reversed(c))
            
            for a in c:
                
                if map[a][PlocX] == "#":
                    tujuanPosTembak[0] = PlocX
                    tujuanPosTembak[1] = a + 1
                    break
                
                elif map[a][PlocX] == "M":
                    musuh.kill([a, PlocX, a, PlocX])
                    map[a][PlocX] = " "
                    tujuanPosTembak[0] = PlocX
                    tujuanPosTembak[1] = a + 1
                    break
            
            for a in range(tujuanPosTembak[1], PlocY):
                map[a][PlocX] = "│"
            lazerInt -= 1

        elif keyboard.is_pressed("down"):
            
            for a in range(PlocY + 1, 119):
                
                if a == 25:
                    tujuanPosTembak[0] = PlocX
                    tujuanPosTembak[1] = 25
                    break
                
                if map[a][PlocX] == "#":
                    tujuanPosTembak[0] = PlocX
                    tujuanPosTembak[1] = a
                    break
                
                elif map[a][PlocX] == "M":
                    musuh.kill([a, PlocX, a, PlocX])
                    map[a][PlocX] = " "
                    tujuanPosTembak[0] = PlocX
                    tujuanPosTembak[1] = a - 1
                    break

            for a in range(PlocY + 1, tujuanPosTembak[1]):
                map[a][PlocX] = "│"
            lazerInt -= 1

    if keyboard.is_pressed("e"):
        if not dinamit == 0 and not dinamit < 0:
            if map[PlocY - 1][PlocX] == " ":
                dinamit -= 1
                map[PlocY - 1][PlocX] = "o"
                posDinamit.append([PlocY - 1, PlocX])

            elif map[PlocY - 1][PlocX - 1] == " ":
                dinamit -= 1
                map[PlocY - 1][PlocX - 1] = "o"
                posDinamit.append([PlocY - 1, PlocX - 1])

            elif map[PlocY + 1][PlocX] == " ":
                dinamit -= 1
                map[PlocY + 1][PlocX] = "o"
                posDinamit.append([PlocY + 1, PlocX])

            elif map[PlocY + 1][PlocX + 1] == " ":
                dinamit -= 1
                map[PlocY + 1][PlocX + 1] = "o"
                posDinamit.append([PlocY + 1, PlocX + 1])

            elif map[PlocY][PlocX - 1] == " ":
                dinamit -= 1
                map[PlocY][PlocX - 1] = "o"
                posDinamit.append([PlocY, PlocX - 1])

            elif map[PlocY + 1][PlocX - 1] == " ":
                dinamit -= 1
                map[PlocY][PlocX] = "o"
                posDinamit.append([PlocY, PlocX])

            elif map[PlocY][PlocX + 1] == " ":
                dinamit -= 1
                map[PlocY][PlocX + 1] = "o"
                posDinamit.append([PlocY, PlocX + 1])

            elif map[PlocY - 1][PlocX + 1] == " ":
                dinamit -= 1
                map[PlocY - 1][PlocX + 1] = "o"
                posDinamit.append([PlocY - 1, PlocX + 1])
    
    for a in posListrik:
        
        if [PlocY, PlocX, PlocY, PlocX] == a:
            lazerInt += 10
            
            if lazerInt > 100:
                lazerInt = 100
            posListrik.remove(a)

    return [PlocY, PlocX, kalah, lazerInt, dinamit, posDinamit, musuh]


def draw():
    # Nge print seluruh isi dict map
    strtes = str()
    
    for a in range(0, 24):
        
        for b in range(0, 120):
            strtes += map[a][b]
        
        print(strtes)
        strtes = ""


def initialization(kem):
    # Nge buat Peta dengan parameter nilai kemungkinan yang sudah dimasukkan pada awal dibuka
    ltest = list()
    for a in range(0, 120):
        ltest.append("#")
    map[0] = ltest
    ltest = list()
    ltest.append("#")
    
    for a in range(0, 120):
        if random.randint(0, kem) == random.randint(0, kem):
            ltest.append("#")
        
        else:
            ltest.append(" ")
    
    map[1] = ltest
    lunit = []
    
    for a in range(0, 25):
        lunit.append("#")
        
        for b in range(0, 120):
            
            try:
                if random.randint(1, kem - int(kem/2)) == random.randint(1, kem - int(kem/2)) and map[a][b-1] == "#":
                    lunit.append("#")
                
                elif random.randint(1, kem + int(kem / 4)) == random.randint(1, kem + int(kem / 4)) and map[a-1][b] == "#":
                    lunit.append("#")
                
                else:
                    lunit.append(" ")
            except KeyError:
                if random.randint(1, kem - int(kem / 2)) != random.randint(1, kem - int(kem / 2)):
                    lunit.append("#")
                
                else:
                    lunit.append(" ")
            
            except IndexError:
                lunit.append(" ")
        
        lunit.append("#")
        map[a] = lunit
        lunit = []

    map[0][1] = ""

    for a in range(0, 120):
        ltest.append("#")
    map[23] = ltest

    for c in range(0, random.randint(20, 300)):
        if random.randint(1, kem) == random.randint(1, kem):
            a = random.randint(2, 23)
            b = random.randint(2, 118)
            map[a][b] = "M"
            musuh.add(a, b, a, b, False)  # Y, X, Yold, Xold, chaseMode

    if True:
        for c in range(0, random.randint(kem-int(kem/2), kem+3)):
            a = random.randint(0, 24)
            b = random.randint(0, 119)
            map[a][b] = "M"
            musuh.add(a, b, a, b, False)  # Y, X, Yold, Xold, chaseMode
        print(musuh.datas)
    
    for ghj in range(0, random.randint(0, 100)):
        if random.randint(1, kem + 5) == random.randint(1, kem + 5):
            random1 = random.randint(0, 24)
            random2 = random.randint(0, 119)
            map[random1][random2] = "I"
            posListrik.append([random1, random2, random1, random2])  # Y, X, Yold, Xold

    # Penaruh DINAMIT AMBIL
    for a in range(5, 30): # DINAMIT itu agk langka
        if random.randint(1, kem) == random.randint(1, kem):
            random1 = random.randint(0, 24)
            random2 = random.randint(0, 119)
            map[random1][random2] = "■"
            posDinamitAmbil.append([random1, random2])
            # Display dinamit setelah di taruh : ǒ


if __name__ == "__main__":
    # DEBUG MODE CHECKER
    try:
        if sys.argv[1] == "dbg_mode":
            dbg_mode = True
            lazerInt = int(sys.argv[2])
            dinamitInt = int(sys.argv[3])
    except:
        pass
    
    # TODO : BUAT DINAMIT

    if os.name != "nt": os.system("clear")
    else: os.system("cls")

    print("\n\n\n")
    print(" [i] Kemungkinan temboknya Random atau tidak? [i]")
    kemungkinan = input("Random atau tidak? [y/t] ")
    if kemungkinan == "y":
        initialization(random.randint(5, 50))
    elif kemungkinan == "t":
        print(" [i] min. 2, maks. 70 (Masukkan Nomor) [i]")
        try:
            kemungkinan = int(input("Masukkan kemungkinan Tembok = "))
        except ValueError:
            exit()
        else:
            initialization(kemungkinan)

    waktuDetikFPS = int(time.perf_counter())
    while True:

        # Print Bar
        print("\n                                                   The Lazer Soldier\n" +
              "                                                     --By Ihsan--         | " +
              str(FPS) + " FPS |")
        print("X: " + str(PlocX) + " ,Y: " + str(PlocY))
        print("_" * 120)

        lbj = cekKontrol(PlocY, PlocX, kalah, lazerInt, dinamitInt, posDinamit, musuh)  # Ngecek klo player nge-klik WASD dll..

        PlocY = lbj[0]  # Memasukkan var hasil return func cekKontrol ke variabel penting
        PlocX = lbj[1]
        kalah = lbj[2]
        lazerInt = lbj[3]
        dinamitInt = lbj[4]
        posDinamit = lbj[5]
        musuh = lbj[6]

        # Sistem biar bisa keluar
        # Biasanya digunakan saat game nge-bug, atau keluar kesalahan.
        if keyboard.is_pressed("q"):
            os.system("cls")
            exit()

        musuh.active(map)  # Buat Musuh bisa bergerak (AI)
        musuh.bind(map)  # Bind Musuh ke map

        a = bindPlayer(PlocX, PlocY, PlocXold, PlocYold)  # Ngeposisikan Player ke tempat yang sudah di
        PlocXold = a[0]                                   # atur pada function cekKontrol()
        PlocYold = a[1]

        draw()  # Draw Map

        # Print Sisa listrik dari Int LazerInt          Dan nge-print jumlah dinamit yang dipunya
        print("\nSisa Listrik = " + str(lazerInt) + "%" + " | Dinamit = " + str(dinamitInt))

        for a in range(0, 25):                           # Ngehapus lazer biar nggak ada jejaknya ;)
            for b in range(0, 120):
                if map[a][b] == "─" or map[a][b] == "│":
                    map[a][b] = " "

        # time.sleep(0.08)  # diberi delay agar beraturan

        # Sistem buat ngecek klo player kalah

        if kalah:
            break
        
        if len(musuh.datas) == 0:
            break
        
        if [PlocY, PlocX, PlocY, PlocX] in musuh.datas:
            kalah = True
            problema = "Kena Musuh"
            break

        if (lazerInt == 0 and len(posListrik) == 0) or (lazerInt < 0 and len(posListrik) == 0):
            kalah = True
            problema = "Kehabisan Listrik"
            break

        # Pickup Checker
        data = pickupChecker(posDinamitAmbil, PlocY, PlocX, dinamitInt, posListrik)
        posDinamitAmbil = data[0]
        dinamitInt = data[1]

        # nge-print ulang pickup item yg di tindihin musuh atau lazer
        for a in posListrik:
            if not map[a[0]][a[1]] == "M" or map[a[0]][a[1]] == "─" or map[a[0]][a[1]] == "│":
                map[a[0]][a[1]] = "I"

        for a in posDinamitAmbil:
            if not map[a[0]][a[1]] == "M" or map[a[0]][a[1]] == "│" or map[a[0]][a[1]] == "─":
                map[a[0]][a[1]] = "■"

        for a in posDinamit:
            if not map[a[0]][a[1]] == "│" or map[a[0]][a[1]] == "─" or map[a[0]][a[1]] == "─":
                map[a[0]][a[1]] = "o"

        if os.name != "nt": os.system("clear")
        else: os.system("cls")

        waktuDetikFPS = int(time.perf_counter())   # Menghitung berapa Frame per Detik (FPS)
        if waktuDetikFPS == wdfl + 1:      # Udah kena delay, jadi.. bukan FPS asli..
            wdfl = waktuDetikFPS
            FPS = FPScount
            FPScount = 0
        else:
            FPScount += 1

        # Developer debug things
        if dbg_mode:
            if dbg_enabled:
                print("posMusuh: "+ str(musuh.datas) + "\nposDinamit: " + str(posDinamit) + "\nposDinamitAmbil: " + str(posDinamitAmbil) + "\nposListrik: " + str(posListrik))

            if keyboard.is_pressed("x"):
                dbg_enabled = True
            elif keyboard.is_pressed("z"):
                dbg_enabled = False
    if os.name != "nt": os.system("clear")
    else: os.system("cls")

    print("")
    if kalah:
        print("                                                   Anda Kalah                " + problema + "\n")
    else:
        print('                                                  Anda Menang')
    print("_" * 120)
    print("\n Tekan Enter untuk Keluar")
    input()

    if os.name != "nt": os.system("clear")
    else: os.system("cls")
