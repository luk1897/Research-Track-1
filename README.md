# Assignment 1

## Project Goal
The robot must take each silver token, approach a gold token and release it next to it, but tokens must only be considered once.

## How to install and run

### Installing
The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

### Running
Run this command on your shell: ```python2 run.py assignment.py```

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```
## Functions

``` python
def forward(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
This function allows the robot to move forward.

``` python
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0 
```
This function allows the robot to rotate.

``` python
def find_silver_token():
    distance=100
    for token in R.see():   
        if token.dist < distance and token.info.marker_type is MARKER_TOKEN_SILVER:     
            code=token.info.code
            distance=token.dist
	    angle=token.rot_y
    if distance==100:
         return -1,-1,-1
    for x in s_code_list:  
            if x==code:
	        return -1, -1, -1
    return code, distance, angle
```
This function allows the robot to find a silver token which has not found by the robot yet.

``` python	
def find_golden_token():
    distance=100
    for token in R.see():  
        if token.dist < distance and token.info.marker_type is MARKER_TOKEN_GOLD:  
            code=token.info.code
            distance=token.dist
	    angle=token.rot_y
    if distance==100:
         return -1,-1,-1
    for x in g_code_list: 
            if x==code:
	        return -1, -1, -1
    return code, distance, angle
```
This function allows the robot to find a golden token which has not found by the robot yet.

``` python
def grab_silver_token(code):
    print("Silver token reached!")
    R.grab() 
    s_code_list.append(code)
    print("Taken!")
```
This function allows the robot to grab a silver token.

``` python
def release_silver_token(code):
    print("Golden token reached!")
    R.release()
    g_code_list.append(code)
    print("Released!")  
```
This function allows the robot to release a silver token.

## Pseudocode

```
set flag for switching between the research of silver and golden tokens to true
set the threshold for the control of the orientation to 2.0
set the threshold for the control of the linear distance from a silver token to 0.4
set the threshold for the control of the linear distance from a golden token to 0.5
set R to Robot()

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
  
function grab silver token with parameter code of the silver token
  print "Silver token reached!"
  the robot grabs the token
  add the code of the silver token to the silver tokens list
  print "Taken"
  
function release silver token with parameter code of the golden token
  print "Golden token reached!"
  the robot releases the silver token
  add the code of the golden token to the golden tokens list
  print "Released"
  
while 1 is equal to 1
    if the number of the elements in the golden tokens list is equal to 6
       call turn with parametres +15, 3
       call forward with parameters 25, 3
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
       call turn with parametres +10, 0.1
    endif
    if distance is less than the threshold for the silver token and flag is equal to true
       call grab silver token with parameter code of the silver token
       set flag to not flag
    endif
    if distance is less than the threshold for the golden token and flag is equal to false
       call release silver token with parameter code of the golden token
       set flag to not flag
    endif
    if angle is greater than minus threshold for the orientation and angle is smaller than the threshold for the orientation
       print "Now I am aligned with the token!
       call forward with parameters 25, 0.5
    endif
    if angle is smaller than minus threshold for the orientation 
       print "Better turn on the left."
       call turn with -10, 0.1 in order to turn on the left
    endif
    if angle is greater than threshold for the orientation 
       print "Better turn on the right"
       call turn with +10, 0.1 on the right" 
```

## Output   
  ![output_assignment1_rstrack1](https://user-images.githubusercontent.com/80416766/199982984-02839a13-a6ac-4049-b16c-48246ef6afd0.png)

## Possible improvements
* The maximum distance within which the robot sees could be increased in order to make its vision more efficient, although, in this case, the environment would have to be enlarged to prove its effectiveness.
* Another possible improvement would be to allow the robot to find the nearest token because, at present, the robot rotates to one side when looking for a token and does not always see the one closest to it.
       
       
    




