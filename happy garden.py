# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:20:45 2023

@author: Student
"""


import pgzrun
import pygame
import pgzero
import random
from pgzero.builtins import Actor
from random import randint
import time

#creating the screen:
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

#defining the global variables
game_over = False
finalized = False
garden_happy = True
fangflower_collision = False
new_enemy_collison = False

time_elapsed = 0
start_time = time.time()
#defining the actor :cow
cow = Actor("cow")
cow.pos = 100, 500
#defining the flower list and wilted list
flower_list = []
wilted_list = []

#defining fang flower:
fangflower_list = []
fangflower_vy_list = []
fangflower_vx_list = []

#defining a new enemy
new_enemy_list = []
new_enemy_vx_list = []
new_enemy_vy_list = []
background_images = ["garden", "garden-raining"]
current_bg_index = 0
last_bg_change_time = time.time()

def draw():
    global game_over, time_elapsed, finalized
    global current_bg_index, last_bg_change_time
    
    # Check if it's time to change the background
    elapsed_time = int(time.time() - last_bg_change_time)
    if elapsed_time >= 10 and not game_over:
        current_bg_index = (current_bg_index + 1) % len(background_images)
        last_bg_change_time = time.time()
    
    # Clear the screen and draw the background
    screen.clear()
    screen.blit(background_images[current_bg_index], (0, 0))
    
    # Draw the other game elements
    if not game_over:
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()
        for enemy in new_enemy_list:
            enemy.draw()
            
        # Draw the time elapsed
        time_elapsed = int(time.time() - start_time)
        screen.draw.text("Garden happy for: " + str(time_elapsed) + " seconds",
                          topleft=(10, 10), color="black")
    else:
        if not finalized:
            cow.draw()
            screen.draw.text("Garden happy for: " + str(time_elapsed) + " seconds",
                              topleft=(10, 10), color="black")
        if not garden_happy:
                screen.draw.text("GARDEN UNHAPPY - GAME OVER!", color="red",
                                  topleft=(10, 50))
        else:
                screen.draw.text("FANGFLOWER OR NEW-ENEMY-ATTACK - GAME OVER!",
                                  color="red", topleft=(10, 50))
                finalized = True

#defining the flower
def new_flower():
 global flower_list, wilted_list
 flower_new = Actor("flower")
 flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)
 flower_list.append(flower_new)
 wilted_list.append("happy")
 return
#adding the flower
def add_flowers():
 global game_over
 if not game_over:
     new_flower()
     clock.schedule(add_flowers, 4)
 return

def check_wilt_times():
 global wilted_list, game_over, garden_happy
 if wilted_list:
     for wilted_since in wilted_list:
         if (not wilted_since == "happy"):
             time_wilted = int(time.time() - wilted_since)
             if (time_wilted) > 10.0:
                 garden_happy = False
                 game_over = True
                 break
 return


def wilt_flower():
 global flower_list, wilted_list, game_over
 if not game_over:
     if flower_list:
         rand_flower = randint(0, len(flower_list) - 1)
         if (flower_list[rand_flower].image == "flower"):
             flower_list[rand_flower].image = "flower-wilt"
             wilted_list[rand_flower] = time.time()
         clock.schedule(wilt_flower, 3)
 return


def check_flower_collision():
 global cow, flower_list, wilted_list
 index = 0
 for flower in flower_list:
     if (flower.colliderect(cow) and
         flower.image == "flower-wilt"):
         flower.image = "flower"
         wilted_list[index] = "happy"
         break
     index = index + 1
 return

def check_fangflower_collision():
 global cow, fangflower_list, fangflower_collision, new_enemy_list
 global game_over
 for fangflower in fangflower_list:
     if fangflower.colliderect(cow):
         cow.image = "zap"
         game_over = True
         break
 for new_enemy in new_enemy_list:
     if new_enemy.colliderect(cow):
         cow.image = "zap"
         game_over = True
         break
 return


def velocity():
 random_dir = randint(0, 1)
 random_velocity = randint(2, 3)
 if random_dir == 0:
     return -random_velocity
 else:
     return random_velocity

def mutate():
  global flower_list, fangflower_list, fangflower_vy_list
  global fangflower_vx_list, game_over
  
  global new_enemy_list, new_enemy_vy_list, new_enemy_vx_list
  
  if not game_over and flower_list:
      for i in range(2):
          rand_flower = randint(0, len(flower_list) - 1)
          fangflower_pos_x = flower_list[rand_flower].x
          fangflower_pos_y = flower_list[rand_flower].y
          del flower_list[rand_flower]
          fangflower = Actor("fangflower")
          fangflower.pos = fangflower_pos_x, fangflower_pos_y
          fangflower_vx = velocity()
          fangflower_vy = velocity()
          fangflower_list.append(fangflower)
          fangflower_vx_list.append(fangflower_vx)
          fangflower_vy_list.append(fangflower_vy)
      clock.schedule(mutate, 5)

 
      for i in range(2):
          rand_flower = randint(0, len(flower_list) - 1)
          new_enemy_pos_x = flower_list[rand_flower].x
          new_enemy_pos_y = flower_list[rand_flower].y
          del flower_list[rand_flower]
          new_enemy = Actor("new_enemy")
          new_enemy.pos = new_enemy_pos_x, new_enemy_pos_y
          new_enemy_vx = velocity()
          new_enemy_vy = velocity()
          new_enemy_list.append(new_enemy)
          new_enemy_vx_list.append(new_enemy_vx)    
          new_enemy_vy_list.append(new_enemy_vy)
      clock.schedule(mutate, 10)

def update_fangflowers():
 global fangflower_list, game_over
 if not game_over:
     index = 0
     for fangflower in fangflower_list:
         fangflower_vx = fangflower_vx_list[index]
         fangflower_vy = fangflower_vy_list[index]
         fangflower.x = fangflower.x + fangflower_vx
         fangflower.y = fangflower.y + fangflower_vy
         if fangflower.left < 0:
             fangflower_vx_list[index] = -fangflower_vx
         if fangflower.right > WIDTH:
             fangflower_vx_list[index] = -fangflower_vx
         if fangflower.top < 150:
             fangflower_vy_list[index] = -fangflower_vy
         if fangflower.bottom > HEIGHT:
             fangflower_vy_list[index] = -fangflower_vy
         index = index + 1
 return
def update_new_enemy():
    global new_enemy_list, new_enemy_vx_list, new_enemy_vy_list, game_over
    if not game_over:
        index = 0
        for new_enemy in new_enemy_list:
            new_enemy_vx = new_enemy_vx_list[index]
            new_enemy_vy = new_enemy_vy_list[index]
            new_enemy.x = new_enemy.x + new_enemy_vx
            new_enemy.y = new_enemy.y + new_enemy_vy
            if new_enemy.left < 0:
                new_enemy_vx_list[index] = -new_enemy_vx
            if new_enemy.right > WIDTH:
                new_enemy_vx_list[index] = -new_enemy_vx
            if new_enemy.top < 150:
                new_enemy_vy_list[index] = -new_enemy_vy
            if new_enemy.bottom > HEIGHT:
                new_enemy_vy_list[index] = -new_enemy_vy
            index = index + 1
    return

def reset_cow():
 global game_over
 if not game_over:
     cow.image = "cow"
 return
add_flowers()
wilt_flower()
def update():
 global score, game_over, fangflower_collision
 global flower_list, fangflower_list, time_elapsed
 fangflower_collision = check_fangflower_collision()
 check_wilt_times()
 if not game_over:
   if keyboard.space:
            cow.image = "cow-water"
            clock.schedule(reset_cow, 0.5)
            check_flower_collision()
            
   if keyboard.left and cow.x > 0:
            cow.x -= 5
   elif keyboard.right and cow.x < WIDTH:
            cow.x += 5
   elif keyboard.up and cow.y > 150:
            cow.y -= 5
   elif keyboard.down and cow.y < HEIGHT:
             cow.y += 5
   if time_elapsed > 15 and not fangflower_list and not new_enemy_list:
             mutate()
             update_fangflowers()
             update_new_enemy()

pgzrun.go()