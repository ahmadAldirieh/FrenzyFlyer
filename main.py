###########################
# Game: Frenzy Flyer

#Done by: Ahmad Aldirieh

###########################
from tkinter import *
from time import *
from random import *
import numpy as np

root = Tk()
screen = Canvas(root, width=600, height=800, background="black")

def setInitialValues():

	#Main game variables
	global score,amountbullets,scoreadder,scoremultiplier
	
	score=0
	amountbullets=3
	scoreadder=5
	scoremultiplier=1


	#High score variable
	global highscore

	#Tries to load high score from highscore.csv
	try:
		highscore=list(np.loadtxt("highscore.csv",delimiter=','))

	#If highscore.csv is empty then it sets high score to 0
	except FileNotFoundError:
		highscore=[0]

	#Different screen related things, and variables to check if player is still alive
	global running,dead,introscreen,controlscreen,birdscreen
	
	running="true"
	dead="false"
	introscreen="true"
	controlscreen="false"
	birdscreen="false"

	#Plane initial cordinates and speed
	global planeY,planeX,planespeed
	
	planeY=350
	planeX=100
	planespeed=0

	#Bullet drawings (displays the amount of bullets you have)
	global bulletdrawx,bulletdrawy,xchangebullet
	
	bulletdrawx=500
	bulletdrawy=50
	xchangebullet=30

	#Bullet related variables
	global bulletX,bulletY,bulletXspeed,bullets,maxspeed
	
	bulletX=[]
	bulletY=[]
	bullets=[]
	bulletXspeed=30
	maxspeed=10
	
	#Cordinates for the main mountain 
	global x1mountain,y1mountain,x2mountain,y2mountain,x3mountain,y3mountain
	
	x1mountain=220
	y1mountain=300
	x2mountain=300
	y2mountain=150
	x3mountain=380
	y3mountain=300

	#Cloud variables
	global xcloud,ycloud,sizecloud,numcloud
	numcloud=150
	xcloud=[]
	ycloud=[]
	sizecloud=[]

	#Snow variables
	global xsnow,ysnow,snowsize,snow,snowspeedy,snowspeedx
	
	xsnow=[]
	ysnow=[]
	snowsize=[]
	snow=[]
	snowspeedy=[]
	snowspeedx=[]

	#Fills in 200 different variables for each snow particle 
	for i in range(200):
		xsnow.append(randint(0,600))
		ysnow.append(randint(-50,0))
		snowsize.append(randint(5,10))
		snow.append(0)
		snowspeedy.append(uniform(1,8))
		snowspeedx.append(uniform(-2,0))

	#Bird related variables
	global birdY,spawnodd,birdtype,birdframe,birds,birdX
	
	birdY=0
	spawnodd=0
	birdtype=""
	birds=[]
	birdspeed=0

	#Game difficulty related variables
	global num,framecounter,birdmultiplier
	
	framecounter=0
	birdmultiplier=1

	#Starts at a difficulty of 15 which is pretty easy
	global num 
	num=15
		
	#Key buttons and mouse click variables
	global xMouse,yMouse,up,down,space
	
	xMouse=0
	yMouse=0
	up= False
	down= False
	space= False 

	#Imported images 
	global plane,logo,bird_frames,bulletimage,upkey,downkey,background1

	#Set each colour to 2 different pictures which are the 2 frames for each bird
	bird_frames = {
		"gold":[PhotoImage(file="Images/gold bird.png"),PhotoImage(file="Images/gold bird 2.png")],
		"grey":[PhotoImage(file="Images/grey bird.png"),PhotoImage(file="Images/grey bird 2.png")],
		"green":[PhotoImage(file="Images/green bird.png"),PhotoImage(file="Images/green bird 2.png")],
		"red":[PhotoImage(file="Images/red bird.png"),PhotoImage(file="Images/red bird 2.png")],	
	}
	plane=PhotoImage(file="Images/plane.png")
	logo=PhotoImage(file="Images/logo.png")
	bulletimage=PhotoImage(file="Images/bullet.png")
	upkey=PhotoImage(file="Images/up.png")
	downkey=PhotoImage(file="Images/down.png")
	background1=PhotoImage(file="Images/background.png")

