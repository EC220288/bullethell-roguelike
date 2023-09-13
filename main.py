import pygame
import sys
import math

# initialize pygame
pygame.init()

# making display/setting variables
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
fps = 60
player_speed = 10
bullet_speed = 8
bullets = []
type = ""
# parent class for player and enemies
class Entity:
    def __init__(self, x, y, width, height):
        # uses a Rect to create entity position
        self.rect = pygame.Rect(x, y, width, height)
        self.movex = 0
        self.movey = 0

    def main(self, display):
        # draws the player using the Rect
        pygame.draw.rect(display, self.colour, self.rect)

    def update(self):
            # updates entity position
        self.rect.x += self.movex
        self.rect.y += self.movey

class Player(Entity):
    # Player class with dimensions and set colour, child class of Entity)
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.colour = (255, 0, 0)

    def controls(self):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.rect.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rect.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.rect.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.rect.y += player_speed


class Enemy(Entity):
    # Child class for Enemies
    def __init__(self, x, y, width, height, type):
        super().__init__(x, y, width,height)
        self.type = type

        if self.type == "chaser":
            self.colour = (255, 0, 0)
    def update(self, type):
        if type == "chaser":
            enemy_speed = 5
            player_x, player_y = player.rect.centerx, player.rect.centery
            angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
            self.movex = math.cos(angle) * enemy_speed
            self.movey = math.sin(angle) * enemy_speed
            self.rect.x += self.movex
            self.rect.y += self.movey

    def main(self, display, type):
        pygame.draw.rect(display, self.colour, self.rect)
        Enemy.update(self,type)







class Bullet:       # todo make bullet shape a parameter of bullet class
    def __init__(self, x, y, angle, speed):
        # allows for bullet parameters to change and calculates bullet direction using trig
        self.rect = pygame.Rect(x, y, 5, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed


    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def bulletmech(bullets):
        new_bullets = []
        # checks if bullets are on screen and only draws if they are
        for bullet in bullets:
            bullet.update()
            if display.get_rect().colliderect(bullet.rect):
                new_bullets.append(bullet)
        bullets[:] = new_bullets
        for bullet in bullets:
            pygame.draw.rect(display, (255, 0, 0), bullet.rect)
        return bullets


# creates the player object
player = Player(400, 300, 32, 32)
mob1 = Enemy(400,300,32,32,"chaser")
while True:
    display.fill((24, 164, 86))

    # Allows the game to be closed by clicking X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # calculates direction based off mouse angle when clicked from player center
                mouse_x, mouse_y = event.pos
                angle = math.atan2(mouse_y - player.rect.centery, mouse_x - player.rect.centerx)
                bullets.append(Bullet(player.rect.centerx, player.rect.centery, angle, bullet_speed))
    keys = pygame.key.get_pressed()

# update and draws the player
    player.main(display)
    mob1.main(display, "chaser")
# mob1.update("chaser") #todo find better way of calling enemies and defining type
    bullets = Bullet.bulletmech(bullets)
    player.controls()
    # controls frame rate
    clock.tick(fps)
    # updates display through double buffering
    pygame.display.flip()

