# Assignment 1

## Pseudocode

` ` ` set flag for switching between the research of silver and golden tokens to true` ` ` 
<p>set the threshold for the control of the orientation to 2.0</p>
<p>set the threshold for the control of the linear distance from a silver token to 0.4</p>
<p>set the threshold for the control of the linear distance from a golden token to 0.5</p>
<p>set R to Robot()</p>

function forward with parameters speed and seconds
    set power of the left motor to speed
    set power of the right motor to speed
    set a sleep with seconds
    set zero the power of the left motor 
    set zero the power of the right motor
 
function turn with parameters speed and seconds
  set power of the left motor to speed
  set power of the right motor to minus speed
  set a sleep with seconds
  set zero the power of the left motor 
  set zero the power of the right motor
  
function find silver token without parameters 
  set distance to 100
  for each token in the function see
      if the token distance is less than the distance and the marker type of the token is equal to MARKER_TOKEN_SILVER
          add the token code to code
          add the token distance to distance
          add the angle between the token and the robot to angle
       endif
  endfor
  if  distance is equal to 100
       add -1 to code
       add -1 to distance
       add -1 to angle
  endif
  for each x in the list of the silver tokens
       if x is equal to code
          add -1 to code
          add -1 to distance
          add -1 to angle
       endif
  endfor
  
function find golden token without parameters
  set distance to 100
  for each token in the function see
      if the token distance is less than the distance and the marker type of the token is equal to MARKER_TOKEN_GOLDEN
          add the token code to code
          add the token distance to distance
          add the angle between the token and the robot to angle
       endif
  endfor
  if  distance is equal to 100
       add -1 to code
       add -1 to distance
       add -1 to angle
  endif
  for each x in the list of the golden tokens
       if x is equal to code
          add -1 to code
          add -1 to distance
          add -1 to angle
       endif
  endfor
  
while 1 is equal to 1
    if the number of the elements in the golden tokens list is equal to 6
       set sleep to 1
       print "My job is done"
       exit from the program
    endif
    if flag is equal to True 
       set code, distance and angle to the return of the function find_silver_token
    endif
    else
       set code, distance and angle to the return of the function find_golden_token
    endelse
    if distance is equal to -1 or code is equal to -1
       print "I can't see any token or the token has already used!"
       call turn with parametres +2, 0.5
    endif
    if distance is less than the threshold for the silver token and flag is equal to true
       print "Silver token found!"
       the robot grabs the token
       add the code of the silver token to the silver tokens list
       print "Taken"
       set flag to not flag
    endif
    if distance is less than the threshold for the golden token and flag is equal to false
       print "Golden token found!
       the robot releases the silver token
       add the code of the golden token to the golden tokens list
       print "Released"
       set flag to not flag
    endif
    if angle is greater than minus threshold for the orientation and angle is smaller than the threshold for the orientation
       print "Now I am aligned with the token!
       call forward with parameters 25, 0.5
    endif
    if angle is smaller than minus threshold for the orientation 
       print "Better turn on the left."
       call turn with -2, 0.5 in order to turn on the left
    endif
    if angle is greater than threshold for the orientation 
       print "Better turn on the right"
       call turn with -2, 0.5 on the right"
       
       
       
       
    




