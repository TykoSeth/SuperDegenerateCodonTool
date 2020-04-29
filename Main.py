from tkinter import *
from PIL import ImageTk, Image
import random
import time
import keyboard

root = Tk()
root.configure(background='black')

path = "Blue.png"

# Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = Image.open(path)

angle = 90
image = ImageTk.PhotoImage(img.rotate(angle))

# The Label widget is a standard Tkinter widget used to display a text or image on the screen.
Player = Label(root, image=image, bg="black")
Player.pack()
XX = -50
YY = 50
Player.place(x=XX, y=YY)

path = "Bullet.png"
bullet_img = Image.open(path)
bullet_tex = ImageTk.PhotoImage(bullet_img)

gameOn = False

goodBullets = 0
badBullets = 0
Bullet_texes = []
for i in range(13):
    Bullet_texes.append(Label(root, image=bullet_tex, bg="black"))
    Bullet_texes[i].place(x=-40, y=0)

Bullets = []


class Bullet_:
    X = 0
    Y = 0
    direction = 0
    isGood = FALSE

    def __init__(self, x, y, d, iG):
        self.X = x
        self.Y = y
        self.direction = d
        self.isGood = iG


class Rect_:
    X = 0
    Y = 0
    width = 0
    height = 0

    def __init__(self, xx, yy, w, h):
        self.X = xx
        self.Y = yy
        self.width = w
        self.height = h

    def Intersects(self, R):
        if self.X < R.X + R.width and self.Y < R.Y + R.height and self.X >= R.X and self.Y >= R.Y:
            return True
        if R.X < self.X + self.width and R.Y < self.Y + self.height and R.X >= self.X and R.Y >= self.Y:
            return True

        return False


class Tank:
    Boom = 0
    X = 0
    Y = 0
    direction = 0
    fireTime = 0
    Rect = Rect_(0, 0, 0, 0)

    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Boom = 0
        self.fireTime = 0
        self.direction = 0
        self.Rect = Rect_(X, Y, 30, 30)


def myClick(id):
    global buttonList
    global boolList
    # myLabel = Label(root, text=e)
    # myLabel.pack()
    # myLabel.place(x=300, y = 240)
    if boolList[id]:
        boolList[id] = FALSE
    else:
        boolList[id] = TRUE


direction = 0


def RectSetup():
    global Rects
    global buttonList, buttonRects
    Rects = []
    for i in range(len(buttonList)):
        Rects.append(Rect_())


spacePress = False