def mouseClickHandler( event ):
	global introscreen,birdscreen,controlscreen,dead,running
	
	Xmouse = event.x
	Ymouse = event.y

	if introscreen=="true":
		#PLAY button (sets introscreen to false and therefore runs the game)
		if 200 < Xmouse < 400 and 300 < Ymouse < 370:
			introscreen="false"

		#Controls button, sends person to control screen
		if 50 < Xmouse <250 and 400 <Ymouse<470:
			controlscreen="true"

		#Power up botton sends person to powerup screen
		if 350 <Xmouse<550 and 400<Ymouse<470:
			birdscreen="true"

	#Back button if person is on the power up screen or the control screen, returns person to introscreen 
	if birdscreen=="true" or controlscreen=="true":
		if 20 <Xmouse<180 and 20<Ymouse<70:
			controlscreen="false"
			birdscreen="false"
			
	if dead=="true":
		#Play again button (reruns game)
		if 75<Xmouse<275 and 400<Ymouse<500:
			runGame()

		#Quit button
		elif 325<Xmouse<525 and 400<Ymouse<500:
			#Function to stop the code from running
			quit()

#Creates the controlscreen
def controlscreencreate():
	global bird_frames,upkey,downkey

	#Deletes the introscreen, creates the imported background 
	screen.delete("all")
	screen.create_image(300,400,image=background1)

	#Back button
	screen.create_rectangle(20,20,180,70,fill="gold",width=5,outline="orange")
	screen.create_text(100,45,text="BACK",font="Arial 15")

	#Displays the controls and objective of the game 
	screen.create_text(300,150,text="CONTROLS", font="Arial 20 bold",fill="black")
	screen.create_text(300,250,text="Use the up and down arrow keys to dodge incoming birds", font="Arial 12",fill="black")
	screen.create_image(560,250,image=upkey)
	screen.create_image(40,250,image=downkey)
	screen.create_text(300,350,text="Use the space bar to shoot a bullet at an incoming bird",font="Arial 13",fill="black")
	screen.create_text(300,500,text="The goal is to try to beat your highscore!",font="Arial 13",fill="black")

	#Draws the space bar 
	screen.create_rectangle(200,400,400,450,fill="",outline="black",width=5)
	screen.create_line(225,410,375,410,fill="black",width=3,smooth=True)

#Creates the birdscreen
def birdscreencreate():

	#Deletes introscreen, draws imported background
	screen.delete("all")
	screen.create_image(300,400,image=background1)

	#Back button
	screen.create_rectangle(20,20,180,70,fill="gold",width=5,outline="orange")
	screen.create_text(100,45,text="BACK",font="Arial 15")

	#Creates the text for all the power ups 
	screen.create_text(300,150,text="POWER UPS", font="Arial 20 bold",fill="black")
	screen.create_text(300,200,text="You can get powerups by shooting different colour birds!",font="Arial 13 ",fill="black")
	screen.create_text(300,300,text="Grey birds dont grant powerups",font="Arial 14",fill="black")
	screen.create_text(300,400,text="Green birds grant bullet refill (3)",font="Arial 14",fill="black")
	screen.create_text(300,500,text="Red birds grant +5000 score",font="Arial 14",fill="black")
	screen.create_text(300,600,text="Gold birds grant 2x score multiplier",font="Arial 14 ",fill="black")

	#Draws the birds on the right 
	screen.create_image(500,300,image=bird_frames["grey"][0])
	screen.create_image(500,400,image=bird_frames["green"][0])
	screen.create_image(500,500,image=bird_frames["red"][0])
	screen.create_image(500,600,image=bird_frames["gold"][0])

	#Draws the birds on the left (second frame)
	screen.create_image(100,300,image=bird_frames["grey"][1])
	screen.create_image(100,400,image=bird_frames["green"][1])
	screen.create_image(100,500,image=bird_frames["red"][1])
	screen.create_image(100,600,image=bird_frames["gold"][1])

