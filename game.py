from ursina import *

class Car(Entity):
    def __init__(self):
        super().__init__()

        self.model, self.texture = 'car', 'car_texture'
        self.car = Entity(model=self.model, texture=self.texture, scale=0.3, rotation=(0,0,0))
        self.speed = 4
        self.deceleration = 0
        self.acceleration = 0

    def input(self, key):

        if key=='left shift':
            self.speed = 12 - self.speed

    def update(self):

        self.car.z += held_keys['w'] * self.speed * math.cos(self.car.rotation_y*pi/180) * time.dt
        self.car.z -= held_keys['s'] * self.speed * math.cos(self.car.rotation_y*pi/180) * time.dt
        self.car.x += held_keys['w'] * self.speed * math.sin(self.car.rotation_y*pi/180) * time.dt
        self.car.x -= held_keys['s'] * self.speed * math.sin(self.car.rotation_y*pi/180) * time.dt

        # if self.deceleration < 1:
        #     self.deceleration += held_keys['s'] * 0.01
        # if self.acceleration < 1:
        #     self.acceleration += held_keys['w'] * 0.01

        # if (held_keys['w']+held_keys['s']) == 0:

        #     print(self.car.rotation)
        #     self.acceleration, self.deceleration = 0, 0

        #? flips the rotation of 'a' and 'd' when going backwards
        # if held_keys['s']==1:
        #     self.car.rotation_y -= held_keys['d'] - held_keys['a']
        # else:
        #     self.car.rotation_y += held_keys['d'] - held_keys['a']

        self.car.rotation_y += (held_keys['d'] - held_keys['a'])*self.speed/2

if __name__ == '__main__':

    app = Ursina()

    Entity(model='quad', scale=60, rotation=(90,0,0), texture='white_cube', texture_scale=(60, 60),
            color=color.light_gray)

    camera.rotation = (90,0,0)
    camera.position = (0,40,0)

    car = Car()

    app.run()
