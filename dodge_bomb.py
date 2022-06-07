
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
     

        self.vx *= x # 横方向に画面外なら，横方向速度の符号反転
        self.vy *= y # 縦方向に画面外なら，縦方向速度の符号反転
        # if (x, y) != (1,1):
        #     self.vx *= x*1.5#横方向
        #     self.vy *= y*1.5 #縦方向


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
            
        # pg.display.update()     # 画面を更新
            
            # vx *= x*self.speed #横方向
            # vy *=y*self.speed #縦方向

        text2 = self.conf_font.render(f"{self.conflict}/100conflicts", True, (255,255,255))   # 描画する文字列の設定
        screen.disp.blit(text2, [0,0])# 文字列の表示位置
    
        return self.conflict
        
    
    def GameOver(self,screen):
        text = self.font.render("GAME OVER", True, (255,0,0))   # 描画する文字列の設定
        screen.disp.blit(text, [400,200])# 文字列の表示位置
        pg.display.update()
          # 画面を更新
   

    def speedup(self, screen, bombs):
        for _ in bombs:
            x, y = check_bound(screen.rect, _.rect)
            if (x, y) != (1,1):
                
                _.vx *= self.speed #横方向
                _.vy *= self.speed #縦方向
                print(_.vx,_.vy)

class Negi(pg.sprite.Sprite): #ねぎを追加
    def __init__(self, fn, r, xy):
        #fn: filename  r: 拡大率  xy:座標のタプル
        super().__init__()
        self.image = pg.image.load(fn)      #Surface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect= self.image.get_rect()   #Rect
        self.rect.center = xy
        

def main():
    NEGI = 0 #ねぎの表示の有無
    negi_list = [20,40,60,80] #ねぎの出現するスコアの値
    global conflict
    
    clock = pg.time.Clock()
    check_wall=RelatedWall()
    # 練習1
    
    screen = Screen('fig/pg_bg.jpg',(1600,900), "逃げろ！こうかとん")    # 画面用のSurface

    screen.disp.blit(screen.image,(0,0))           # 背景画像用Surfaceを画面用Surfaceに貼り付ける

    # 練習3

    tori = pg.sprite.Group()
    tori.add(Bird("fig/3.png",2, (900,400)))                # こうかとん画像の中心座標を設定する
    # screen.disp.blit(tori.image, tori.rect)               # こうかとん画像用のSurfaceを画面用Surfaceに貼り付ける
    
    # 練習5
    # bomb = Bomb((255,0,0), 10, (+2,+2), screen)
    # screen.disp.blit(bomb.image, bomb.rect)                   # 爆弾用のSurfaceを画面用Surfaceに貼り付ける
 
    bombs = pg.sprite.Group()

    for _ in range(2):
        # check_wall.show_conflict(screen,Bomb((255,0,0), 10, (+2,+2), screen))
        bombs.add(Bomb((255,0,0), 10, (+4,+4), screen))

    conflict = check_wall.show_conflict(screen, bombs)

    negi = pg.sprite.Group() ##

    while True:
        # 練習2
        screen.disp.blit(screen.image, (0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT: return       # ✕ボタンでmain関数から戻る

        if conflict == 100:
            text = font.render("Play again:push space button", True, (0,0,255))   # 描画する文字列の設定
            screen.disp.blit(text, [400,200])# 文字列の表示位置
            text2 = font.render("Quit:push enter", True, (0,0,255))   # 描画する文字列の設定
            screen.disp.blit(text2, [400,400])# 文字列の表示位置
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

        # elif conflict//20==0:
        #     negi_img = pg.image.load("fig/negi.png")
        #     negi_img = pg.transform.rotozoom(negi_img, 0, )
        #     negi_rect = negi_img.get_rect()

        elif len(pg.sprite.groupcollide(tori, bombs, False, False)) !=0:
            text=font.render("Play again:push space button", True, (0,0,255))  
            text2 = font.render("Quit:push enter", True, (0,0,255))   # 描画する文字列の設定
            screen.disp.blit(text, [100,400])# 文字列の表示位置
            screen.disp.blit(text2, [100,500])# 文字列の表示位置
            check_wall.GameOver(screen)
            key_contenue_states = pg.key.get_pressed()
            if key_contenue_states[pg.K_SPACE]==True:
                print("ldkflakdf")
                pg.display.update()
                check_wall.conflict = 0
                conflict = 0
                return True
            elif key_contenue_states[pg.K_RETURN]==True:
                # time.sleep(2)
                return False
        else:
            # 練習4
            tori.update(screen)
            # screen.disp.blit(tori.image, tori.rect)
            tori.draw(screen.disp)
            # 練習6
            bombs.update(screen)
            # screen.disp.blit(bomb.image, bomb.rect)
            bombs.draw(screen.disp)
            font= pg.font.Font(None, 100)  
            check_wall.speedup(screen, bombs)

            conflict = check_wall.show_conflict(screen, bombs)

        if check_wall.conflict == negi_list[0]:
            NEGI = 1 #ねぎの表示
            negi_list.pop(0) #リスト番号０の削除

        if NEGI == 1:
            negi.add(Negi("fig/negi.png", 0.1, (random.randint(0, 1600), random.randint(0, 400))))
            NEGI = 0

        for i in pg.sprite.groupcollide(negi, tori, False, False):
            negi.remove(i)
            NEGI = 0
            check_wall.conflict += 5  #スコアを５追加
 
        negi.draw(screen.disp)


        

        pg.display.update()  # 画面の更新
        clock.tick(1000) 
    
# 練習7

def check_bound(sc_r, obj_r): # 画面用Rect, ｛こうかとん，爆弾｝Rect
    # 画面内：+1 / 画面外：-1
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