
import pygame as pg
import sys
import random
import time


class Screen:
    def __init__(self, fn, wh, title):
        super().__init__()
        pg.display.set_caption(title)
        self.width, self.height = wh
        self.disp = pg.display.set_mode((self.width, self.height))
        self.rect=self.disp.get_rect()
        self.image = pg.image.load(fn)

class Bird(pg.sprite.Sprite):
    key_delta = {pg.K_UP   : [0, -5],       
             pg.K_DOWN : [0, +5],
             pg.K_LEFT : [-5, 0],
             pg.K_RIGHT: [+5, 0],}

    def __init__(self,fn,r,xy):
        super().__init__()
        self.image=pg.image.load(fn)
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect = self.image.get_rect()
        self.rect.center = xy

    def update(self, screen):
        
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key] == True:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]
                # 練習7
                if check_bound(screen.rect, self.rect) != (1,1): 
                    self.rect.centerx -= delta[0]
                    self.rect.centery -= delta[1]


class Bomb(pg.sprite.Sprite):
    def __init__(self,color, r, vxy, screen):
        super().__init__()
        self.image = pg.Surface((2*r, 2*r))
        self.image.set_colorkey((0,0,0))
        pg.draw.circle(self.image, color, (r,r), r)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, screen.rect.width)
        self.rect.centery = random.randint(0, screen.rect.height)
        self.vx, self.vy = vxy

    def update(self, screen):
        self.rect.move_ip(self.vx, self.vy)
        x, y = check_bound(screen.rect, self.rect)

        self.vx *= x 
        self.vy *= y 

class RelatedWall():
    def __init__(self):
        self.speed = 1.05
        self.conflict = 0
        self.font= pg.font.Font(None, 300)   
        self.conf_font =  pg.font.Font(None, 100)  

    def show_conflict(self,screen, bombs):
        for _ in bombs:
            x, y = check_bound(screen.rect, _.rect)
            if (x, y) != (1,1):
                self.conflict+=1

        text2 = self.conf_font.render(f"{self.conflict}/100conflicts", True, (255,255,255))
        screen.disp.blit(text2, [0,0])
    
        return self.conflict
        
    
    def GameOver(self,screen):
        text = self.font.render("GAME OVER", True, (255,0,0))
        screen.disp.blit(text, [400,200])
        pg.display.update()


    def speedup(self, screen, bombs):
        for _ in bombs:
            x, y = check_bound(screen.rect, _.rect)
            if (x, y) != (1,1):
                
                _.vx *= self.speed 
                _.vy *= self.speed 
                print(_.vx,_.vy)

class Negi(pg.sprite.Sprite): #C0B21168
    def __init__(self, fn, r, xy):
      
        super().__init__()
        self.image = pg.image.load(fn)    
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect= self.image.get_rect()  
        self.rect.center = xy
        

def main():
    NEGI = 0
    negi_list = [20,40,60,80]
    global conflict
    
    clock = pg.time.Clock()
    check_wall=RelatedWall()

    screen = Screen('fig/pg_bg.jpg',(1600,900), "逃げろ！こうかとん")

    screen.disp.blit(screen.image,(0,0)) 

    tori = pg.sprite.Group()
    tori.add(Bird("fig/3.png",2, (900,400))) 

    bombs = pg.sprite.Group()

    for _ in range(2):
        bombs.add(Bomb((255,0,0), 10, (+4,+4), screen))

    conflict = check_wall.show_conflict(screen, bombs)

    negi = pg.sprite.Group()

    while True:
        screen.disp.blit(screen.image, (0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT: return   

        if conflict == 100:
            text = font.render("Play again:push space button", True, (0,0,255))
            screen.disp.blit(text, [400,200])
            text2 = font.render("Quit:push enter", True, (0,0,255))
            screen.disp.blit(text2, [400,400])
            key_contenue_states = pg.key.get_pressed()
            if key_contenue_states[pg.K_SPACE]==True:
                pg.display.update()
                check_wall.conflict = 0
                conflict = 0
                continue
            elif key_contenue_states[pg.K_RETURN]==True:
                time.sleep(2)
                return
            pg.display.update()

        elif len(pg.sprite.groupcollide(tori, bombs, False, False)) !=0:
            text=font.render("Play again:push space button", True, (0,0,255))  
            text2 = font.render("Quit:push enter", True, (0,0,255))
            screen.disp.blit(text, [100,400])
            screen.disp.blit(text2, [100,500])
            check_wall.GameOver(screen)
            key_contenue_states = pg.key.get_pressed()
            if key_contenue_states[pg.K_SPACE]==True:
                pg.display.update()
                check_wall.conflict = 0
                conflict = 0
                return True
            elif key_contenue_states[pg.K_RETURN]==True:
                return False
        else:
            tori.update(screen)
            tori.draw(screen.disp)
            bombs.update(screen)
            bombs.draw(screen.disp)
            font= pg.font.Font(None, 100)  
            check_wall.speedup(screen, bombs)

            conflict = check_wall.show_conflict(screen, bombs)

        if check_wall.conflict == negi_list[0]: #C0B21168
            NEGI = 1 
            negi_list.pop(0)

        if NEGI == 1: #C0B21168
            negi.add(Negi("fig/negi.png", 0.1, (random.randint(0, 1600), random.randint(0, 400))))
            NEGI = 0

        for i in pg.sprite.groupcollide(negi, tori, False, False): #C0B21168
            negi.remove(i)
            NEGI = 0
            check_wall.conflict += 5
        negi.draw(screen.disp)
        pg.display.update()
        clock.tick(1000) 
    
def check_bound(sc_r, obj_r):
    x, y = +1, +1
    if obj_r.left < sc_r.left or sc_r.right  < obj_r.right : x = -1
    if obj_r.top  < sc_r.top  or sc_r.bottom < obj_r.bottom: y = -1
    return x, y


if __name__ == "__main__":
    pg.init() 
    while True:
        result = main()
        if result!=True:
            break
    pg.quit()
    sys.exit()