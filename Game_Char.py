import pygame
from helper import *
import random
from pygame.locals import *

pygame.init()
font = pygame.font.SysFont("notomono", 30)

def check_collide(tiles, player, check_point):
    x = player.x
    y = player.y
    if check_point == "left":
        x = player.x - 5
    elif check_point == "right":
        x = player.x + 5
    elif check_point == "up":
        y = player.y - 10
    elif check_point == "down":
        y = player.y + 10
    for all in tiles:
        if pygame.Rect(x, y, player.width, player.height).colliderect(
            pygame.Rect(all[0], all[1], 45, 45)
        ):
            return True

    return False

########################################
class Players:
    def __init__(self, x, y, w, h, path):
        self.action="Idle"
        self.path=path
        self.x = x
        self.y = y
        self.flip=1
        self.speed=0.04
        self.char_speed=0
        self.max_speed=2
        self.gravity = 2
        self.force = 3
        self.max_jump_height = 250
        self.max_height_reach = False
        self.collide = False
        self.collide2 = False
        self.running_mode=False
        self.width=30
        self.height=30
        self.img_size=(w,h)
        self.img_coll=[]
        self.index=0
        self.animation_time=26
        self.counter=0
        self.counter2=0
        self.inc=1
        self.inventory=[]
        self.items=[]
        self.frame_num=8
        self.move=False
        for i in range(134,139):
            self.items.append(i)
##
##    def loadimages2(self, Action, direction, cnt):
##        self.img_coll=[]
##        for i in range(cnt):
##            self.img=pygame.transform.scale(pygame.image.load(f"{self.path}/{Action}/{Action}_{i}.png"),self.img_size)
##            self.img_coll.append(self.img)
    
    def animation(self):
        if self.index!=len(self.img_coll)-1:
            self.index+=1 if self.counter==self.animation_time else 0
            if (self.counter>=self.animation_time):
                self.counter=0
        else:
            self.index=0
        if self.action!="Idle":
            self.counter+=self.inc
        else:self.counter+=1 

    def getitem(self,x,y,tiles_arr,displaceX):
        kinput = pygame.key.get_pressed()
        user=pygame.Rect(x,y,45,90)
        for i in range(len(tiles_arr)):
            for j in range(len(tiles_arr[0])):
                if(int(tiles_arr[i][j]) in self.items):
                    collectible=Rect(j*45-displaceX,i*45,45,45)
                    collide = pygame.Rect.colliderect(user, collectible)
                    if(collide):
                        text = font.render("Press G to pick up item", False, (255,255,255))
                        screen.blit(text, (200,10))
                        if(kinput[pygame.K_g]):
                            tiles_arr[i][j]=196
                            self.inventory.append(1)

    def move(self, keys, collision, collision2, up_collision,displace):
        kinput = pygame.key.get_pressed()
        #write your movement code here
        self.collide=collision
        self.collide2=collision2
        self.action="Idle"
        if(keys[pygame.K_LSHIFT]):
            self.speed=0.04
            self.max_speed=2.2
            self.inc=2
        else:
            self.speed=0.03
            self.max_speed=1.5
            self.inc=1
        if (kinput[pygame.K_d]):
            self.action="Run"
            self.flip=1
            self.char_speed+=self.speed
        elif (kinput[pygame.K_a] and self.x>0):
            self.action="Run"
            self.flip=-1
            self.char_speed-=self.speed
        else:
            for i in range(0,4):
                if(self.char_speed<0):
                    self.char_speed+=0.01
                elif(self.char_speed>0):
                    self.char_speed-=0.01
        if(self.char_speed>self.max_speed):
            self.char_speed=self.max_speed
        elif(self.char_speed<-self.max_speed):
            self.char_speed=-self.max_speed

        if(kinput[pygame.K_w] and self.counter2<30 and up_collision==False):
##            self.action="Jump"
            self.gravity-=0.2
            self.counter2+=1
        elif(self.collide==False):
            self.gravity+=0.15
        else:
            self.gravity=0
            self.counter2=0
        if(self.collide==True):
            self.y-=1
                
        self.char_speed=float(format(self.char_speed,".2f"))
        if(self.x<350):
            self.x+=self.char_speed
            self.move=False
        else:
            self.move=True
       
           
        if(up_collision==True):
            self.gravity=0
            self.gravity+=0.5
        self.y+=self.gravity
        
        return(self.x,self.y,self.char_speed,self.move)

    def draw(self, screen):
       
        self.frame_num=6 if self.action=="Idle" else 8
            
        self.img_coll=loadimages2(self.path,self.action, self.img_size, self.frame_num)
        try:
            if(self.flip==1):
                screen.blit(self.img_coll[self.index],(self.x,self.y))
            else:
                screen.blit(pygame.transform.flip(self.img_coll[self.index],True,False),(self.x,self.y))
        except:
            self.index=0
        self.animation()

########################################

class enemy(Players):
    def __init__(self,x,y,w, h, path):
        super().__init__(x,y,w, h, path)
        self.roaming_range=1200
        self.initial_state=True
        self.final_state=False
        self.covered_range=0
        self.delay_time=80
        self.delay_count=0
        self.fight_range=False
        self.radius=200
        self.speed2=0.5
        self.attack_range=50
        self.attack_gap=70
        self.attack_gap_count=0
        self.scroll=0
    def draw_enemy(self,screen):
        pygame.draw.rect(screen,(255,0,0),(self.x,self.y,self.width,self.height))
        pygame.draw.circle(screen,(255,0,0),(self.x,self.y),self.radius,1)
    def go_for_attack(self,hero):
        distanceX=self.x-hero.x
        distanceY=self.y-hero.y
        if distanceX<0:
            distanceX=-distanceX
        if distanceY<0:
            distanceY=-distanceY    

        if distanceX>self.attack_range or distanceY>self.height:
           
            self.x+=self.speed2 if (self.x-hero.x)<0 else -self.speed2

            # self.y+=self.speed2 if (self.y-hero.y)<0 else -self.speed2
        else:
            
            disp=self.x+30 if(self.x-hero.x)<0 else self.x-30
            pygame.draw.rect(screen,(0,255,0),(disp,self.y,self.width,self.height))     
            if check_hit([hero],pygame.Rect(disp,self.y,self.width,self.height)):
            #    hero.hero_health-=5
               print("enemy hitted")    
    def movement(self,hero):
##        self.y+=self.gravity if self.y<SCREEN_HEIGHT-200 else 0
        if not self.fight_range:
           
            if self.initial_state:
                self.flip=1
                self.covered_range+=1
            if self.final_state:
                self.flip=-1
                self.covered_range-=1
            self.x+=self.speed2*self.flip

            
            if self.covered_range>=self.roaming_range:
                    if self.delay_count==self.delay_time:
                        self.final_state=True
                        self.initial_state=False
                        self.delay_count=0
                        self.delay_time=random.randint(200,500)
                    else:
                        self.final_state=False
                        self.initial_state=False
                        self.delay_count+=1
    
            if self.covered_range<=0:
                    if self.delay_count==self.delay_time:
                        self.final_state=False
                        self.initial_state=True
                        self.delay_count=0
                        self.delay_time=random.randint(200,500)
                        self.action="Idle"
                    else:
                        self.initial_state=False
                        self.final_state=False
                        self.delay_count+=1
                        self.action="Idle"
        if pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2).colliderect(pygame.Rect(hero.x,hero.y,hero.width,hero.height)):
            # print("collide")
            self.fight_range=True
            
        else:
            self.fight_range=False
        
        if self.scroll:
            self.x-=hero.char_speed
        #print(hero.collide)
            
            
        #print(self.x)    
