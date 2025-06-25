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
        self.Intergral_E = 0
        self.derivitave_E = 0
        self.previous_E = 0
        self.Sintegral_E = 0
        self.Sderivative_E = 0
        self.Sprevious_E = 0

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

    def get_mappedGrid(self):
        return self.mapped_Grid

    def coast(self):
        decay = .95 * (1 - (abs(self.velocity)/self.max_velocity))
        self.velocity *= decay
        if abs(self.velocity) <.05:
            self.velocity = 0
        # this is used to simulate friction coasting
        # to ensure it doesnt get stuck aproachcing 0 forever it is hard set to 0 if < .05


    def steerin_pid(self,dt  = .1):
        if self.targetX is None or self.targetY is None:
            return 0
        desired_angle = math.atan2(self.targetY - self.y, self.targetX - self.x)
        # gives desired angle from atan2(delta Y, delta X)
        
        # atan2 returns the angle of a vector from 0,0 
        
        
        angle_error = desired_angle - self.angle
        # proportional Error (P)
        # if the car is far off course this number should be huge if it is not it will be smaller


        angle_error = (angle_error + math.pi) % (2* math.pi) - math.pi
        # normalize it from -pi , pi

        self.AIntergral_E += angle_error * dt
        self.Aderivitave_E = (angle_error - self.Aprevious_E)/dt
        self.Aprevious_E = angle_error
        # calculations for intergral error and derivitive error
        # need to track error because it will be constantly checking as adustments are made



        output = (self.kp * angle_error + self.ki * self.AIntergral_E + self.kd* self.Aderivitave_E)
        
        return output

    def speed_pid(self, dt=0.1):
        distance = self.set_heading()

        if distance < 0.5:  # if very close, no more speed needed
            return 0

        # PID calculations
        self.Sintegral_E += distance * dt
        self.Sderivative_E = (distance - self.Sprevious_E) / dt
        self.Sprevious_E = distance

        # PID output: acceleration input
        output = (self.kp * distance +self.ki * self.Sintegral_E +self.kd * self.Sderivative_E)
        return output



    def update(self, dt = .1):

        acc_input = self.speed_pid(dt)
        steering_input = self.steerin_pid(dt)
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