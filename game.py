from ursina import *

# class Car(Entity):
#     def __init__(self):
#         super().__init__()

if __name__ == '__main__':

    app = Ursina()

    Entity(model='quad', scale=60, rotation=(90,0,0), texture='white_cube', texture_scale=(60, 60),
            color=color.light_gray)
    
    box = Entity(model='cube', position=(20,0,0), color=color.orange, collider='mesh')

    camera.orthographic = True
    camera.rotation = (90,0,0)
    camera.position = (0,40,0)

    model,texture = 'car', 'car_texture'
    car = Entity(model=model, texture=texture, scale=0.6, rotation=(0,0,0), collider='box')
    car.speed = 0
    car.max_speed = 4
    car.dir = 1
    car.rot = 0

    speedometer = Text(text=str(car.speed*25), position=(0,0,0), color = color.black)
    wheel = Entity(model='cube', texture='steering_wheel', position=(0,0,16), scale=6)

    def input(key):

        if key=='left shift':
            car.max_speed = 12 - car.max_speed # double/halve the speed (4 -> 8 -> 4)

    def update():
        speedometer.text = str(math.floor(car.speed*25))
        wheel.rotation = (0, car.rot, 0)

        speed_is_zero = car.speed==0
        crashed = car.intersects()
        rotation_in_radians = car.rotation_y*pi/180
        turning = max(held_keys['d'], held_keys['a'])==1
        low_speed = car.speed < 4
        braking = held_keys['left control']==1
        pedal_is_pressed = xor(held_keys['w'], held_keys['s'])==1 # only one, not both
        changing_direction = not car.dir==held_keys['w'] - held_keys['s']
        max_speed_dropped = car.speed>car.max_speed
        
        if speed_is_zero:
            car.dir = held_keys['w'] - held_keys['s']

        if crashed:
            car.speed = 0
            car.z -= car.dir * math.cos(rotation_in_radians) * time.dt
            car.x -= car.dir * math.sin(rotation_in_radians) * time.dt

        car.z += car.dir * car.speed * math.cos(rotation_in_radians) * time.dt
        car.x += car.dir * car.speed * math.sin(rotation_in_radians) * time.dt

        if turning:
            car.rot =  min(max(car.rot + (held_keys['d'] - held_keys['a'])*2, -120), 120)
        else:
            if car.rot > 0:
                car.rot = max(car.rot - 128*time.dt, 0)
            else:
                car.rot = min(car.rot + 128*time.dt, 0)

        if not crashed:
            if low_speed:
                #turn steadily
                car.rotation_y += car.dir * car.rot * car.speed/4 * time.dt
            else:
                #turn normally
                car.rotation_y += car.dir * car.rot * time.dt

        if braking:
            #rapid decrease
            car.speed = max(car.speed - 8*time.dt, 0)

        if not pedal_is_pressed or (not speed_is_zero and changing_direction) or max_speed_dropped:
            #decrease
            car.speed = max(car.speed - 2*time.dt, 0)
        else:
            #increase
            car.speed = min(car.speed + xor(held_keys['w'], held_keys['s']) * 2 * time.dt, car.max_speed)

    def xor(a, b):
        if a==1 and b==1:
            return 0
        return max(a,b)

    app.run()
