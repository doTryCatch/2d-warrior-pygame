import random
import pygame
from helper import*
from pygame.locals import *
pygame.init()
font = pygame.font.SysFont("notomono", 30)

def check_collide(tiles, player, check_point):
    x = player.x
    y = player.y
    if check_point == "left":
        x = player.x - 4
    elif check_point == "right":
        x = player.x + 4
    elif check_point == "up": 

        y = player.y - 4
    elif check_point == "down":
        y = player.y + 4
    for all in tiles:
        if pygame.Rect(x+13, y, player.width-30, player.height-4).colliderect(
            pygame.Rect(all.x, all.y, all.width, all.height)
        ):
            return True
    if not check_point:
        for all in tiles:
            if pygame.Rect(x+20, y, player.width*0.3, player.height).colliderect(
                pygame.Rect(all.x+(all.width//2-0.15*all.width), all.y, 0.3*all.width, all.height)
            ):
                return True


    return False

########################################
class Players:
    def __init__(self, x, y, w, h, path,key):
        self.init_pos=(x,y)
        self.scroll=0
        self.key=key
        self.action = "Idle"
        self.path = path
        self.x = x
        self.y = y
        self.flip = 1
        self.G = 4
        self.max_force = 7
        self.char_speed = 0
        self.max_speed = 1
        self.gravity = 0
        self.force = 0
        self.max_jump_height = 250
        self.max_height_reach = False
        self.collide = False
        self.collide2 = False
        self.running_mode = False
        self.width = w
        self.height = h
        self.accleration=0
        self.cond=True
        self.img_size = (w, h)
        self.img_coll = []
        self.index = 0
        self.animation_time = 16
        self.counter = 0
        self.jump_height = 0
        self.inc = 1
        self.speedY=0
        self.inventory = []
        self.food = []
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.isLadder=False
        self.isFood=False
        self.climbing=False
        self.frame_num = 8
        self.screen_scroll=False
        self.ladder_collide = False
        self.move=True
        self.extra_dist_cover=0
        self.rest_state=False
        self.slideableBlockCollision=False
        for i in range(111, 131):
            self.food.append(i)

    def animation(self):
        if self.index != len(self.img_coll) - 1:
            self.index += 1 if self.counter == self.animation_time else 0
            if self.counter >= self.animation_time:
                self.counter = 0
        else:
            self.index = 0
        if self.action != "Idle":
            self.counter += self.inc
        else:
            self.counter += 1

   
    def moved(self, tiles, ladder,food,b1x,slide_block):
        # print(self.rest_state)
        self.right = check_collide(tiles, self, "right")
        self.left = check_collide(tiles, self, "left")
        self.up = check_collide(tiles, self, "up")
        self.down = check_collide(tiles, self, "down")
        self.isLadder=check_collide(ladder,self,"")
        self.isFood=check_collide(food,self,"")
        self.slideableBlockCollision=check_collide([tiles[-1]],self,"down")
        # print("right=",self.right," left=",self.left," up=",self.up," down=",self.down," ladder=",self.isLadder)
        # right= False  left= False  up= False  down= True  ladder= True
        if check_collide([slide_block],self,"right"):
            self.right=True
        elif check_collide([slide_block],self,"left"):
            self.left=True
        elif check_collide([slide_block],self,"down"):
            self.down=True    
       
        if not self.climbing:
            self.animation()
        if not self.isLadder:
            self.climbing=False    
        keys = pygame.key.get_pressed()

        self.running_mode = (
            keys[self.key["sprint"]] * keys[self.key["right_move"]]
            | keys[self.key["sprint"]] * keys[self.key["left_move"]]
        )
        if self.char_speed==0 :
            self.action="Idle"
      
    
        if self.down:
            self.force=self.max_force
            self.max_height_reach=False
            self.speedY=0
            self.gravity=0
        else:
            if not self.isLadder:
                self.gravity=self.G
          
        if keys[pygame.K_s] and self.isLadder:
            self.climbing=True
            self.animation()
            self.y+=.7

        if keys[self.key["jump"]]:
            
            if self.isLadder:
                self.climbing=True
                self.animation()
                self.action="Climb"
                self.gravity=0
                self.y-=.7
            
            else:
                self.action="Jump"
                self.force -=  0.03
                if self.force <= 0 or self.up:
                
                    self.max_height_reach = True
                
                    
                    
                if not self.max_height_reach :  
                
                    self.y-=self.force
       


        if keys[self.key["left_move"]] and not keys[self.key["right_move"]]:
            self.accleration, self.inc,self.max_speed = (0.15, 2,3) if keys[self.key["sprint"]] else (0.05, 1,2)

            # print(self.accleration)
            self.flip=-1
            if not self.isLadder:
                if keys[self.key["jump"]]:
                    self.action="Jump"    
                else:
                    self.action="Run"    
            if not self.left:
                    self.char_speed-=self.accleration if abs(self.char_speed)<=self.max_speed  else 0
            else:
                self.char_speed=0        
        elif keys[self.key["right_move"]] and not keys[self.key["left_move"]]:
            self.accleration, self.inc,self.max_speed = (0.3, 2,3) if keys[self.key["sprint"]] else (0.05, 1,2)

            self.flip=1
            if not self.isLadder:
                if keys[self.key["jump"]]:
                    self.action="Jump"    
                else:
                    self.action="Run"    
            if not self.right:
                self.char_speed+=self.accleration if self.char_speed<=self.max_speed  else 0       
            else:
                self.char_speed=0         
        else:
            
            if self.char_speed>0.1:
                self.char_speed-=self.accleration
            elif self.char_speed<-0.1:
                self.char_speed+=self.accleration
            else:
                self.char_speed=0     
              
        if keys[self.key["attack"]]:
            self.action="Attack"
            self.inc=2
        if self.isLadder and (not self.down or self.left and self.right or self.left and self.right and self.up  ) :
            self.action="Climb" 
       
    
       
            
            
        # if not (check_collide(arr,self,"left") or check_collide(arr,self,"right")) :
        
       
        self.y += self.gravity 
        if self.x<=2:
            self.left=False
        if not self.screen_scroll:
            if self.x<=2 and keys[self.key["left_move"]]:
                self.char_speed=0
               
                

            self.x +=self.char_speed
          
        
        if(self.x>300):
            self.screen_scroll=True
        if b1x>-50:
            self.screen_scroll=False
      
        self.extra_dist_cover+=self.char_speed    
             
           
        
          

   

    ##        print(self.char_speed)
    def movement(self,tiles,b1x,end):
        self.right = check_collide(tiles, self, "right")
        self.left = check_collide(tiles, self, "left")
        self.up = check_collide(tiles, self, "up")
        self.down = check_collide(tiles, self, "down")
        self.ladder_collide=check_collide(Ladder,self,"")
        
        keys = pygame.key.get_pressed()
        if not self.climbing:
            self.animation()
        if not self.ladder_collide:
            self.climbing=False
        if self.char_speed==0 and not keys[self.key["jump"]]:
            self.action="Idle"
        if(keys[self.key["sprint"]]):
            self.speed=0.05
            self.max_speed=3
            self.inc=2
        else:
            self.speed=0.03
            self.max_speed=2
            self.inc=1
        if (keys[self.key["right_move"]]):
            if not keys[self.key["jump"]]:
                self.action="Run"
                if self.char_speed<-0.15:
                    self.action="Slide"
                    self.inc=1
            self.flip=1
            self.char_speed+=self.speed
        elif (keys[self.key["left_move"]]):
            if not keys[self.key["jump"]]:
                self.action="Run"
                if self.char_speed>0.15:
                    self.action="Slide"
                    self.inc=1
            self.flip=-1
            self.char_speed-=self.speed
        else:
            for i in range(0,4):
                if(self.char_speed<0):
                    self.char_speed+=0.01
                elif(self.char_speed>0):
                    self.char_speed-=0.01
        if self.x<0:
            self.x=0
            self.char_speed=0
        elif self.x>745:
            self.x=745
            self.char_speed=0
        if(self.char_speed>self.max_speed):
            self.char_speed=self.max_speed
        elif(self.char_speed<-self.max_speed):
            self.char_speed=-self.max_speed
        if(keys[self.key["jump"]] and self.jump_height<24 and not self.up and not self.ladder_collide and self.cond==True):
##            print(self.ladder_collide)
            self.action="Jump"
            self.gravity-=0.4
            self.jump_height+=1
        elif(self.down):
            self.cond=True
        else:
            self.cond=False
        if (self.ladder_collide):
            self.climbing=True
            self.action="Climb"
            self.gravity=0
            acc=1
            if(keys[self.key["sprint"]]):
                acc=2
                self.inc=2
            if(keys[self.key["jump"]] or keys[pygame.K_s] or keys[self.key["left_move"]] or keys[self.key["right_move"]]):
                self.animation()
            if(keys[self.key["jump"]]):
                self.gravity=-0.7*acc
            elif(keys[pygame.K_s]):
                self.gravity=0.7*acc
        elif(not self.down):
            self.gravity+=0.15
        else:
            self.gravity=0
            self.jump_height=0
        if self.down:
            self.y-=1
                
        self.char_speed=float(format(self.char_speed,".2f"))
        if not self.down:
            if self.left:
                self.char_speed=0.1
            if self.right:
                self.char_speed=-0.1
        if(self.move==True):
            self.x+=self.char_speed
    
        
        if self.up:
            self.gravity=0.2
        self.y+=self.gravity
    ##        print(self.char_speed)
        if (keys[self.key["attack"]]):
            self.action="Attack"
            self.inc=2

        #Screen Scroll
        if(self.x>350):
            self.move=False
            self.screen_scroll=True
        if b1x>-50:
            self.move=True
            self.screen_scroll=False
        if b1x<-end:
            self.move=True
            self.screen_scroll=False
            if(self.x<350):
                self.x=350
                self.move=False
                self.screen_scroll=True
        if self.x<10:
            print("yes")
            self.move=False        
##        print(b1x)
        print(self.x)    

        
    def draw(self, screen):
        self.img_coll = loadimages2(self.path, self.action, self.img_size )
        try:
            if self.flip == 1:
                screen.blit(self.img_coll[self.index], (self.x, self.y))
            else:
                screen.blit(
                    pygame.transform.flip(self.img_coll[self.index], True, False),
                    (self.x, self.y),
                )
        except:
            self.index = 0

  
                       


########################################


class enemy(Players):
    def __init__(self, x, y, w, h, path):
        super()._init_(x, y, w, h, path)
        self.roaming_range = 1200
        self.initial_state = True
        self.final_state = False
        self.covered_range = 0
        self.delay_time = 80
        self.delay_count = 0
        self.fight_range = False
        self.radius = 400
        self.speed2 = 1
        self.attack_range = 50
        self.attack_gap = 70
        self.attack_gap_count = 0
        self.left_collide = True
        self.right_collide = True

    def draw_enemy(self, screen):
        ##        pygame.draw.rect(screen,(255,0,0),(self.x,self.y,self.width,self.height))
       
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius, 1)

    def check_hit(self, hero, enemy_rect):
        if pygame.Rect(hero.x, hero.y, hero.width, hero.height).colliderect(enemy_rect):
            return True
        return False

    def go_for_attack(self, hero):
        distanceX = self.x - hero.x
        distanceY = self.y - hero.y
        if distanceX < 0:
            distanceX = -distanceX
        if distanceY < 0:
            distanceY = -distanceY

        if distanceX > self.attack_range or distanceY > self.height:
            self.speed2 = 1.5
            if (self.x - hero.x) < 0:
                self.flip = 1
            else:
                self.flip = -1
            self.x += (
                self.speed2
                * self.flip
                * (not self.left_collide)
                * (not self.right_collide)
            )

            # self.y+=self.speed2 if (self.y-hero.y)<0 else -self.speed2
        else:
            self.action=""
            disp = self.x + 30 if (self.x - hero.x) < 0 else self.x - 30
            ##            pygame.draw.rect(screen,(0,255,0),(disp,self.y,self.width,self.height))
            if self.check_hit(hero, pygame.Rect(disp, self.y, self.width, self.height)):
                #    hero.hero_health-=5
                print("enemy hitted")

    def movement(self, hero, tiles):
        # print(hero.char_speed)
        
        if hero.screen_scroll:
           
           self.x-=hero.char_speed
        ##        print(self.left_collide, self.right_collide)
        self.right = check_collide(tiles, self, "right")
        self.left = check_collide(tiles, self, "left")
        self.up = check_collide(tiles, self, "up")
        self.down = check_collide(tiles, self, "down")
        self.y += self.G if not self.down else 0
        

        if self.right:
            self.x -= 1
            self.right_collide = True
            self.final_state = True
            self.initial_state = False
        elif self.left:
            self.x += 1
            self.left_collide = True
            self.initial_state = True
            self.final_state = False
        else:
            self.right_collide = False
            self.left_collide = False

        if not self.fight_range:
            if self.initial_state:
                self.flip = 1
                self.covered_range += 1
            if self.final_state:
                self.flip = -1
                self.covered_range -= 1

            self.x += (
                self.speed2
                * self.flip
                * (not self.left_collide)
                * (not self.right_collide)
            )

            if self.covered_range >= self.roaming_range:
                if self.delay_count == self.delay_time:
                    self.final_state = True
                    self.initial_state = False
                    self.delay_count = 0
                    self.delay_time = random.randint(200, 500)
                else:
                    self.final_state = False
                    self.initial_state = False
                    self.delay_count += 1

            if self.covered_range <= 0:
                if self.delay_count == self.delay_time:
                    self.final_state = False
                    self.initial_state = True
                    self.delay_count = 0
                    self.delay_time = random.randint(200, 500)
                    self.action = "Idle"
                else:
                    self.initial_state = False
                    self.final_state = False
                    self.delay_count += 1
                    self.action = "Idle"
        if pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        ).colliderect(pygame.Rect(hero.x, hero.y, hero.width, hero.height)):
            # print("collide")
            self.fight_range = True

        else:
            self.speed2 = 0.5
            self.fight_range = False
        if self.speed2 == 0.5:
            self.action = "Walk"
        elif self.speed2 == .7:
            self.action = "Run"
            
       
        # print(hero.collide)

        # print(self.x)
