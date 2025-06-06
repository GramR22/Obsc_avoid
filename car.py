import math
import numpy as np

grid = np.zeros((30, 30), dtype=int)
grid[10, 5:25] = 1
grid[5:20, 15] = 1
grid[25:28, 25:28] = 1



class car:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.targetX = None
        self.targetY = None
        self.hasTarget = False
        self.path = []
        self.mapped_Grid = np.full((30,30),-1,dtype=int)
        self.angle = 0
        self.scanangles = [0,math.pi/6,math.pi/4,math.pi/3,math.pi/2,
                           2*(math.pi)/3,3*(math.pi)/4,5*(math.pi)/6,
                           math.pi,7*(math.pi)/6,5*(math.pi)/4,
                           4*(math.pi)/3,3*(math.pi)/2,5*(math.pi)/3,
                           7*(math.pi)/4,11*(math.pi)/6]
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


    def update(self, acc_input = 0, steering_input = 0):

        self.angle += steering_input
        # adjusts the steering angle based off of an input from the ai model

        if acc_input > 0:
        
            friction_coef = math.log1p(self.max_velocity - self.velocity) 
            self.velocity += acc_input * friction_coef
            self.velocity = min(self.velocity,self.max_velocity)
            self.is_accelerating = True
            self.is_decelerating = False
            # np.clip enforces that is remains in the min and max
            # ensures it does not go above the maximum
            # log1p(x) = log(1 + x) this is a simulation of friction or the slow down of      		the car


        elif acc_input < 0:
            #ensures it does not go below the minimum/reverse max
            #log1p(x) for the friction
                
            friction_coef = math.log1p(abs(self.min_velocity - self.velocity))
    
            self.velocity += acc_input * friction_coef	
            self.velocity = max(self.velocity,self.min_velocity)
            self.is_accelerating = False
            self.is_decelerating = True
        else:
            self.is_accelerating = False
            self.is_decelerating = False    
            self.coast()
    
        self.pos_Update()


    def pos_Update(self):
        dX = self.velocity * math.cos(self.angle)
        dY = self.velocity * math.sin(self.angle)
        self.x += dX
        self.y += dY
        
    
    def set_Target(self,target):
        if self.check_collision(grid,target) == False:
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


    def check_collision(self,grid,target):
        if grid[target[1]][target[0]] == 1:
            return True
        else:
            return False


    def scan_Grid(self):
        for pulse in self.scanangles:
            for i in (1,2):
                grid_X = int(self.x + i * math.cos(pulse))
                grid_Y = int(self.y + i * math.sin(pulse))
                # uses basic polar equations to determin the area to scan and where
                # because it is scaning at a radius of 2 it will check 1 then two for each given angle

                if not (0 <= int(grid_X) < 30 and 0 <= int(grid_Y) < 30):
                    break
                    # if its below 0 or above 30 it is not in the grid as i made it 30 x 30
                if grid[grid_Y][grid_X] == 1:
                    self.mapped_Grid[grid_Y][grid_X] = 1
                    break
                    # something is here :O
                else:
                    self.mapped_Grid[grid_Y][grid_X] = 0
                    # nothing in this area


    def render(self):
        pass