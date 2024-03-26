import pygame
import sys
import random
from helper import *
import math
# Initialize Pygame
pygame.init()
def puzzle():
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Set up the screen
    WIDTH, HEIGHT = 600, 600
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Number Puzzle")
    box_size=50
    frame_num=3
    class DraggablePiece:
        def __init__(self, posX,posY,x, y,size,index):
            self.x = x
            self.y=y
            self.posX=posX
            self.posY=posY
          
            self.dragging=False
            self.size=size
            self.actualIndex=index
            self.placedIndex=0
            self.rect=pygame.Rect(self.x+self.posX,self.y+self.posY,self.size,self.size)
            

        def draw(self):
           
            pygame.draw.rect(SCREEN, BLACK, self.rect)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(str(self.actualIndex), True, RED)
            text_rect = text_surface.get_rect(center=self.rect.center)
            SCREEN.blit(text_surface, text_rect)

        def update(self):
            if self.dragging:
                self.rect.center = pygame.mouse.get_pos()

   
    # Define constants
   
    # Define class for draggable pieces
    def check_repeat(arr,i,j):
        for all in arr:
              if(all["i"]==i and all["j"]==j):
                   return True
              
        return False 
    def random_indexContainig_array_generator(row,col,piece_num):
        arr=[]
        img_piece=[]
        while len(arr)!=piece_num:
            i=random.randint(0,row)
            j=random.randint(0,col)
            if len(arr)<=0:
                arr.append({"i":i,"j":j})
            else:
                if not check_repeat(arr,i,j):
                       
                    arr.append({"i":i,"j":j})
          
        return arr            
                             

              
    pos_arr=random_indexContainig_array_generator(3,9,9)  
    img_piece=[]
    posX=100
    posY=50
    for i,all in enumerate(pos_arr):
         img_piece.append(DraggablePiece(50,300,all["j"]*box_size,all["i"]*box_size,box_size,i))
         
         


         
   
 
    def draw_frame(posX,posY,size,frame_num):
        check=1
        for i in range(0,frame_num):
                for j in range(0,frame_num):
                    x,y=j*size,i*size
                    index=i*frame_num+j
                    if img_piece[index].placedIndex!=index:
                         check=0
                         
                         
                    pygame.draw.rect(screen,(0,0,0),(posX+x,posY+y,box_size,box_size),1) 
        return check            


    def draw_piece_container(posX,posY,size,arr):
        for i in range(0,4):
                for j in range(0,10):
                    x,y=j*size,i*size
                    pygame.draw.rect(screen,(0,0,0),(posX+x,posY+y,box_size,box_size),1)   
        for all in arr:
               
                all.draw()
                all.update()
                




                         
                         

    # Main game loop
   
    while True:
            SCREEN.fill(WHITE)

            
        

            # Check for events
            # screen.blit(img,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for piece in img_piece:
                        if piece.rect.collidepoint(event.pos):
                            piece.dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                        for piece in img_piece:
                            if piece.dragging:
                                piece.dragging = False
                                for i in range(0,frame_num):
                                    for j in range(0,frame_num):
                                        x,y=j*box_size,i*box_size
                                        rct=pygame.Rect(posX+x,posY+y,box_size,box_size)
                                      
                                        if piece.rect.colliderect(rct):
                                            dist=math.sqrt(math.pow((piece.rect.center[0]-rct.center[0]),2)+math.pow((piece.rect.center[1]-rct.center[1]),2))
                                         
                                            if dist<15:
                                                piece.rect.center=rct.center
                                                piece.placedIndex=i*frame_num+j 
                                               
                                               
                                       




                                       

                                            
                                        
            #draw frame
            
            win=draw_frame(100,50,box_size,3)
            draw_piece_container(50,300,box_size,img_piece)
           
            
            #check win 
            
                        
        

            pygame.display.flip()

puzzle()