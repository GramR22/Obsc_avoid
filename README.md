# Obsc_avoid
autnomous simulation

---------Car class---------
    -needs to have x,y so it can show up on the gird
    
    
    -needs to have variables for the angle(direction the car is pointed){uses radians}
    
    
    -needs to have a varble for vehicle velocity


Methods  
    -logic for coasting
    -method for acceleration and deceleration
    -method to update its postion on the grid
    -method to adjust the angle(Turn Left or Right) of the car
    
accel/decel
    -limit top speed and minimum speed or reverse speed

update
    -calls coasting fucntion to simulate rolling friction
    -change the angle of the car by using cos to turn right and sin to turn left
    -uses polar equations to determine the direction of the vehicle
    RIGHT
        velocity + cos(angle)
    
    LEFT
        velocity + sin(angle)


Simulated lidar
    used unit circle and polar cordinates to scan 360 degrees


Collision logic
    checks a main grid for collisions based on where it is and where it plans to go
    ...

Studied Controls and how it works.
    https://www.digikey.com/en/maker/tutorials/2024/implementing-a-pid-controller-algorithm-in-python
    https://www.youtube.com/watch?v=XfAt6hNV8XM&t=8s 
