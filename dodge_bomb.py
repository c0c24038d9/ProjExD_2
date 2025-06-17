import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

KK_IMAGES = { # 
    (0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),       # 静止 
    (0, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 0.9),    # 上 (270度回転) 
    (0, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9),      # 下 (90度回転) 
    (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),    # 左 (180度回転) 
    (5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 180, 0.9),       # 右 (0度回転) 
    (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 225, 0.9),   # 左上 (225度回転) 
    (5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 0.9),    # 右上 (315度回転) 
    (-5, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),    # 左下 (135度回転) 
    (5, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 135, 0.9)      # 右下 (45度回転) 
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:  # 引数の型を提示
    
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """

    yoko, tate = True, True  #初期値:画面の中
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate  #横方向,縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:

    """
    ゲームオーバー時に, 半透明の黒い画面上に「Game Over」と表示し, 泣いているこうかとん画像を貼り付ける関数
    """
    kk2_img = pg.image.load("fig/8.png")

    black_img = pg.Surface((WIDTH,HEIGHT))
    black_rct = black_img.get_rect()
    pg.draw.rect(black_img, (0,0,0), pg.Rect(0,0,WIDTH,HEIGHT))  #黒の四角を画面サイズに描画
    black_img.set_alpha(150)  #透明度
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GAME OVER",True, (255, 255, 255))  #ゲームオーバーの文字を表示
    screen.blit(black_img, black_rct)  #ブラックアウト
    screen.blit(kk2_img, [350,300])  #こうかとん右
    screen.blit(kk2_img, [750,300])  #こうかとん左
    screen.blit(txt, [400, 300])
    pg.display.update()
    time.sleep(5)  #5秒間表示(停止)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0),(10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))  #円の周りの黒を透過
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す
    """
    return KK_IMAGES.get(sum_mv, KK_IMAGES[(0, 0)])


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  #空のSurface(爆弾)
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #赤い円を描画
    bb_img.set_colorkey((0, 0, 0))  #円の周りの黒を透過
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  #横座標
    bb_rct.centery =random.randint(0, HEIGHT)  #縦座標
    vx, vy = 5, 5  #爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾の衝突判定
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 


        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # key_lst = pg.key.get_pressed()
        # sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #もし画面外(False)だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #移動を打ち消し
        
        kk_img = get_kk_img(tuple(sum_mv))
        screen.blit(kk_img, kk_rct)

        
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  #横にはみ出ていたら
            vx *= -1  #横座標反転
        if not tate:  #縦にはみ出ていたら
            vy *= -1  #縦座標反転

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
