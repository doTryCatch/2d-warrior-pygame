import pygame
import time
from Game_Char_Copy import *
from slidable_block import *
from RealObject import *


class Playr:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 2
        self.force = 3
        self.max_jump_height = 250
        self.max_height_reach = False
        self.collide = False
        self.running_mode = False
        self.width = 30
        self.height = 30

    def move(self, keys):
        self.running_mode = keys[pygame.K_LSHIFT] * keys[pygame.K_d]
        if self.y < SCREEN_HEIGHT - 100:
            self.collide = False
            if self.max_height_reach:
                self.gravity = 0.1
        else:
            self.collide = True
            self.force = 2.7
            self.max_height_reach = False

        self.gravity = 0 if self.collide else 0.4
        self.y += self.gravity
        
        if keys[pygame.K_w] and not self.max_height_reach:
            self.force -= self.force * 0.01
            if self.force <= 0:
                self.max_height_reach = True
            self.y -= self.force if self.force > 0 else 0

        self.x += (keys[pygame.K_d] - keys[pygame.K_a]) * 0.7 if not self.running_mode else 1.5

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
hero_pos,tiles_arr,tiles,ladder,food,door,lift,boxes,inventory,others,Enmy=loadimages1('abc') 
tiles.append(slideBlock(100,280,100,20))
slide_block=slidableObject(200,0,90,80)


