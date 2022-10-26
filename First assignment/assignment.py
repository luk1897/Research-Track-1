from __future__ import print_function

import time
from sr.robot import *

g_code_list=[]  # list for silver token code
s_code_list=[]  # list for golden token code

flag= True      # flag used to alternate between searching for the silver and golden tokens """

a_th = 2.0      # It is used for the control of the orientation (Float) """

s_th = 0.4      #It is used for the control of the linear distance from a silver token (Float) """

g_th = 0.5      #It is used for the control of the linear distance from a golden token (Float).
	        #This is important because between the robot and a golden token there is a silver token
	       

R = Robot()     #instance of the class Robot

def forward(speed, seconds):
    """
    
    Function for setting a linear velocity
    
    Parametres: speed of the wheels (int) and
    time interval (int) 
    
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    
    Function for setting an angular velocity
    
    Parametres: speed of the wheels (int) and
    time interval (int)
    
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    
    Function to find the closest silver token

    Returns: code of the token (int), distance of the token (int)
    and the angle between the robot and the token
    
    The function can return all -1 -1 -1 if no token is detected or 
    if the token has already been used 
    
    """
    distance=100
    for token in R.see():   #from see() we can find out all the informations we need
        if token.dist < distance and token.info.marker_type is MARKER_TOKEN_SILVER:     #thanks to the second condition, we can find only silver tokens
            code=token.info.code
            distance=token.dist
	    angle=token.rot_y
    if distance==100:
         return -1,-1,-1
    for x in s_code_list:   # token code check
            if x==code:
	        return -1, -1, -1
    return code, distance, angle
   	
def find_golden_token():
    """
    
    Function to find the closest golden token

    Returns: code of the token (int), distance of the token (int)
    and the angle between the robot and the token
    
    The function can return all -1 -1 -1 if no token is detected or 
    if the token has already been used 
    
    """
    distance=100
    for token in R.see():  
        if token.dist < distance and token.info.marker_type is MARKER_TOKEN_GOLD:  #thanks to the second condition, we can find only golden tokens
            code=token.info.code
            distance=token.dist
	    angle=token.rot_y
    if distance==100:
         return -1,-1,-1
    for x in g_code_list:     # token code check
            if x==code:
	        return -1, -1, -1
    return code, distance, angle


while 1:
    if len(g_code_list)==6:  # checking if the job is done because when the list has six code, the task is completed
       time.sleep(1)
       print("My job is done")
       exit(0)      
    if flag == True:   # here the function find_silver_token() starts
        code, distance, angle = find_silver_token()
    else :             # here the function golden_token() starts
        code, distance, angle = find_golden_token() 
    if distance==-1 or code == -1:        # if the distance or the code are -1, the robot turns to find a token
       print("I can see any token or the token has already used!")
       turn(+2, 0.5)
    elif distance < s_th and flag == True:   #condition to grab a silver token
            print("Silver token found!")
            R.grab() 
            s_code_list.append(code)   # after the silver token is grabbed, the silver token code is added to the list
            print("Taken!")
            flag=not flag              # thanks to it we can switch to the function which looks for golden tokens
    elif distance < g_th and flag == False:   #condition to release a silver token
            print("Golden token found!")
            R.release()
            g_code_list.append(code)      # after the silver token is released, the golden token code is added to the list
            print("Released!")  
            flag=not flag               # thanks to it we can switch to the function which looks for silver tokens
    elif -a_th<= angle <= a_th: # the robot go forward if it is aligned with the token
       print("Now I am aligned with the token!")
       forward(25, 0.5)
    elif angle < -a_th: # the robot needs to turn on the left or on the right if it is not aligned with the token
       print("Better turn on the left.")
       turn(-2, 0.5)
    elif angle > a_th:
       print("Better turn on the right.")
       turn(+2, 0.5)
    
        
        
        
        
    

