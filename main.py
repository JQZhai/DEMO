import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *
pygame.init()
pygame.mixer.init()
bg_size=width,height=480,700
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战--ZJQ Demo')
background=pygame.image.load('images/background.png').convert()
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
WHITE=(255,255,255)
    # 载入音乐
pygame.mixer.music.load('sound/hundouluo.wav')
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound('sound/supply.wav')
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.6)
enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)
def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1=enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e1=enemy.MidEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
def add_big_enemies(group1,group2,num):
    for i in range(num):
        e1=enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
def inc_speed(target,inc):
    for each in target:
        each.speed+=inc
def main():
    pygame.mixer.music.play(-1)
    #生成主角飞机
    me=myplane.MyPlane(bg_size)
    #生成敌机
    enemies=pygame.sprite.Group()
    #小飞机
    small_enemies=pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)
    #中飞机
    mid_enemies=pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,4)
    #大飞机
    big_enemies=pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,15)
    #只打开一次文件
    recorded=False
    #一般的子弹
    bullet1=[]
    bullet1_index=0
    BULLET1_NUM=6
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    clock=pygame.time.Clock()
    #超级子弹
    DOUBLE_BULLTET_TIME=USEREVENT+1
    is_double_bullet=False
    bullet2=[]
    bullet2_index=0
    BULLET2_NUM=12
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+30,me.rect.centery)))
    clock=pygame.time.Clock()
    #无敌时间
    INVINCIBLE_TIME=USEREVENT+2
    #命
    life_image=pygame.image.load('images/life.png').convert_alpha()
    life_rect=life_image.get_rect()
    life_num=5
    #中弹图片索引
    e1_destroy_index=0
    e2_destroy_index=0
    e3_destroy_index=0
    me_destroy_index=0
    #统计得分
    score=0
    score_font=pygame.font.Font('font/againts refresh.ttf',44)
    #难度
    level=1
    #炸弹
    bomb_image=pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect=bomb_image.get_rect()
    bomb_font=pygame.font.Font('font/againts refresh.ttf',54)
    bomb_num=3
    # 游戏结束画面
    gameover_font = pygame.font.Font('font/againts refresh.ttf', 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()
    #发放补给包
    bullet_supply=supply.Bullet_Supply(bg_size)
    bomb_supply=supply.Bomb_Supply(bg_size)
    SUPPLY_TIME=USEREVENT
    pygame.time.set_timer(SUPPLY_TIME,15*1000)
    #暂停
    paused=False
    pause_nor_image=pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image=pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image=pygame.image.load('images/resume_pressed.png').convert_alpha()
    resume_pressed_image=pygame.image.load('images/resume_nor.png').convert_alpha()
    paused_rect=pause_nor_image.get_rect()
    paused_rect.left,paused_top=width-paused_rect.width-10,10
    paused_image=pause_nor_image
    #飞机喷气
    switch_image=True
    #更优秀的喷气
    delay=100
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1 and paused_rect.collidepoint(event.pos):
                    paused=not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME,30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type==MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image=resume_pressed_image
                    else:
                        paused_image=pause_pressed_image
                else:
                    if paused:
                        paused_image=resume_nor_image
                    else:
                        paused_image=pause_nor_image
            elif event.type==KEYDOWN:
                if event.key==K_SPACE:
                    if bomb_num:
                        bomb_num-=1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom>0:
                                each.active=False
            elif event.type==SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type==DOUBLE_BULLTET_TIME:
                is_double_bullet=False
                pygame.time.set_timer(DOUBLE_BULLTET_TIME,0)
            elif event.type==INVINCIBLE_TIME:
                me.invincible=False
                pygame.time.set_timer(INVINCIBLE_TIME,0)


    #根据得分增加难度
        if level==1 and score>5000:
            level+=1
            upgrade_sound.play()
            #增加3架小型，2架中型，1架大型
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)
            add_small_enemies(big_enemies,enemies,1)
            inc_speed(small_enemies,1)
        elif level==2 and score>30000:
            level+=1
            upgrade_sound.play()
            #增加5架小型，2架中型，1架大型
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_small_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        elif level==3 and score>60000:
            level+=1
            upgrade_sound.play()
            #增加5架小型，2架中型，1架大型
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_small_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            inc_speed(big_enemies,1)  
        elif level==4 and score>100000:
            level+=1
            upgrade_sound.play()
            #增加5架小型，2架中型，1架大型
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_small_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            inc_speed(big_enemies,1) 
        elif level==5 and score>200000:
            level+=1
            upgrade_sound.play()
            #增加5架小型，2架中型，1架大型
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_small_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            inc_speed(big_enemies,1)  
        elif level==6 and score>500000:
            level+=1
            upgrade_sound.play()
            #增加5架小型，2架中型，1架大型
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_small_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            inc_speed(big_enemies,1)
        elif level==7 and score>1000000:
            level+=1
            upgrade_sound.play()
            #增加5架小型，2架中型，1架大型
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_small_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            inc_speed(big_enemies,1)   
        screen.blit(background,(0,0))
        if not paused and life_num:    
        #检测用户的操作
            key_pressed=pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(me, bomb_supply):
                    get_bomb_sound.play()
                    if bomb_num < 10:
                        bomb_num += 1
                    bomb_supply.active = False

            # 绘制超级子弹补给
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(me, bullet_supply):
                    get_bullet_sound.play()
                    # 发射超级子弹
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLTET_TIME, 15 * 1000)
                    bullet_supply.active = False
        #发射子弹
            if not(delay%10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets=bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+30,me.rect.centery))
                    bullet2_index=(bullet2_index+2)%BULLET2_NUM
                else:
                    bullets=bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index=(bullet1_index+1)%BULLET1_NUM
        #检测子弹碰撞
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit=pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active=False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit=True
                                e.energy-=1
                                if e.energy==0:
                                    e.active=False
                            else:
                                e.hit=True
                                e.energy-=1
                                if e.energy==0:
                                    e.active=False
 # 绘制敌方大型机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)

                    # 当生命大于20%显示绿色, 否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5),
                                     2)

                    # 即将出现在画面, 播放音效
                    if each.rect.bottom == -5:
                        enemy3_fly_sound.play(-1)

                else:
                    enemy3_down_sound.play()
                    enemy3_fly_sound.stop()
                    score += 1000
                    each.reset()
                    #毁灭
                    # if e3_destroy_index == 0:
                    #     enemy3_down_sound.play()
                    # if not(delay % 2):
                    #     screen.blit(each.destroy_images[
                    #                 e3_destroy_index], each.rect)
                    #     e3_destroy_index = (e3_destroy_index + 2) % 6
                    #     if e3_destroy_index == 0:
                    #         enemy3_fly_sound.stop()
                    #         score += 1000
                    #         each.reset()
        #画中型机
            for M in mid_enemies:
                if M.active:
                    M.move()
                    if M.hit:
                        screen.blit(M.image_hit,M.rect)
                        M.hit=False
                    else:
                        screen.blit(M.image,M.rect)
                    pygame.draw.line(screen,BLACK,\
                    (M.rect.left,M.rect.top -5),\
                    (M.rect.right,M.rect.top -5),\
                    2)
            #血量低于20%变红
                    energy_remain=M.energy/enemy.MidEnemy.energy
                    if energy_remain>0.2:
                        energy_color=GREEN
                    else:
                        energy_color=RED
                    pygame.draw.line(screen,energy_color,\
                    (M.rect.left,M.rect.top-5),\
                    (M.rect.left+M.rect.width*energy_remain,\
                    M.rect.top-5),2)
                else:
                    # 毁灭
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    if not(delay % 2):
                        screen.blit(M.destroy_images[e2_destroy_index], M.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 600
                            M.reset()
        #画小飞机
            for S in small_enemies:
                if S.active:
                    S.move()
                    if M.hit:
                        screen.blit(M.image_hit,M.rect)
                        M.hit=False
                    else:
                        screen.blit(S.image,S.rect)
                else:
                    if e1_destroy_index==0:
                        enemy1_down_sound.play() 
                    if not(delay%3):
                        screen.blit(S.destroy_images[e1_destroy_index],S.rect)
                        e1_destroy_index=(e1_destroy_index+1)%4
                        if e1_destroy_index==0:
                            score+=100
                            S.reset()
        #检测碰撞
            enemies_down=pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active=False
                for e in enemies_down:
                    e.active=False
            #画出我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1,me.rect)
                else:
                    screen.blit(me.image2,me.rect)
            else:
                if not(delay%3):
                    if me_destroy_index==0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index],me.rect)
                    me_destroy_index=(me_destroy_index+1)%4
                    if me_destroy_index==0:
                        life_num-=1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME,3*1000)
        #画炸弹
            bomb_text=bomb_font.render('X %d' % bomb_num,True,WHITE)
            text_rect=bomb_text.get_rect()
            screen.blit(bomb_image,(10,height-10-bomb_rect.height-20))
            screen.blit(bomb_text,(20+bomb_rect.width,height-text_rect.height))
        #画命
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,\
                    (width-10-(i+1)*life_rect.width,\
                    height-10-life_rect.height))
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()          
            # 停止全部音效
            pygame.mixer.stop()
            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)
            if not recorded:
                recorded =True
                # 读取历史最高分
                with open('record.txt', 'r') as f:
                    record_score = int(f.read())
                # 判断是否高于历史最高分
                if score > record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))
            # 绘制结束界面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))
            
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
        #画得分
        score_text=score_font.render('Score : %s'% str(score),True,WHITE)
        screen.blit(score_text,(10,5))
        screen.blit(paused_image,paused_rect)
    #5帧切换一次
        if not(delay%5):
            switch_image=not switch_image
        delay-=1
        if not delay:
            delay=100
        pygame.display.flip()
        clock.tick(60)
if __name__=="__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
