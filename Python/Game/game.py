import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 600

game_state = "start"
sound_toggle = True

TITLE = "Rogue"

music.play("game_music")
music.set_volume(0.5)

menu = {
    "begin": Rect(325, 200, 200, 50),
    "toggle_sound": Rect(325, 250, 200, 50),
    "quit": Rect(325, 300, 200, 50)
}

background = Actor('background')

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.actor = Actor("coin", (x, y))
    
    def draw(self):
        self.actor.draw()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coins = 0
        self.direction = "down"
        self.frame = 0
        self.anim_timer = 0
        self.frame_time = 0.1
        self.images = {
            "up": ["up_player_1", "up_player_2", "up_player_3", "up_player_4"],
            "down": ["down_player_1", "down_player_2", "down_player_3", "down_player_4"],
            "left": ["left_player_1", "left_player_2", "left_player_3", "left_player_4"],
            "right": ["right_player_1", "right_player_2", "right_player_3", "right_player_4"]
        }
        self.actor = Actor(self.images[self.direction][0], (x, y))

    def update(self):
        if keyboard.up:
            if self.y > 5:
                self.y -= 5
            self.direction = "up"
        elif keyboard.down:
            if self.y < HEIGHT-5:
                self.y += 5
            self.direction = "down"
        elif keyboard.left:
            if self.x > 5:
                self.x -= 5
            self.direction = "left"
        elif keyboard.right:
            if self.x < WIDTH-5:
                self.x += 5
            self.direction = "right"

        self.animate()
        self.actor.x = self.x
        self.actor.y = self.y

    def animate(self):
        self.anim_timer += self.frame_time
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.images[self.direction])
        self.actor.image = self.images[self.direction][self.frame]

    def draw(self):
        self.actor.draw()

class Enemy:
    def __init__(self, x_start, x_end, y):
        self.start = x_start
        self.end = x_end
        self.x = x_start
        self.y = y
        self.speed = 2
        self.direction = "right"
        self.frame = 0
        self.anim_timer = 0
        self.frame_time = 0.1
        self.images = {
            "left": ["left_enemy_1", "left_enemy_2", "left_enemy_3", "left_enemy_4"],
            "right": ["right_enemy_1", "right_enemy_2", "right_enemy_3", "right_enemy_4"]
        }
        self.actor = Actor(self.images[self.direction][0], (x_start, y))

    def update(self):
        if((self.x + self.speed) > self.start and (self.x + self.speed) < self.end):
            self.x += self.speed
        else:
            self.speed *= -1
            if(self.direction == "right"):
                self.direction = "left"
            else:
                self.direction = "right"
        self.animate()
        self.actor.x = self.x

    def animate(self):
        self.anim_timer += self.frame_time
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.images[self.direction])
        self.actor.image = self.images[self.direction][self.frame]
    
    def draw(self):
        self.actor.draw()


player = Player(50, 550)

enemies = [Enemy(100, 300, 200), Enemy(350, 550, 500), Enemy(550, 750, 400)]

coins = [Coin(200, 100), Coin(450, 400), Coin(650, 300)]

def update():
    global game_state
    if(game_state == "game"):
        player.update()
        for enemy in enemies:
            enemy.update()
            if(player.actor.colliderect(enemy.actor)):
                if sound_toggle:
                    sounds.hit.play()
                print("GAME OVER")
                exit()
        for coin in coins:
            if(player.actor.colliderect(coin.actor)):
                if sound_toggle:
                    sounds.coin.play()
                coins.remove(coin)
                player.coins += 1
        if(player.coins == 3):
            print("YOU WIN")
            exit()

def draw_menu():
    for name, rect in menu.items():
        screen.draw.filled_rect(rect, (100, 100, 100))
        label = {
            "begin": "Begin Game",
            "toggle_sound": "Music: ON" if sound_toggle else "Music: OFF",
            "quit": "Quit Game"
        }[name]
        screen.draw.text(label, center=rect.center, fontsize=36, color=(255,255,255))

def draw():
    global game_state
    screen.clear()
    if(game_state == "start"):
        draw_menu()
    else:
        background.draw()
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for coin in coins:
            coin.draw()

def on_mouse_down(pos):
    global game_state, sound_toggle
    if(game_state == "start"):
        if(menu["begin"].collidepoint(pos)):
            game_state = "game"
        elif(menu["toggle_sound"].collidepoint(pos)):
            sound_toggle = not sound_toggle
            if(sound_toggle):
                music.set_volume(0.5)
            else:
                music.set_volume(0)
        elif(menu["quit"].collidepoint(pos)):
            exit()
pgzrun.go()