def Gem():  # hidden tank game
    global XX, YY
    global direction, img, image, blocks
    global Bullets
    global Bullet_texes, badBullets, goodBullets, spacePress
    xx = 0
    yy = 0
    speed = 4
    # RectSetup()
    if keyboard.is_pressed('left'):
        xx -= speed
        direction = 2
        angle = 90
        image = ImageTk.PhotoImage(img.rotate(angle))
        Player.config(image=image)
    elif keyboard.is_pressed('right'):
        angle = 270
        direction = 0
        image = ImageTk.PhotoImage(img.rotate(angle))
        Player.config(image=image)
        xx += speed
    elif keyboard.is_pressed('up'):
        direction = 1
        angle = 0
        image = ImageTk.PhotoImage(img.rotate(angle))
        Player.config(image=image)
        yy -= speed
    elif keyboard.is_pressed('down'):
        direction = 3
        angle = 180
        image = ImageTk.PhotoImage(img.rotate(angle))
        Player.config(image=image)
        yy += speed
    if keyboard.is_pressed('space') and goodBullets < 1 and spacePress == False:
        dx = 0
        dy = 0
        if direction == 0:
            dx = 22
            dy = 10
        if direction == 2:
            dx = -8
            dy = 10
        if direction == 1:
            dx = 10
            dy = -6
        if direction == 3:
            dx = 10
            dy = 28
        Bullets.append(Bullet_(XX + dx, YY + dy, direction, True))
        goodBullets += 1
        spacePress = True
    if not keyboard.is_pressed('space'):
        spacePress = False

    if XX + xx > 0 and XX + xx < 608:
        XX = XX + xx
        Player.place(x=XX + xx, y=YY)
    if YY + yy > 0 and YY + yy < 448:
        YY = YY + yy
        Player.place(x=XX, y=YY + yy)

    # bullet loop
    i = len(Bullets) - 1
    while i > -1:
        B = Bullets[i]
        destroy = False
        if B.direction == 0:  # going right
            B.X += 6
        if B.direction == 1:  # going up
            B.Y -= 6
        if B.direction == 2:  # going left
            B.X -= 6
        if B.direction == 3:  # going down
            B.Y += 6

        Bullet_texes[i].place(x=B.X, y=B.Y)


        #wall collisions
        Rect = Rect_(B.X, B.Y, 8, 8)
        for k in range(len(buttonRects)):
            if (Rect.Intersects(buttonRects[k])):
                destroy = True

        if B.X > 648 or B.X < -40 or B.Y > 480 or B.Y < -40:
            destroy = True
        if destroy:
            if B.isGood:
                goodBullets -= 1
            else:
                badBullets -= 1
            Bullet_texes[i].place(x=B.X, y=-100)
            Bullets.remove(B)

        i -= 1
    for j in range(len(Bullet_texes)):
        if j > len(Bullets):
            Bullet_texes[j].place(x=-50, y=-50)


def gameInit():
    global Bullets, Player, Tanks, XX, YY
    Bullets = []
    XX = 150
    YY = 150
    Player.place(x=XX,y=YY)
    Tanks = []

tpress = False
def main2():
    global buttonList
    global boolList
    global buttonRects, gameOn,tpress

    root.geometry("640x480")  # set window size
    root.title("Seth and Allwin")

    var = IntVar()
    C = Checkbutton(root, text="Check this box")
    C.pack()
    C.place(x=300, y=50)

    e = Entry(root, width=12, bg="#000050", fg="white", borderwidth=10)  # input field
    e.pack()
    e.place(x=200, y=50)
    e.insert(0, "0")  # sets a default value in there
    e.get()

    # myButton = Button(root, text="Click", command=myClick(e), fg="blue", bg="white", pady=50, padx=50)

    timer = 32
    timer2 = 0

    buttonList.append(Button(root, text="XXX", command=lambda: myClick(0), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(1), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(2), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(3), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(4), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(0), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(1), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(2), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(3), fg="black", bg="white"))
    buttonList.append(Button(root, text="XXX", command=lambda: myClick(4), fg="black", bg="white"))

    xx = 10
    yy = 10

    # myButton.pack()
    for i in range(len(buttonList)):
        buttonList[i].pack()
        buttonList[i].place(x=xx, y=yy)
        RR = Rect_(xx, yy, 30, 30)
        buttonRects.append(RR)
        yy += 80
        if yy > 180:
            yy = 10
            xx += 80
        boolList.append(FALSE)

    timerup = TRUE
    inTheLoop = TRUE
    # root.mainloop()
    while 1:
        root.update_idletasks()
        root.update()


        if keyboard.is_pressed('T'):
            if not tpress:
                if gameOn:
                    gameOn = False
                else:
                    gameInit()
                    gameOn = True
            tpress = True
        else:
            tpress = False

        if gameOn:
            Gem()


        timer2 += 1
        if timer2 > 8:
            timer2 = 0
            timer += 1

        if e.get() == "":
            e.insert(0, "0")

        # myButton.config(text=e.get())

        GG = "#" + "0000" + str(timer % 10) + "0"
        for i in range(len(buttonList)):
            if boolList[i]:
                buttonList[i].config(bg=GG)
            else:
                buttonList[i].config(bg="White")

        time.sleep(0.01)


buttonList = []
boolList = []
buttonRects = []
main2()
