# Obsc_avoid
autnomous simulation

---------Car class---------
    -needs to have x,y so it can show up on the gird
    
    
    -needs to have variables for the angle(direction the car is pointed){uses radians}
    
    
    -needs to have a varble for vehicle velocity


Methods  
    -needs method for acceleration and deceleration
    -needs method to update its postion on the grid
    -needs a method to adjust the angle(Turn Left or Right) of the car
    
accel/decel
    -needs to limit top speed and minimum speed or reverse speed

update
    -needs to change the angle of the car by using cos to turn right and sin to turn left
    -uses polar equations to determine the direction of the vehicle
    RIGHT
        velocity + cos(angle)
    
    LEFT
        velocity + sin(angle)