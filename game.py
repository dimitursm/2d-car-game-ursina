from ursina import *

class Car(Entity):
    def __init__(self):
        super().__init__()

        self.model, self.texture = 'car', 'car_texture'
        self.car = Entity(model=self.model, texture=self.texture, scale=0.6, rotation=(0,0,0), collider='box')
        self.speed = 0
        self.max_speed = 4
        self.dir = 1
        self.rot = 0

    def input(self, key):

        if key=='left shift':
            self.max_speed = 12 - self.max_speed # double/halve the speed (4 -> 8 -> 4)

    def update(self):

        rotation_in_radians = self.car.rotation_y*pi/180
        speed_is_zero = self.speed==0
        turning = max(held_keys['d'], held_keys['a'])==1
        low_speed = self.speed < 4
        braking = held_keys['left control']==1
        pedal_is_pressed = self.xor(held_keys['w'], held_keys['s'])==1 # only one, not both
        changing_direction = not self.dir==held_keys['w'] - held_keys['s']
        max_speed_dropped = self.speed>self.max_speed

        if speed_is_zero:
            self.dir = held_keys['w'] - held_keys['s']

        self.car.z += self.dir * self.speed * math.cos(rotation_in_radians) * time.dt
        self.car.x += self.dir * self.speed * math.sin(rotation_in_radians) * time.dt

        if turning:
            self.rot =  min(max(self.rot + (held_keys['d'] - held_keys['a'])*2, -120), 120)
        else:
            if self.rot > 0:
                self.rot = max(self.rot - 128*time.dt, 0)
            else:
                self.rot = min(self.rot + 128*time.dt, 0)

        if low_speed:
            #turn steadily
            self.car.rotation_y += self.dir * self.rot * self.speed/4 * time.dt
        else:
            #turn normally
            self.car.rotation_y += self.dir * self.rot * time.dt

        if braking:
            #rapid decrease
            self.speed = max(self.speed - 8*time.dt, 0)

        if not pedal_is_pressed or (not speed_is_zero and changing_direction) or max_speed_dropped:
            #decrease
            self.speed = max(self.speed - 2*time.dt, 0)
        else:
            #increase
            self.speed = min(self.speed + self.xor(held_keys['w'], held_keys['s']) * 2 * time.dt, self.max_speed)

    def xor(self, a, b):
        if a==1 and b==1:
            return 0
        return max(a,b)

if __name__ == '__main__':

    app = Ursina()

    Entity(model='quad', scale=60, rotation=(90,0,0), texture='white_cube', texture_scale=(60, 60),
            color=color.light_gray)
    
    # Entity(model=Cone(4), position=(20,0,0), color=color.orange, collider='mesh')

    camera.orthographic = True
    camera.rotation = (90,0,0)
    camera.position = (0,40,0)

    car = Car()

    speedometer = Text(text=str(car.speed*25), position=(0,0,0), color = color.black)
    wheel = Entity(model='cube', texture='steering_wheel', position=(-30,0,15), scale=6)

    def update():
        speedometer.text = str(math.floor(car.speed*25))
        wheel.rotation = (0, car.rot, 0)

    app.run()