#Creates the intro screen 
def introscreencreate():
	global logo

	#Deletes any other screens (if player presses back button), draws imported background
	screen.delete("all")
	screen.create_image(300,400,image=background1)

	#Draws my custom made logo 
	screen.create_image(300,150,image=logo)

	#Draws the three buttons 
	screen.create_rectangle(200,300,400,370,fill="gold",width=5,outline="orange")
	screen.create_rectangle(50,400,250,470,fill="gold",width=5,outline="orange")
	screen.create_rectangle(350,400,550,470,fill="gold",width=5,outline="orange")
	screen.create_text(300,335,text="PLAY",font="Arial 21 bold",fill="green")
	screen.create_text(150,435,text="CONTROLS",font="Arial 21 bold",fill="navy")
	screen.create_text(450,435,text="POWER UPS",font="Arial 21 bold",fill="navy")


#Draws the mountains and imported background 
def drawbackground():
	global x1mountain,y1mountain,x2mountain,y2mountain,x3mountain,y3mountain,background1
	screen.create_image(300,400,image=background1)

	#Created the mountains and the snow on top of each mountain according to the inital mountain cordiantes and modified each one so its in the right position
	screen.create_polygon(x1mountain-200,y1mountain,x2mountain-200,y2mountain,x3mountain-200,y3mountain,fill="peru",outline="brown")
	screen.create_polygon(x1mountain-148,y1mountain-100,x2mountain-200,y2mountain,x3mountain-252,y3mountain-100,fill="white")
	screen.create_polygon(x1mountain,y1mountain,x2mountain,y2mountain,x3mountain,y3mountain,fill="peru",outline="brown")
	screen.create_polygon(x1mountain-120,y1mountain,x2mountain-100,y2mountain-50,x3mountain-80,y3mountain,fill="peru",outline="brown")
	screen.create_polygon(x1mountain+200,y1mountain,x2mountain+200,y2mountain,x3mountain+200,y3mountain,fill="peru",outline="brown")
	screen.create_polygon(x1mountain+80,y1mountain,x2mountain+100,y2mountain-50,x3mountain+120,y3mountain,fill="peru",outline="brown")
	screen.create_polygon(x1mountain-45,y1mountain-150,x2mountain-100,y2mountain-50,x3mountain-155,y3mountain-150,fill="white")
	screen.create_polygon(x1mountain+53,y1mountain-100,x2mountain,y2mountain,x3mountain-53,y3mountain-100,fill="white")
	screen.create_polygon(x1mountain+155,y1mountain-150,x2mountain+100,y2mountain-50,x3mountain+45,y3mountain-150,fill="white")
	screen.create_polygon(x1mountain+253,y1mountain-100,x2mountain+200,y2mountain,x3mountain+147,y3mountain-100,fill="white")
	screen.create_polygon(x1mountain-320,y1mountain,x2mountain-300,y2mountain-50,x3mountain-280,y3mountain,fill="peru",outline="brown")
	screen.create_polygon(x1mountain+280,y1mountain,x2mountain+300,y2mountain-50,x3mountain+320,y3mountain,fill="peru",outline="brown")
	screen.create_polygon(x1mountain-245,y1mountain-150,x2mountain-300,y2mountain-50,x3mountain-355,y3mountain-150,fill="white")
	screen.create_polygon(x1mountain+355,y1mountain-150,x2mountain+300,y2mountain-50,x3mountain+345,y3mountain-150,fill="white")

#Fills in the eampty arrays for the cloud
def spawncloud():
	for i in range(numcloud):
		xcloud.append(randint(-50,650))
		ycloud.append(randint(-50,10))
		sizecloud.append(randint(80,100))

