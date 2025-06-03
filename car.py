import math
import numpy as np




class car:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.max_velocity = 10
        self.min_velocity = -2


    def turn_R(self, turn_value):
        self.angle += turn_value


    def turn_L(self, turn_value):
        self.angle -= turn_value


    def accel(self,acc_value):
        if self.velocity + acc_value > self.max_velocity:
            friction_coef = math.log1p(self.max_velocity - self.velocity) 
            self.velocity += acc_value * friction_coef
            np.clip(self.velocity,self.min_velocity,self.max_velocity)

        # np.clip enforces that is remains in the min and max
        # ensures it does not go above the maximum
        # log1p(x) = log(1 + x) this is a simulation of friction or the slow down of the car
        else:
            friction_coef = math.log1p(self.max_velocity - self.velocity)
            self.velocity += acc_value * friction_coef


    def decel(self, decel_value):
        if self.velocity - decel_value < self.min_velocity:
            friction_coef = math.log1p(abs(self.max_velocity + self.velocity)) 
            self.velocity += decel_value * friction_coef
            np.clip(self.velocity,self.min_velocity,self.max_velocity)
            #ensures it does not go below the minimum/reverse max
            #log1p(x) for the friction
        else:
            if self.velocity < 0:
                friction_coef = math.log1p(abs(self.min_velocity - self.velocity))
            else:
                friction_coef = math.log1p(abs(self.max_velocity - self.velocity))
            self.velocity -= decel_value * friction_coef
            #conditions for handling negetive numbers

    
    def update(self):
        dx = self.velocity * math.cos(self.angle)
        dy = self.velocity * math.sin(self.angle)
        self.pos_Update(dx, dy)


    def pos_Update(self, dX, dY):
        self.x += dX
        self.y += dY
        