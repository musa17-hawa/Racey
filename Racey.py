import pygame
import time
import random
pygame.init()

# crash_sound = pygame.mixer.Sound("crash.wav")
# pygame.mixer.music.load("game.wav")
# intro_sound = pygame.mixer.Sound("intro.wav")

display_width = 800
display_height = 600
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0, 200, 0)
blue = (90, 100, 235)
grey = (95, 95, 95)
purple = (72, 6, 100)
bright_red = (255, 0, 100)
bright_green = (0, 255, 100)
light_blue = (10, 180, 255)

largetext = pygame.font.Font('FreeSerifBold.ttf', 48)
mdtext = pygame.font.Font('FreeSerifBold.ttf', 38)
mtext = pygame.font.Font('FreeSerifBold.ttf', 28)
smtext = pygame.font.Font('FreeSerifBold.ttf', 18)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Racey')
clock = pygame.time.Clock()
carImg = pygame.image.load('racecar.png')
car_width = 44
pygame.display.set_icon(carImg)

pause = False

def things_dodged(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("Dodged: "+str(count), True, red)
	gameDisplay.blit(text, (0,0))

def Quit():
	pygame.quit()
	quit()

def car (x,y):
	gameDisplay.blit(carImg,(x,y))

def things(xx,yy,ww,hh,cc):
	pygame.draw.rect(gameDisplay, cc, [xx, yy, ww, hh])

def text_objects(text, font):
	textsurface = font.render(text, True, red)
	return textsurface, textsurface.get_rect()

def text_default(text, font):
	textsurface = font.render(text, True, black)
	return textsurface, textsurface.get_rect()

def text_purple(text, font):
	textsurface = font.render(text, True, purple)
	return textsurface, textsurface.get_rect()

def text_intro(text, font):
	textsurface = font.render(text, True, blue)
	return textsurface, textsurface.get_rect()


def crash():
	# pygame.mixer.music.stop()
	# pygame.mixer.Sound.play(crash_sound)
	TextSurf, TextRect = text_objects("Game Over !", largetext)
	TextRect.center = ((display_width/2),(display_height/3))
	gameDisplay.blit(TextSurf, TextRect)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		button("Play Again!",150,400,110,50, green, bright_green, game_loop)
		button("Give Up!",550,400,110,50, blue, light_blue, Quit)

		pygame.display.update()
		clock.tick(15)

def button(msg, x, y, w, h, i, a, action = None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if (x+w > mouse[0] > x) and (y + h > mouse[1] > y):
		pygame.draw.rect(gameDisplay, a, (x,y,w,h))
		if click[0] == 1 and action != None:
			action()
			
	else:
		pygame.draw.rect(gameDisplay, i, (x,y,w,h))

	TextSurf, TextRect = text_purple(msg, smtext)
	TextRect.center = ((x+(w/2)), (y+(h/2)))
	gameDisplay.blit(TextSurf, TextRect)

def unpause():
	global pause
	# pygame.mixer.music.unpause()
	pause = False

def paused():
	# pygame.mixer.music.pause()
	TextSurf, TextRect = text_intro("Paused", largetext)
	TextRect.center = ((display_width/2),(display_height/3))
	gameDisplay.blit(TextSurf, TextRect)

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.K_d:
				unpause()
		button("Continue",150,400,90,50, green, bright_green, unpause)
		button("Restart",550,400,90,50, blue, light_blue, game_loop)

		pygame.display.update()
		clock.tick(15)
		


def game_intro():
	# pygame.mixer.music.stop()
	# pygame.mixer.Sound.play(intro_sound)
	intro = True
	gameDisplay.fill(black)
	TextSurf, TextRect = text_intro("Hello and Welcome to Racey !", largetext)
	TextRect.center = ((display_width/2),(display_height/3))
	gameDisplay.blit(TextSurf, TextRect)
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		button("Go!",150,400,90,50, green, bright_green, game_loop)
		button("Exit :(",550,400,90,50, red, bright_red, Quit)

		pygame.display.update()
		clock.tick(5)
		

def game_loop():
	pygame.mixer.music.play(-1)
	global pause
	x = (display_height * 0.65)
	y = (display_height * 0.83)

	x_change = 0
	start_x = random.randrange(0,display_width)
	start_y = -400
	thing_speed = 10
	move_speed = 1
	ww = 100
	hh = 100
	dodged = 0


	gameExit = False

	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -7+move_speed*-1
				if event.key == pygame.K_RIGHT:
					x_change = 7+move_speed*1
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
					pause = True
					paused()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0

		x+= x_change
		gameDisplay.fill(white)
		things(start_x, start_y, ww, hh, black)
		start_y+= thing_speed
		car(x,y)
		things_dodged(dodged)

		if x > display_width - car_width or x < 0:
			crash()
			gameExit = True
		if start_y > display_height:
			start_y = 0 - hh
			start_x = random.randrange(0, display_width)
			dodged += 1
			thing_speed += 0.3
			move_speed +=0.2
		if y < start_y+hh:
			if x > start_x and x < start_x+ww or x+car_width > start_x and x+car_width < start_x+ww: 
				crash()
		pygame.display.update()
		clock.tick(60)


game_intro()
game_loop()
Quit()