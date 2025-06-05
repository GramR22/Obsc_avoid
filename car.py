import math
import numpy as np




class car:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.targetX = None
        self.targetY = None
        self.hasTarget = False
        self.path = []
        self.angle = 0
        self.velocity = 0
        self.max_velocity = 10
        self.min_velocity = -2
        self.is_accelerating = False
        self.is_decelerating = False


    def coast(self):
        decay = .95 * (1 - (abs(self.velocity)/self.max_velocity))
        self.velocity *= decay
        if abs(self.velocity) <.05:
            self.velocity = 0
        # this is used to simulate friction coasting
        # to ensure it doesnt get stuck aproachcing 0 forever it is hard set to 0 if < .05


    def turn_R(self, turn_value):
        self.angle += turn_value


    def turn_L(self, turn_value):
        self.angle -= turn_value


    def accel(self,acc_value):
        self.is_accelerating = True
        if self.velocity + acc_value > self.max_velocity:
            friction_coef = math.log1p(self.max_velocity - self.velocity) 
            self.velocity += acc_value * friction_coef
            self.velocity = np.clip(self.velocity,self.min_velocity,self.max_velocity)
        # np.clip enforces that is remains in the min and max
        # ensures it does not go above the maximum
        # log1p(x) = log(1 + x) this is a simulation of friction or the slow down of the car
        else:
            friction_coef = math.log1p(self.max_velocity - self.velocity)
            self.velocity += acc_value * friction_coef


    def decel(self, decel_value):
        self.is_decelerating = True
        if self.velocity - decel_value < self.min_velocity:
            friction_coef = math.log1p(abs(self.max_velocity + self.velocity)) 
            self.velocity += decel_value * friction_coef
            self.velocity = np.clip(self.velocity,self.min_velocity,self.max_velocity)
            #ensures it does not go below the minimum/reverse max
            #log1p(x) for the friction
        else:
            if self.velocity < 0:
                friction_coef = math.log1p(abs(self.min_velocity - self.velocity))
            else:
                friction_coef = math.log1p(abs(self.max_velocity - self.velocity))
            self.velocity -= decel_value * friction_coef
            #conditions for handling negetive numbers


    def update(self, acc_input = 0, steering_input = 0):

        self.angle += steering_input
        # adjusts the steering angle based off of an input from the ai model

        if acc_input > 0:
            if self.velocity + acc_input > self.max_velocity:
                friction_coef = math.log1p(self.max_velocity - self.velocity) 
                self.velocity += acc_input * friction_coef
                self.velocity = min(self.velocity,self.max_velocity)
                self.is_accelerating = True
                self.is_decelerating = False
                # np.clip enforces that is remains in the min and max
                # ensures it does not go above the maximum
                # log1p(x) = log(1 + x) this is a simulation of friction or the slow down of the car
            elif self.velocity + acc_input >= self.max_velocity:
                self.velocity = self.max_velocity
            else:
                friction_coef = math.log1p(self.max_velocity - self.velocity)
                self.velocity += acc_input * friction_coef

        elif acc_input < 0:
            if self.velocity + acc_input < self.min_velocity:
                friction_coef = math.log1p(abs(self.min_velocity - self.velocity))
                self.velocity += acc_input * friction_coef
                self.velocity = max(self.velocity,self.min_velocity)
                #ensures it does not go below the minimum/reverse max
                #log1p(x) for the friction
                
            else:
                if self.velocity < 0:
                    friction_coef = math.log1p(abs(self.min_velocity - self.velocity))
                else:
                    friction_coef = math.log1p(abs(self.max_velocity - self.velocity))
                self.velocity += acc_input * friction_coef
                #conditions for handling negetive numbers
            self.is_accelerating = False
            self.is_decelerating = True
        else:
            self.is_accelerating = False
            self.is_decelerating = False    
            self.coast()
      
        self.velocity = np.clip(self.velocity,self.min_velocity,self.max_velocity)
        # np.clip enforces that is remains in the min and max
        self.pos_Update()


    def pos_Update(self):
        dX = self.velocity * math.cos(self.angle)
        dY = self.velocity * math.sin(self.angle)
        self.x += dX
        self.y += dY
        
    
    def set_Target(self,target):
        if self.check_collision(grid) == False:
            self.targetX = target[0]
            self.targetY = target[1]
        else:
            pass
            # logic for getting new target


    def set_heading(self):
        self.angle = math.atan2(self.targetY - self.y, self.targetX - self.x)
        distance = math.sqrt(((self.targetX - self.x) ** 2) + ((self.targetY - self.y) ** 2))
        return distance
        # its a plus because it's euclidean distance


    def check_collision(self,grid):
        pass


    def scan_Grid(self):
        pass


    def render(self):
        pass