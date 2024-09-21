#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
init()
#создай окно игры
window = display.set_mode((700, 500))
display.set_caption('pygame window')
#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'), (700, 500 ))

mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
gunfire = mixer.Sound('gunfire.mp3')


game = True

clock = time.Clock()
FPS = 60#ЧАСТОТА КАДРОВ
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.speed
    def fire(self):#Метод выстрел
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -100:
            self.kill()
            
            

lost = 0
#?_____________________________________________________________________.
class Enemy(GameSprite):
    def update(self):#метод для автоматического движеня спрайта№2
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = -100
            self.rect.x = randint(0,700)
            lost += 1
class meteorites(GameSprite):
    def update(self):#метод для автоматического движеня спрайта№3
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -100
            self.rect.x = randint(0,700)

        


player = Player('rocket.png',50, 400, 5)#! экземпляр класса Player.
meteorite = meteorites('asteroid.png', randint(50, 650), randint(-100,-10),  randint(1,2))
meteorite2 = meteorites('asteroid.png', randint(50, 650), randint(-100,-10), randint(1,2))
meteorite3 = meteorites('asteroid.png', randint(50, 650), randint(-100,-10), randint(1,2))
enemy = Enemy('ufo.png', 50, randint(-100,-10), randint(1,3))
enemy2 = Enemy('ufo.png', 100, randint(-100,-10), randint(1,3))
enemy3 = Enemy('ufo.png', 150, randint(-100,-10), randint(1,3))
enemy4 = Enemy('ufo.png', 200, randint(-100,-10), randint(1,3))
enemy5 = Enemy('ufo.png', 250, randint(-100,-10), randint(1,3))
#? создание группы для метиоритов.
metior = sprite.Group()
metior.add(meteorite)
metior.add(meteorite2)
metior.add(meteorite3)
# TODO группа для врагов.
monsters = sprite.Group()#создание группы для работы с группой спрайтов как с одним
monsters.add(enemy)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)

bullets = sprite.Group()


finish = False

font1 = font.SysFont('Arial', 25)

num_fire = 0
enemy_kill = 0
live = 3
check = font1.render('Счёт: ' + str(enemy_kill),  True, (255, 255, 255))

live_counter = font1.render('счётчик жизней:' + str(live), True, (255, 255, 255))

missed = font1.render('Пропущено: ' +  str(lost), True, (255, 255, 255))

win = font1.render('YOU WIN!', True, (255, 215, 0))

lose = font1.render('YOU LOSE', False, (255, 0, 0))

rel_time = False



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if finish == False:
                if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        player.fire()
                        num_fire += 1
                        gunfire.play()
                    if num_fire >= 5 and rel_time == False:
                        rel_time = True
                        last_time = timer()                     
            if finish:
                if e.key == K_r:
                    for i in monsters:
                        i.kill()
                    for i in range(5):
                        enemy = Enemy('ufo.png',randint (50, 650), randint(-100,-10), randint(1,3))
                        monsters.add(enemy)
                        player.rect.x = 50
                        player.rect.y = 400
                    for i in range(3):
                        meteorite = meteorites('asteroid.png',randint (50, 650), randint(-100,-10), randint(1,3))
                        metior.add(meteorite)
                        player.rect.x = 50
                        player.rect.y = 400
                    for i in bullets:
                        i.kill()
                    mixer.music.play()
                    enemy_kill = 0
                    lost = 0
                    lost = 0
                    finish = False
    
    if finish != True:
        window.blit(background,(0, 0))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1.5:
                reload1 = font1.render('Wait, reload...', False, (255, 0, 0))
                window.blit(reload1, (300, 200))
            else:
                num_fire = 0
                rel_time = False


        
        missed = font1.render('Пропущено: ' +  str(lost), True, (255, 255, 255))
        live_counter = font1.render('счётчик жизней:' + str(live), True, (255, 255, 255))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        metior.draw(window)
        metior.update()
        bullets.draw(window)
        bullets.update()
        reload1 = font1.render('Wait, reload...', False, (255, 0, 0))
        check = font1.render('Счёт: ' + str(enemy_kill),  True, (255, 255, 255))
        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        sprites_list1 = sprite.groupcollide(bullets, metior, True, False )
        sprites_list2 = sprite.spritecollide(player, metior, True )
        sprites_list3 = sprite.spritecollide(player, monsters, True )
        for i in sprites_list:
            enemy_kill += 1
            enemy = Enemy('ufo.png', randint(0, 650), randint(-100,-10), randint(1,3)) 
            monsters.add(enemy)
        if enemy_kill == 10:
            window.blit(win, (300, 200))
            finish = True
            mixer.music.stop()
        if lost == 3:
            window.blit(lose, (300, 200))
            finish = True
            mixer.music.stop()
        if sprites_list3:
            live -= 1 
        if sprites_list2:
            live -= 1
        if live == 0:
            window.blit(lose, (300, 200))
            finish = True
            mixer.music.stop()
        window.blit(missed, (0, 0))
        window.blit(check, (0, 20))
        window.blit(live_counter, (0, 40))

    display.update()
    clock.tick(FPS)