#Draws a set number of clouds (stated in setInitalValues), each one with different cordinates and size
def drawcloud():
	global xcloud,ycloud,sizecloud,numcloud
	for i in range(numcloud):
		screen.create_oval(xcloud[i],ycloud[i],xcloud[i]+sizecloud[i],ycloud[i]+sizecloud[i],fill="white",outline="")

#Draws snow falling from the top of the screen
def drawsnow():
	global xsnow,ysnow,snowsize,snow,snowspeedy,snowspeedx	

	#Creates the snow particles and changes their x and y cordinates so they move
	for i in range(len(snow)):
		screen.create_oval(xsnow[i],ysnow[i],xsnow[i]+snowsize[i],ysnow[i]+snowsize[i],fill="ghostwhite",outline="")
		ysnow[i]=ysnow[i]+snowspeedy[i]
		xsnow[i]=xsnow[i]+snowspeedx[i]

		# Checks if snow particle goes off screen and makes it respawn on top with new cordinates
		if ysnow[i]>800:
			xsnow[i]=randint(0,700)
			ysnow[i]=randint(-50,0)
			snowsize[i]=randint(5,10)
			snowspeedy[i]=uniform(1,8)
			snowspeedx[i]=uniform(-2,0)

#Prints the score on the top of the screen and the score multiplier (achieved by shooting a gold bird)
def scoreupdate():
	global score,scoreadder,scoremultiplier,roundedscore

	#When score surpasses one million, its outputed as 1m, 1.2m etc... so it doesn't take up the whole upper part of the screen
	if score>=1000000:
		score=score+scoreadder*scoremultiplier
		roundedscore = round(score/1000000,1)
		screen.create_text(300,50,text=str(roundedscore)+"m",font='Arial 35 bold',fill="gold")
		
	#Does it normally if score isn't over a million (score increases by 5 every frame but can be changed according to the score multiplier)
	else:	
		screen.create_text(300,50,text=score,font='Arial 35 bold',fill="gold")
		score=score+scoreadder*scoremultiplier

	#Outputs the score multiplier on the top left of the screen 
	screen.create_text(90,20,text="SCORE MULTIPLIER",font="Arial 10 bold",fill="gold")
	screen.create_text(90,50,text=str(scoremultiplier)+"X",font="Arial 25 bold",fill="gold")

#Checks if you beat your previous high score
def highscorefinder():
	global score,highscore
	
	if score>max(highscore):
		highscore.append(score)
			
	#Saves the updated high score to highscore.csv
	np.savetxt("highscore.csv",highscore,delimiter=",")

#Draws the amount of bullets you have on the top right of the screen
def drawbullets():
	global amountbullets,bulletimage,bulletdrawx,bulletdrawy,xchangebullet
	
	for i in range(amountbullets):
		
		#draws bullets according to the number of bullets you have, using xchange so the second and third bullet spawn next to the first one and not on top of it
		if i ==0:
			screen.create_image(bulletdrawx,bulletdrawy,image=bulletimage)
		if i ==1:
			screen.create_image(bulletdrawx+xchangebullet,bulletdrawy,image=bulletimage)
		if i ==2:
			screen.create_image(bulletdrawx+xchangebullet*2,bulletdrawy,image=bulletimage)

#Checks if any keys are pressed
def keyDownHandler( event ):
	global bulletXspeed,planeY,bulletY,amountbullets

	#Changes plane y cordinate (increasing it to go down, decreasing it to go up)
	if event.keysym=="Up":
		planeY=planeY-15

	elif event.keysym=="Down":
		planeY=planeY+15

	#If space is clicked and the player has 1 or more bullets it runs the spawnbullet function
	elif event.keysym=="space" and amountbullets >0:
		spawnbullet()
		amountbullets=amountbullets-1

