import pygame,random,math,time
pygame.init()
_images ={}
ping_effect = pygame.mixer.Sound("ping.wav")
pygame.mixer.music.load('c418_cat.mp3')

pygame.mixer.music.play(-1)

def GetImage(path):  #Efficiently get images
        result = _images.get(path)
        if result == None:
            result = pygame.image.load(path).convert()
            _images[path]=result
        return result


class rock(pygame.sprite.Sprite):
    def __init__(self,colour,size= None):
        super().__init__()

        self._gravity = 5000
        self._colour = colour
        if size == None:
            self._size = random.randint(xpixel_internal//130,xpixel_internal//100)
        else:
            self._size = size

        self.image = pygame.Surface((self._size,self._size)).convert()
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
            self.rect.x = random.randint(0,xpixel_internal)
            self.rect.y = 0
        elif loc == 2:
            self.rect.y = random.randint(0,ypixel_internal)
            self.rect.x = 0
        elif loc == 3:
            self.rect.x = random.randint(0,xpixel_internal)
            self.rect.y = ypixel_internal
        else:
            self.rect.y = random.randint(0,ypixel_internal)
            self.rect.x = xpixel_internal
        
            

        self._vector = [random.randint(-self._speed,self._speed),random.randint(-self._speed,self._speed)]

    def update(self,Guy):
        
        self._vector[0]+= (Guy.rect.x-self.rect.x)/self._gravity
        self._vector[1]+= (Guy.rect.y-self.rect.y)/self._gravity
        self.rect.x += self._vector[0]+Guy._vector[0]
        self.rect.y += self._vector[1]+Guy._vector[1]
       
        
        
class player(rock):
    def GetFace(self):
        self.image = pygame.transform.scale(GetImage("catface.png"),(xpixel_internal//20,math.ceil(xpixel_internal//20*1.2)))
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
        self.rect.x= math.floor(xpixel_internal/2)
        self.rect.y= math.floor(ypixel_internal/2)
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
        if pressed()[pygame.K_SPACE]:
            self._vector =[int(self._vector[0]/1.05),int(self._vector[1]/1.05)]
            self.UpFlame()
            self.DownFlame()
            self.LeftFlame()
            self.RightFlame()
            

class laser(rock):
    def __init__(self,vector,Guy):
        self._colour = (255,0,255)
        super().__init__(self._colour)
        self._age = 0
        self._vector = vector
        self.rect.x,self.rect.y = Guy.rect.center
    def update(self,Guy):
        
        if self._age >180 or self.rect.x >xpixel_internal or self.rect.x <0 or self.rect.y > ypixel_internal or self.rect.y <0:
            self.kill()
        self.rect.x += self._vector[0]+Guy._vector[0]
        self.rect.y += self._vector[1]+Guy._vector[1]
        self._age+=1

    def reset(self):
        self._age =177
        self.image.fill((255,255,255))
        ping_effect.play()


performance_mode = True # If true doesnt use scaling, if false uses scaling

xpixel_internal = 1200
ypixel_internal = 700
gameDisplay = pygame.surface.Surface((xpixel_internal,ypixel_internal))
if performance_mode == True:
   xpixel = xpixel_internal
   ypixel = ypixel_internal
else:
    xpixel = 1920
    ypixel = 1080
gameDisplayScaled = pygame.display.set_mode((xpixel,ypixel))
pressed = pygame.key.get_pressed
working = True

while working:
    gameDisplay.fill((0,0,0))
    font = pygame.font.Font(None, 50)
    Return = font.render(("Press [RETURN] to start"),True,(255,255,255))
    gameDisplay.blit(Return,((xpixel_internal-Return.get_width())/2,(ypixel_internal)/2))
    if performance_mode == False:
        gameDisplayScaled.blit((pygame.transform.scale(gameDisplay,(xpixel,ypixel))),(0,0))
    else:
        gameDisplayScaled.blit(gameDisplay,(0,0))
    pygame.display.update()
    time.sleep(0.1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            working = False
        if pressed()[pygame.K_RETURN] == 1 or True:
            font = pygame.font.Font(None, 25)

            Rock_list = pygame.sprite.Group()
            Sprite_list = pygame.sprite.Group()

            for q in range(15):  #Add the sprites
                roc = rock((255,0,0))
                roc.reset()
                Rock_list.add(roc)
                Sprite_list.add(roc)
            Guy = player((0,255,255))
            Sprite_list.add(Guy)
            Guy.GetFace()


            Laser_List = pygame.sprite.Group()
            laser_speed = 5
            laser_time = 0.01

            clock = pygame.time.Clock()
            score = 0
            working = True
            Last_laser = time.time()
            Fired = False

            background = pygame.transform.scale(GetImage("space.png"),(xpixel_internal,ypixel_internal))
            start,timelast = time.time(),time.time()
            
            while Guy._health>0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        working = False
                    if pressed()[pygame.K_b] == 1:
                        print(clock.get_fps())
                if time.time() - Last_laser > laser_time:
                    tv=[0,0]
                    if pressed()[pygame.K_LEFT]:
                        tv[0]+=-laser_speed
                        Fired = True
                        
                    if pressed()[pygame.K_RIGHT]:
                        tv[0]+=laser_speed
                        Fired = True
                        
                    if pressed()[pygame.K_UP]:
                        tv[1]+= -laser_speed
                        Fired = True
                        
                    if pressed()[pygame.K_DOWN]:
                        tv[1]+= laser_speed
                        Fired = True
                        
                    if Fired:
                        TempLaser =laser([-Guy._vector[0]+tv[0],-Guy._vector[1]+tv[1]],Guy)
                        Laser_List.add(TempLaser)
                        Sprite_list.add(TempLaser)
                        Last_laser = time.time()
                        Fired = False
                        
                gameDisplay.fill((0,0,0))
                gameDisplay.blit(background,(0,0))
                rects = []
            ##    for item in Sprite_list:
            ##        rects.append(item.rect)
                DeltaTime = time.time()- timelast
                timelast = time.time()
                
                rects = Sprite_list.update(Guy)
                
                for item in Sprite_list:
            ##        rects.append(item.rect)
                    if item.rect.x > xpixel_internal or item.rect.x <0 or item.rect.y > ypixel_internal or item.rect.y < 0:
                        item.reset()
                hit_list = pygame.sprite.spritecollide(Guy,Rock_list,False)
                
                for item in hit_list:
                    if item.GetColour() == (0,255,0):
                            score +=1
                            Guy._health+=2
                    else:
                            #score -=1
                            Guy._health-=1
                    item.reset()

                for item in Laser_List:
                    temp = pygame.sprite.spritecollide(item,Rock_list,False)
                    if temp !=[]:
                        item.reset()
                        for item2 in temp:
                            item2.reset()
                            Guy._health +=3
                            score +=5
                    
                
                scoretext = font.render(("Score :"+str(score)+" | Health :"+str(Guy._health)+" Vector :(" +str(Guy._vector[0])+" "+str(Guy._vector[1])+")"),True,(255,255,255))
                gameDisplay.blit(scoretext,(2,2))
                Sprite_list.draw(gameDisplay)
                if performance_mode == False:
                    gameDisplayScaled.blit((pygame.transform.scale(gameDisplay,(xpixel,ypixel))),(0,0))
                else:
                    gameDisplayScaled.blit(gameDisplay,(0,0))
                pygame.display.update()#rects)
                
                clock.tick(60)
                
            end = time.time()
            font = pygame.font.Font(None, 60)
            gameover = font.render(("Game Over"),True,(255,255,255))
            font = pygame.font.Font(None, 40)
            scoretext = font.render(("Score:"+str(score)+" Time :"+str(int(end-start))+" seconds"),True,(255,255,255))
            gameDisplay.blit(scoretext,((xpixel_internal-scoretext.get_width())/2,(ypixel_internal)/2))
            gameDisplay.blit(gameover,((xpixel_internal-gameover.get_width())/2,(ypixel_internal-gameover.get_width())/2))
            gameDisplayScaled.blit((pygame.transform.scale(gameDisplay,(xpixel,ypixel))),(0,0))
            pygame.display.update()#rects)
            time.sleep(5)















