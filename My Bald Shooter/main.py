import pygame
pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Aamirs Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

music = pygame.mixer.music.load("overtaken.mp3")
pygame.mixer.music.play(-1) #-1 continues playing it

score = 0

screenwidth = 500
screenheight = 500

class player(object):
    def __init__(self, x, y, width, height,):
        self.x = x
        self.y = y
        self.width = width #width and height of man will be 64 by by 64 as this is the same dimesnions of the sprite
        self.height = height
        self.vel = 7
        self.isjump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkcount = 0
        self.standing = True
        self.hitbox = (self.x +20, self.y +15, 28, 48)
        
    def draw(self, win):
        if self.walkcount + 1 >= 27:
            self.walkcount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkcount//3], (self.x, self.y))
                self.walkcount += 1
            elif self.right:
                win.blit(walkRight[self.walkcount//3], (self.x, self.y))
                self.walkcount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
      
        self.hitbox = (self.x +20, self.y +15, 28, 48)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2) # shows visible hit box for player 

    def hit(self):
        self.isjump = False
        self.jumpcount = 10
        self.x = 60
        self.y = 410
        self.walkcount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-5", 1, (255,0,0))
        win.blit(text, ((screenwidth/2) - (text.get_width()/2),200 ))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()

class projectile(object):
    def __init__(self,x,y,radius,colour,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 9 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)
        

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkcount = 0
        self.vel = 4
        self.path = [self.x, self.end]
        self.hitbox = (self.x +17, self.y + 2, 31, 57)
        self.health = 10
        self.alive = True

    
    def draw(self, win):
        self.move()
        if self.alive:
            if self.walkcount + 1 >= 33:
                self.walkcount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkcount //3], (self.x, self.y))
                self.walkcount += 1
            else: 
                win.blit(self.walkLeft[self.walkcount //3], (self.x, self.y))
                self.walkcount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 -self.health)), 10))
            self.hitbox = (self.x +17, self.y + 2, 31, 57)
                #pygame.draw.rect(win, (255,0,0), self.hitbox,2) #code to show the hitbox
                

    
    def move(self):
        if self.vel > 0 :
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

        
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.alive = False
        print("ouch")
        




def redrawgamewindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (251,252,252))
    win.blit(text, (370, 10))
    man.draw(win)
    yoda.draw(win)
    for bullet in bullets:
        bullet.draw(win)
  
    pygame.display.update()


#Main loop
font = pygame.font.SysFont('Arial', 32, True)
win_font = pygame.font.SysFont("Times New Roman", 100, True)
man = player(200, 410, 64, 64)
yoda = enemy(50,410,64,64, 450)
shootloop = 0
bullets = []
running = True
game_finished = False
while running:
    clock.tick(27) #set the the fps at 27 as it is the same number of sprites ]

    if yoda.alive == True:
        if man.hitbox[1] < yoda.hitbox[1] + yoda.hitbox[3] and man.hitbox[1] + man.hitbox[3] > yoda.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > yoda.hitbox[0] and  man.hitbox[0] < yoda.hitbox[0] + yoda.hitbox[2]:
                    man.hit()
                    score -= 5
    else:
        game_finished = True
        
    if game_finished:
        win_text = win_font.render("You Win ;)", 1, (46,204,113) )
        win.blit(win_text, (screenwidth//2 - win_text.get_width()//2, screenheight//2 - win_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False # Exits the game after winning 
            
    
    else:
    
        if shootloop > 0:
            shootloop +=1
        if shootloop > 3:
            shootloop = 0

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for bullet in bullets:
            if bullet.y - bullet.radius <yoda.hitbox[1] + yoda.hitbox[3] and bullet.y + + bullet.radius > yoda.hitbox[1]:
                if bullet.x + bullet.radius > yoda.hitbox[0] and bullet.x - bullet.radius < yoda.hitbox[0] + yoda.hitbox[2]:
                    yoda.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
            
            
            if bullet.x < 500 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shootloop == 0:
            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 3:
                bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 5, (169,169,169), facing))
            
            shootloop = 1

        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < screenwidth - man.width: #minusing width as the coordinate for sqaure is assigneed to top left of shape 
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkcount = 0

        if not(man.isjump):
            if keys[pygame.K_UP]:
                man.isjump = True
                man.right = False
                man.left = False
                man.walkcount = 0
        else:
            if man.jumpcount >= -10:
                neg = 1
                if man.jumpcount < 0:
                    neg = -1
                man.y -= (man.jumpcount ** 2) * 0.5 * neg
                man.jumpcount -= 1
            
            else:
                man.isjump = False
                man.jumpcount = 10

            
        redrawgamewindow()

pygame.quit()