#Fills in empty arrays for the bullet
def spawnbullet():
	global bullets, bulletY,bulletX
	
	bulletY.append(planeY)
	bulletX.append(100)
	bullets.append(0)

#Spanws a set number of birds accordinf to framecounter, making it harder as more frames pass 
def numbird():
	global framecounter,birdmultiplier,num

	#This makes the game progressively harder as frames pass, I capped out the difficulty to 7.5 as anything beyond that is impossible/ not humanly possible
	if framecounter %100 == 0 and num>7.4:
		num=num-0.5
		birdmultiplier=birdmultiplier+1

	if framecounter>=(num*birdmultiplier):
		spawnbird()
		birdmultiplier=birdmultiplier+1

#Fills in empty arrays for the birds flying towards the player 
def spawnbird():
	global birdY,birdtype,birdspeed
	
	birdY=randint(90,780)
	birdtype=determinebird()
	birdspeed=uniform(6,18)
	
	#Appends everything needed to draw a bird, sets fram to 0
	birds.append({"x":600,"y":birdY,"type":birdtype,"frame":0,"speed":birdspeed})

#Determines which colour bird to draw
def determinebird():
	global spawnodd
	
	#Creates a spawnodd variable to get a random number from 1 to 100 everytime it draws a bird
	spawnodd=randint(1,100)
	#70% of the bird being grey
	if 0<spawnodd<=70:
		return "grey"
	#10% chance of the bird being red
	if 70<spawnodd<=80:
		return "red"
	#17% chance of the bird being green
	if 80<spawnodd<=97:
		return "green"
	#3% chance of the bird being gold
	if 97<spawnodd<=100:
		return "gold"

#Bird movement
def updatebird():
	global birds
	
	#Updates each indivual bird to move to the left at different speeds
	for bird in birds:
		bird["x"]=bird["x"]-bird["speed"]

#Plane movement
def updateplane():
	global planeY,planespeed
	
	planeY=planeY+planespeed

#Creates a moving bullet 
def updatebullet():
	global bullets,bulletX,bulletY,bulletXspeed
	
	for i in range(0,len(bulletX)):
		bulletX[i]=bulletX[i]+bulletXspeed
	#Runs the deleteoffscreen function to check if the bullet missed and needs to be deleted	
	deleteoffscreen()

def deleteoffscreen():

	#Checks if the bullet goes off the screen and deletes it 
	i=0
	while i <len(bulletX)-1:
		if bulletX[i] >600:
			bulletX.pop(i)
			bulletY.pop(i)
			bullets.pop(i)
		else:
			i=i+1

	#Checks if bird goes off the screen and deletes it 
	m=0
	while m  <len(birds)-1:
		if birds[m]["x"]<0:
			birds.pop(m)

		else:
			m=m+1

#Draws the plane
def drawplane():
	global plane,planeX,planeY,planei,planespeed
	
	planei=screen.create_image(planeX,planeY+planespeed, image=plane)

#Draws an infinite number of birds (at a set spawn rate) until the player dies
def drawbird():
	global birds,bird_frames,birdX
	
	for bird in birds:
		birdTYPE=bird["type"]
		birdFRAME=bird["frame"]
		birdDRAWN=bird_frames[birdTYPE][birdFRAME]
		
		#Switches betwwen frame 0 and 1 so the bird looks like its flying
		bird["frame"]=(birdFRAME +1) % len(bird_frames[birdTYPE])
		screen.create_image(bird["x"],bird["y"],image=birdDRAWN)

#Draws bullet
def drawbullet():
	for i in range(0,len(bulletX)):
		bullets[i]=screen.create_rectangle(bulletX[i]+20,bulletY[i]+10,bulletX[i]+40,bulletY[i]+20,fill="yellow",outline="")
		
#Deletes bullet
def deletebullet():
	for i in range(0,len(bulletX)):
		screen.delete(bullets[i])

