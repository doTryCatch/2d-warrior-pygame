import pygame
import os
import sys,csv
from  objects import *
from RealObject import *
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tiles_dimension=(45,45)
enemy_size=(60,90)
img_arr=[]
tiles=[]
Ladder=[]
Food=[]
Door=[]
Lift=[]
Boxes=[]
Inventory=[]
Danger=[]
Rest=[]
Floor=[]
Enemy=[]
Pushable=[]


def loadimages(path,tiles_dimension):
    img=pygame.image.load(path)
    img=pygame.transform.scale(img,tiles_dimension)
    return img




def load(index,range_i,array,img,dim):
    if img:
        if(210<index<=220):
            array.append((dim[0]*tiles_dimension[0],dim[1]*tiles_dimension[1],tiles_dimension[0],tiles_dimension[1],img))

        if(range_i[0]<=index<=range_i[1]):
            array.append(objects(dim[0]*tiles_dimension[0],dim[1]*tiles_dimension[1],tiles_dimension[0],tiles_dimension[1],img)) 
        return array        
    else:
        if(range_i[0]<=index<=range_i[1]):
            array.append({"x":dim[0]*tiles_dimension[0],"y":dim[1]*tiles_dimension[1]})
              
        return array   



def loadimages1(path):
    with open("Level11.csv") as file: 
        data = csv.reader(file)
        for all in data:
            tiles.append(all)
    hero_pos=()
    for i in range(len(tiles)):
       for j in range(len(tiles[0])):
            img=[]
            try:
                index=int(tiles[i][j])
                if(0<index<=100):
                    img.append(loadimages(f"Assets/Level1/1-1/Tile_{index}.png",tiles_dimension))
                    load(index,(0,100),Floor,img,(j,i))
                elif (100<index<=450):
                    try:
                        img.append(loadimages(f"Assets/Level1/1-1/Extras/Tile_{index}.png",tiles_dimension))
                    except:    
                        for k in range(find_file_length(f"Assets/Level1/1-1/Extras/Tile_{index}")):
                            img.append(loadimages(f"Assets/Level1/1-1/Extras/Tile_{index}/{k+1}.png",tiles_dimension))
                        
                    load(index,(101,110),Ladder,img,(j,i))
                    load(index,(111,130),Food,img,(j,i))
                    load(index,(131,140),Door,img,(j,i))
                    load(index,(141,170),Lift,img,(j,i))
                    load(index,(171,170),Boxes,img,(j,i))
                    load(index,(181,170),Inventory,img,(j,i))
                    load(index,(300,450),Rest,img,(j,i))
                    load(index,(211,220),Pushable,img,(j,i))
                  

                elif(index==0):
                    hero_pos=(j,i)
                
                else:
                    load(index,(451,460),Enemy,'',(j,i))    
            except:
                img.append(pygame.image.load("Assets/Empty.png"))
            
    tiles[0][0]='-1'           
    return hero_pos,tiles,Floor, Ladder, Food, Door, Lift, Boxes, Inventory, Rest ,Enemy      





def find_file_length(path):
    directory_path = '/home/one/Downloads/Pygame/'+path
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return  len(files)

   


def loadimages2(path, Action, img_size):
    img_coll=[]
    len=find_file_length(f"{path}/{Action}")
  

    for i in range(len):
        img=pygame.transform.scale(pygame.image.load(f"{path}/{Action}/{Action}_{i}.png"),img_size)
        img_coll.append(img)
    return img_coll
            
def hover(array_of_setof_button_in_rect_form_with_pos):
        mouse_pos = pygame.mouse.get_pos()
        for img, position in array_of_setof_button_in_rect_form_with_pos:
            rect=img.get_rect(center=position)
            if rect.collidepoint(mouse_pos):
                # Adjust button's position and size for hover effect
                hovered_rect = pygame.Rect(
                    rect.left - 10,  # Move slightly left
                    rect.top - 10 ,   # Move upwards
                    rect.width + 15 , # Increase width
                    rect.height + 15 # Increase height
                )
                hovered_image = pygame.transform.scale(img, (hovered_rect.width, hovered_rect.height))
                screen.blit(hovered_image, hovered_rect)
            else:
                # Draw button without hover effect
                screen.blit(img, rect)    
def draw_rect( color,dimension):
    pygame.draw.rect(screen,color,dimension)
def Rect(img,pos):
    rect=img.get_rect(center=pos)
    return rect  
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
def blur_image(surface, radius):
    # Create a blurred copy of the surface using the average blur algorithm
    blurred_surface = pygame.transform.smoothscale(surface, (surface.get_width() // radius, surface.get_height() // radius))
    blurred_surface = pygame.transform.smoothscale(blurred_surface, (surface.get_width(), surface.get_height()))
    return blurred_surface  
def set_image(img,img_size): 
      Image = pygame.image.load(img) 
      Image = pygame.transform.scale(Image,img_size) if img_size else Image
      return Image




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
        if pygame.Rect(x, y, player.width, player.height).colliderect(
            pygame.Rect(all.x, all.y, all.width, all.height)
        ):
            return True

    return False

