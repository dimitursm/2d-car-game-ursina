from ursina import *

class Car(Entity):
    def __init__(self):
        super().__init__()

        self.model, self.texture = 'car', 'car_texture'
        self.car = Entity(model=self.model, texture=self.texture, scale=0.3, rotation=(0,0,0))
        self.speed = 0
        self.max_speed = 4
        self.dir = 1
        self.zero = True

    def input(self, key):

        if key=='left shift':
            self.max_speed = 12 - self.max_speed # double/halve the speed (4 -> 8 -> 4)

    def update(self):

        if self.speed==0:
            self.zero = True

        self.car.z += self.dir * self.speed * math.cos(self.car.rotation_y*pi/180) * time.dt
        self.car.x += self.dir * self.speed * math.sin(self.car.rotation_y*pi/180) * time.dt

        self.car.rotation_y += self.dir * (held_keys['d'] - held_keys['a'])*self.speed/2

        if (self.xor(held_keys['w'], held_keys['s'])==0 or not self.zero) and not self.dir==held_keys['w'] - held_keys['s']:
            self.speed = max(self.speed - 2*time.dt, 0)
            self.zero = False
        elif self.speed>self.max_speed:
            self.speed = max(self.speed - 2*time.dt, 0)
        elif self.zero or self.dir==held_keys['w'] - held_keys['s']:
            self.dir = held_keys['w'] - held_keys['s']
            self.speed = min(self.speed + self.xor(held_keys['w'], held_keys['s']) * 2 * time.dt, self.max_speed)

    def xor(self, a, b):
        if a==1 and b==1:
            return 0
        return max(a,b)

if __name__ == '__main__':

    app = Ursina()

    Entity(model='quad', scale=60, rotation=(90,0,0), texture='white_cube', texture_scale=(60, 60),
            color=color.light_gray)

    camera.rotation = (90,0,0)
    camera.position = (0,40,0)

    car = Car()

    speedometer = Text(text=str(car.speed*25), position=(0,0,0), color = color.black)

    def update():
        speedometer.text = str(math.floor(car.speed*25))

    app.run()