#Checks for any collisions
def checkforcollisions():
	global planeX,planeY,birds,dead,bulletX,bulletY,bullets,planespeed,birdTYPE,score,amountbullets,scoremultiplier

	#So the player cant make the plane leave the screen
	if planeY >= 800:
		planeY=770
	if planeY<=90:
		planeY=110

	#Checks if a bird hits the plane and sets dead to true
	for bird in birds:
		birdX=bird["x"]
		birdY=bird["y"]

		if planeX<birdX<planeX+40 and planeY-40<birdY<planeY+40:
			dead="true"
			break

	#Checks if bullet hits a bird
	i=0
	while i <len(bulletX):
		for bird in birds:
			birdX=bird["x"]
			birdY=bird["y"]
			birdTYPE=bird["type"]

			#Deletes both the bullet and the bird
			if birdX-30<bulletX[i]<birdX+20 and birdY-40<bulletY[i]<birdY+40:
				screen.delete(bullets[i])
				bulletX.pop(i)
				bulletY.pop(i)
				bullets.pop(i)
				birds.remove(bird)

				#Powerups are activated if differet colour birds are shot (no powerups if grey is shot)
				if birdTYPE=="red":
					score=score+5000

				if birdTYPE=="gold":
					scoremultiplier=scoremultiplier*2

				if birdTYPE=="green":
					amountbullets=3

				break

		i=i+1


def endscreen():
	global score,highscore

	screen.create_image(300,400,image=background1)

	
	#Output if score is greater than 1 million
	if score>=1000000:
		roundedscore=round(score/1000000,1)
		screen.create_text(300,200,text="Your Score:"+str(roundedscore)+"m",font='Arial 20 bold',fill="gold")
	else:
			#Output if score is less than 1 million
			screen.create_text(300,200,text="Your Score:"+str(score),font='Arial 20 bold',fill="gold")

	#Output if highscore is greater than 1 million
	if highscore[-1]>=1000000:
		roundedhighscore=round(highscore[-1]/1000000,1)
		screen.create_text(300,300,text="Global High Score:"+str(roundedhighscore)+"m",font='Arial 20 bold',fill="black")
	
	else:
		#Output if highscore is less than 1 million
		screen.create_text(300,300,text="Global High Score:"+str(int(highscore[-1])),font='Arial 20 bold',fill="black")

	screen.create_text(300,100,text="You crashed!",font="Arial 30 bold",fill="black")

	#Play again and quit buttons
	screen.create_rectangle(75,400,275,500,fill="gold",width=5,outline="orange")
	screen.create_rectangle(325,400,525,500,fill="gold",width=5,outline="orange")

	screen.create_text(175,450,text="Play Again",font="Arial 22 bold",fill="navy")
	screen.create_text(425,450,text="Quit",font="Arial 22 bold",fill="navy")

def runGame():
	global dead,framecounter,introscreen,running,runGAME,controlscreen,highscore

	setInitialValues() 
	spawncloud()

	while introscreen=="true":
		introscreencreate()
		screen.update()
	
		while controlscreen=="true":
			controlscreencreate()
			screen.update()
		
		while birdscreen=="true":
			birdscreencreate()
			screen.update()
		
	if dead=="false":
		while running=="true":
			drawbackground()
			drawsnow()
			drawcloud()
			drawbullets()
			scoreupdate()
			updateplane()  
			updatebullet()
			numbird()
			updatebird()
			drawplane()
			drawbullet()
			drawbird()
			checkforcollisions()
			screen.update()
			sleep(0.05)
			screen.delete("all")
			deletebullet()
			framecounter=framecounter+1	

			#If player dies it runs the endscreen function and the highscorefinder function to see if they beat their old highscore
			if dead =="true":
				highscorefinder()
				endscreen()
				break
			
#Call the runGame function
root.after( 0, runGame )

#Connecting user inputs to functions
screen.bind( "<Button-1>", mouseClickHandler )
screen.bind( "<Key>", keyDownHandler )

screen.pack()
screen.focus_set()
root.mainloop()