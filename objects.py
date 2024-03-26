class objects:
    def __init__(self,x,y,w,h,img):
        self.x=x
        self.init_pos=(x,y)
        self.y=y
        self.width=w
        self.height=h
        self.index=0
        self.animation_time=30
        self.counter=0
        self.img_coll=img
    def update(self,hero):
        
        if hero.screen_scroll:
            if not hero.slideableBlockCollision:
                self.x-=hero.char_speed
            else:
                if not hero.rest_state:
                    self.x-=1 if hero.char_speed>0 else -1    
     
                
        
    def animation(self):
        if self.index!=len(self.img_coll)-1:
            self.index+=1 if self.counter==self.animation_time else 0
            if (self.counter>=self.animation_time):
                self.counter=0
        else:
            self.index=0
        self.counter+=1    
              
    def draw(self,screen):
            self.animation()
            screen.blit(self.img_coll[self.index],(self.x,self.y))
          


                                              





           
