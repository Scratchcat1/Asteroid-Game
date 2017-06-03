import pygame,random,math,time
pygame.init()
_images ={}
def GetImage(path):  #Efficiently get images
        result = _images.get(path)
        if result == None:
            result = pygame.image.load(path).convert()
            _images[path]=result
        return result


class rock(pygame.sprite.Sprite):
    def __init__(self,colour):
        super().__init__()

        self._gravity = 5000
        self._colour = colour
        self._size = random.randint(5,10)

        self.image = pygame.Surface((self._size,self._size))
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self._health = 15
        self._speed = 1
        self._vector = [random.randint(-self._speed,self._speed),random.randint(-self._speed,self._speed)]


    def GetColour(self):
            return self._colour
    def reset(self):
        self._health = 3
        colour = random.randint(0,10)
        if colour == 0:
            self._colour = (0,255,0)
        else:
            self._colour = (255,0,0)
        self.image.fill(self._colour)
        loc = random.randint(0,4)
        if loc == 1:
            self.rect.x = random.randint(0,xpixel)
            self.rect.y = 0
        elif loc == 2:
            self.rect.y = random.randint(0,ypixel)
            self.rect.x = 0
        elif loc == 3:
            self.rect.x = random.randint(0,xpixel)
            self.rect.y = ypixel
        else:
            self.rect.y = random.randint(0,ypixel)
            self.rect.x = xpixel
        
            

        self._vector = [random.randint(-self._speed,self._speed),random.randint(-self._speed,self._speed)]

    def update(self,Guy):
        
        self._vector[0]+= (Guy.rect.x-self.rect.x)/self._gravity
        self._vector[1]+= (Guy.rect.y-self.rect.y)/self._gravity
        self.rect.x += self._vector[0]+Guy._vector[0]
        self.rect.y += self._vector[1]+Guy._vector[1]
       
        
        
class player(rock):
    def GetFace(self):
        self.image = pygame.transform.scale(GetImage("catface.png"),(40,50))
        self.rect = self.image.get_rect()
        self._accel = 0.5

    def DownFlame(self):
        pygame.draw.rect(gameDisplay,(0,255,0),(math.floor(self.rect.width/2)+self.rect.x-1,self.rect.bottom,random.randint(1,4),random.randint(10,30)))
    def LeftFlame(self):
        pygame.draw.rect(gameDisplay,(0,255,0),(self.rect.right,math.floor(self.rect.height/2)+self.rect.y-1,random.randint(10,30),random.randint(1,4)))
    def UpFlame(self):
        pygame.draw.rect(gameDisplay,(0,255,0),(math.floor(self.rect.width/2)+self.rect.x-1,self.rect.y,random.randint(1,4),-random.randint(10,30)))
    def RightFlame(self):
        pygame.draw.rect(gameDisplay,(0,255,0),(self.rect.x,math.floor(self.rect.height/2)+self.rect.y-1,-random.randint(10,30),random.randint(1,4)))

    def update(self,ran):
        #pos = pygame.mouse.get_pos()
        #elf.rect.x,self.rect.y = pos[0],pos[1]
        self.rect.x= math.floor(xpixel/2)
        self.rect.y= math.floor(ypixel/2)
        if pressed()[pygame.K_a]:
            self._vector[0] += self._accel
            self.LeftFlame()
        if pressed()[pygame.K_w]:
            self._vector[1] += self._accel
            self.DownFlame()
        if pressed()[pygame.K_s]:
            self._vector[1] -= self._accel
            self.UpFlame()
        if pressed()[pygame.K_d]:
            self._vector[0] -= self._accel
            self.RightFlame()
        if pressed()[pygame.K_b]:
            self._vector =[int(self._vector[0]/1.05),int(self._vector[1]/1.05)]
            self.UpFlame()
            self.DownFlame()
            self.LeftFlame()
            self.RightFlame()
            
xpixel = 1920
ypixel = 1000
gameDisplay = pygame.display.set_mode((xpixel,ypixel))

font = pygame.font.Font(None, 25)

Rock_list = pygame.sprite.Group()
Sprite_list = pygame.sprite.Group()

for q in range(25):  #Add the sprites
    roc = rock((255,0,0))
    roc.reset()
    Rock_list.add(roc)
    Sprite_list.add(roc)
Guy = player((0,255,255))
Sprite_list.add(Guy)
Guy.GetFace()





pressed = pygame.key.get_pressed
clock = pygame.time.Clock()
score = 0
working = True

background = pygame.transform.scale(GetImage("space.png"),(xpixel,ypixel))
start = time.time()
while Guy._health>0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            working = False
    gameDisplay.fill((0,0,0))
    gameDisplay.blit(background,(0,0))
    rects = []
##    for item in Sprite_list:
##        rects.append(item.rect)
    
    rects = Sprite_list.update(Guy)
    
    for item in Sprite_list:
##        rects.append(item.rect)
        if item.rect.x > xpixel or item.rect.x <0 or item.rect.y > ypixel or item.rect.y < 0:
            item.reset()
    hit_list = pygame.sprite.spritecollide(Guy,Rock_list,False)
    
    for item in hit_list:
        if item.GetColour() == (0,255,0):
                score +=1
                Guy._health+=1
        else:
                #score -=1
                Guy._health-=1
        item.reset()
         
    
    scoretext = font.render(("Score :"+str(score)+" Vector :("+str(Guy._vector[0])+" "+str(Guy._vector[1])+")"),True,(255,255,255))
    gameDisplay.blit(scoretext,(2,2))
    Sprite_list.draw(gameDisplay)
    
    pygame.display.update()#rects)
    
    clock.tick(60)
end = time.time()
font = pygame.font.Font(None, 60)
gameover = font.render(("Game Over"),True,(255,255,255))
font = pygame.font.Font(None, 40)
scoretext = font.render(("Score:"+str(score)+" Time :"+str(int(end-start))+" seconds"),True,(255,255,255))
gameDisplay.blit(scoretext,((xpixel-scoretext.get_width())/2,(ypixel)/2))
gameDisplay.blit(gameover,((xpixel-gameover.get_width())/2,(ypixel-gameover.get_width())/2))
pygame.display.update()















