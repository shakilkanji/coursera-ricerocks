# program template for Spaceship
import simplegui
import math
from random import randint

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
friction = 0.02
new_game = True
rock_set = set()
missile_set = set()

def start_over():
    global score, lives, new_game, rock_set, missile_set
    score = 0
    lives = 3
    new_game = True
    rock_set = set()
    missile_set = set()
    soundtrack.rewind()
    
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrust == True:
            self.image_center[0] = 135
        else:
            self.image_center[0] = 45
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)    
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += 0.3 * forward[0]
            self.vel[1] += 0.3 * forward[1]
        self.pos[0] = self.pos[0] % 800
        self.pos[1] = self.pos[1] % 600
        self.vel[0] *= (1-friction)
        self.vel[1] *= (1-friction)
        
    def decrement_angular_vel(self):
        self.angle_vel = -0.06
        
    def increment_angular_vel(self):
        self.angle_vel = 0.06
        
    def stop_rotation(self):
        self.angle_vel = 0
        
    def start_thrust(self):
        self.thrust = True
        ship_thrust_sound.play()
        
    def stop_thrust(self):
        self.thrust = False
        ship_thrust_sound.rewind()
        
    def shoot(self):
        global missile_set
        forward = angle_to_vector(self.angle)
        a_missile = Sprite([self.pos[0] + 38 * forward[0], self.pos[1] + 38 * forward[1]], [self.vel[0] + 4 * forward[0], self.vel[1] + 4 * forward[1]], 
                           self.angle, 0, missile_image, missile_info, missile_sound, 100)
        missile_set.add(a_missile)
        
# Key Handlers

def keydown(key):
    if key==simplegui.KEY_MAP["left"]:
        my_ship.decrement_angular_vel()
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.increment_angular_vel()
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.start_thrust()
    elif key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()
            
def keyup(key):
    if key==simplegui.KEY_MAP["left"] or key==simplegui.KEY_MAP["right"]:
        my_ship.stop_rotation()
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.stop_thrust()
        
def mouse_handler(position):
    global new_game
    new_game = False
    soundtrack.play()
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, lifespan = None):
        self.pos = [pos[0],pos[1]]
        self.pos0 = pos[0]
        self.pos1 = pos[1]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_position0(self):
        return self.pos[0]
    
    def get_position1(self):
        return self.pos[1]
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.age += 1
        if self.age > self.lifespan:
            return True
              
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) < (self.radius + other_object.get_radius()):
            return True
        else:
            return False
        
def group_collide(group, other_object):
    for sprite in set(group):
        if Sprite.collide(sprite, other_object):
            group.remove(sprite)
            return True
        
def group_group_collide(group1, group2):
    for sprite in set(group1):
        if group_collide(group2, sprite):
            group1.remove(sprite)
            return True

def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        if (sprite.get_position0() > 830 or sprite.get_position0() < -30 or
            sprite.get_position1() > 630 or sprite.get_position1() < -30):
            group.remove(sprite)
        if sprite.update():
             group.remove(sprite)
        
def draw(canvas):
    global time, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_set, canvas)
    process_sprite_group(missile_set, canvas)
    if group_collide(rock_set, my_ship):
        lives -= 1
    if group_group_collide(rock_set, missile_set):
        score += 1
    if lives < 1:
        start_over()
    
    # update ship and sprites
    my_ship.update()
    
    
    # draw score and lives
    canvas.draw_text("Score: " + str(score), (660, 30), 30, "White")
    canvas.draw_text("Lives: " + str(lives), (20, 30), 30, "White")
    
    # draw splash
    if new_game:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2, HEIGHT/2], [WIDTH/2, HEIGHT/2])
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_set
    a_rock = Sprite([randint(50,750), randint(50,550)], [0.1 * randint(-10,10), 0.1 * randint(-10,10)], randint(0,7), 0.01 * randint(-20, 20), asteroid_image, asteroid_info)
    if len(rock_set) < 12 and new_game == False and dist(a_rock.get_position(), my_ship.get_position()) > 60: 
        rock_set.add(a_rock)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
timer.start()
frame.start()