def level1(keys):
    running =True
    clock = pygame.time.Clock()
    FONT_SIZE = 20
    def load_conversation(file_name): 
        msg = []
        with open(file_name) as file:
            for line in file:
                msg.append(line)
        return msg

    def print_text(text, pos, speaker):
        font = pygame.font.Font(None, FONT_SIZE)
        text_surface = font.render(text, True, (0, 0, 0))  # Change to black (RGB values: 0, 0, 0)
        text_rect = text_surface.get_rect()

        padding = 10
        tail_offset = 20
        box_offset = 50

        if speaker == "player1":
            text_rect.topleft = (hero.x - tail_offset - text_rect.width, hero.y - text_rect.height - box_offset)
            tail_pos = (text_rect.right, text_rect.bottom)
            tail_end = (tail_pos[0] + tail_offset, tail_pos[1] + tail_offset)
        else:
            text_rect.topright = (hero.x + tail_offset + text_rect.width, hero.y - text_rect.height - box_offset)
            tail_pos = (text_rect.left, text_rect.bottom)
            tail_end = (tail_pos[0] - tail_offset, tail_pos[1] + tail_offset)

        background_rect = text_rect.inflate(padding, padding)
        
        pygame.draw.rect(screen, (245, 245, 220), background_rect)
        screen.blit(text_surface, text_rect)

        pygame.draw.polygon(screen, (245, 245, 220), [(tail_pos[0], tail_pos[1] - 5), 
                                            (tail_pos[0], tail_pos[1] + 5), 
                                            (tail_end[0], tail_end[1])])
    
    # print(Enmy,others)

    # enmy=enemy(Enmy[0]["x"],Enmy[0]["y"],60,90,"Assets/Enemy/troops") 

    def check_meet():
          index=0
          for all in msg:
            if pygame.Rect(hero.x, hero.y, hero.width, hero.height).colliderect(pygame.Rect(all["pos"].x, all["pos"].y, all["pos"].width, all["pos"].height)):
                return True,index
            index+=1
          return False,index

    ind=0
    def draw(object,killed,hero):
        for all in object:
           
                all.update(hero)
                all.draw(screen)
            # if keys[pygame.K_z]:
            #     all.img_coll=loadimages
                
            #     try:
            #         all.img_coll=pygame.transform.scale(all.img_coll,(100,100))
            #     except:
            #         for img in all.img_coll:
            #             img=pygame.transform.scale(img,(100,100))

               
    
                if killed:
                        all.x+=4 if hero.extra_dist_cover>=0 else -4
            

              

                

        
    ##background images setup
    bgimg=loadimages("Assets/Level1/1-1/Tile_0.png",(8000,600))
    bgimg2=loadimages("Assets/Level1/1-1/Background2.png",(8000,600))
    B1x=-50
    B2x=-50
    hero_Dim=(60,90)

    

    hero=Players(hero_pos[0]*hero_Dim[1],hero_Dim[0]*hero_pos[1],hero_Dim[0],hero_Dim[1],"Assets/Player",keys)
    hero2 = Playr(1500, SCREEN_HEIGHT - 100)
    hero3=Playr(1300, SCREEN_HEIGHT - 100)
    msg = [{"i":0,"msg":load_conversation("first_convo.txt"),"meet_status":False,"pos":hero3},{"i":0,"msg":load_conversation("second_convo.txt"),"meet_status":False,"pos":hero2}]
    turn = ""
    conversation = ""
    current_character = 0
    last_update_time = time.time()
    text_speed = 0.05
    collision=False
    down=False
    check_point=[200,500,700]
    bgx=-50
    killed=False
    state=""
    while running: 
        for event in pygame.event.get():
           
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not killed:
                  
                        
                        B1x+=hero.extra_dist_cover*0.5
                        B2x+=hero.extra_dist_cover*0.8
                        hero.y=100
                        
                       
                        
                        killed=True
                        
                    
                if event.key == pygame.K_RETURN and not msg[index-1]["meet_status"] and collision:
                    msg[index-1]["i"] += 1
                    turn = "player2" if turn == "player1" else "player1"
                    current_character = 0

         
        collision,index = check_meet()
      

        if msg[index-1]["i"] == len(msg[index-1]["msg"]) - 1:
           
            conversation = "finished"
            msg[index-1]["meet_status"]=True
          


        keys = pygame.key.get_pressed()

        
        mx,my=pygame.mouse.get_pos()

        
        if hero.screen_scroll:
          
         
            if not hero.slideableBlockCollision:
                B1x-=hero.char_speed*0.5
                B2x-=hero.char_speed*0.8
            else:
                if not hero.rest_state:
                    B1x-=0.5 if hero.char_speed>0 else -.5
                    B2x-=0.8 if hero.char_speed>0 else -.8
        else:
            B1x=-50
            B2x=-50
        # print(hero.char_speed)
        #Animalsw
      
        # print(B1x," ",hero.extra_dist_cover," ",B1x+hero.extra_dist_cover)
        screen.blit(bgimg2,(B1x,0))    #Background1
        screen.blit(bgimg,(B2x,0))   #Background2
        draw(tiles,killed,hero)

        draw(others,killed,hero)
    
        draw(ladder,killed,hero)
     
    
        if not killed:
            hero.draw(screen)   #Hero
        draw(food,killed,hero)
        if conversation != "left" and not killed:
            hero.moved(tiles,ladder,food,B1x,slide_block)
      
        hero2.draw(screen)
        hero3.draw(screen)
        slide_block.draw(screen)
        slide_block.update(tiles,hero)

        def Max(a,b):
            if b>a:
               
                return b,0
            return a,hero.extra_dist_cover
       
        for all in check_point:
            if (bgx-B1x)>=all:
                hero.scroll,hero.extra_dist_cover=Max(hero.scroll,all)
          

       
    
        if collision:
            conversation = "left"
            if turn == "":
                turn = "player1"
            if current_character < len(msg[index-1]["msg"][msg[index-1]["i"]]):
                if time.time() - last_update_time > text_speed:
                    current_character += 1
                    last_update_time = time.time()
            print_text(msg[index-1]["msg"][msg[index-1]["i"]][:current_character], (msg[index-1]["pos"].x, msg[index-1]["pos"].y - 50), "player1" if turn == "player1" else "player2")
            
        # pygame.draw.rect(screen, (255,0,0), (hero.x,hero.y,hero.width-20,hero.height),1)
        if killed:    
            ind+=4
            if abs(hero.extra_dist_cover)-ind<=0:
                killed=False
                hero.extra_dist_cover=0
                ind=0
            # killed=False    
            # hero.extra_dist_cover=0
        # print(ind," ",hero.extra_dist_cover," ",ind-hero.extra_dist_cover)      
              

        pygame.display.flip()

        clock.tick(165)  # limits FPS to 60
        # pygame.QUIT()
      
    
    
   
