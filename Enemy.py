
import random
from helper import Players,pygame,check_collide

########################################



class enemy(Players):
    def __init__(self, x, y, w, h, path):
        super().__init__(x, y, w, h, path)
        self.roaming_range = 1200
        self.initial_state = True
        self.final_state = False
        self.covered_range = 0
        self.delay_time = 80
        self.delay_count = 0
        self.fight_range = False
        self.radius = 200
        self.speed2 = 0.5
        self.attack_range = 50
        self.attack_gap = 70
        self.attack_gap_count = 0
        self.scroll = 0
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
            self.speed2 = 1
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
            disp = self.x + 30 if (self.x - hero.x) < 0 else self.x - 30
            ##            pygame.draw.rect(screen,(0,255,0),(disp,self.y,self.width,self.height))
            if self.check_hit(hero, pygame.Rect(disp, self.y, self.width, self.height)):
                #    hero.hero_health-=5
                print("enemy hitted")

    def movement(self, hero, tiles):
        ##        print(self.left_collide, self.right_collide)
        self.y += (
            self.gravity
            if not check_collide(
                tiles,
                self,
                "down",
            )
            else 0
        )

        if check_collide(
            tiles,
            self,
            "right",
        ):
            self.x -= 1
            self.right_collide = True
            self.final_state = True
            self.initial_state = False
        elif check_collide(
            tiles,
            self,
            "left",
        ):
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
        elif self.speed2 == 1:
            self.action = "Run"
        if self.scroll:
            self.x -= hero.char_speed
        # print(hero.collide)

        # print(self.x)
