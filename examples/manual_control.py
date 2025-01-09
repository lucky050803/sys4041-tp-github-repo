# Quick and dirty example for manual keyboard robot control

import sys,tty,os,termios,fcntl
import random
import time
import json
import atexit
import pigpio

pin_backward_left = 25
pin_backward_right = 17
pin_forward_left = 23
pin_forward_right = 22

# steering offset for f-up robots
heading_bias = -12

def printObjectNicely(obj):
    count=1
    if(type(obj)==list):
        for i in obj:
            print("\t "+ ("BLOCK_" if i.type=="BLOCK" else "ARROW_")+str(count)+" : "+ json.dumps(i.__dict__))
            count+=1
    else:
        print("\t "+ ("BLOCK_" if obj.type=="BLOCK" else "ARROW_")+str(count)+" : "+ json.dumps(obj.__dict__))

def avancer(vitesse=100):
    pi.set_PWM_dutycycle(pin_forward_left, vitesse+heading_bias)
    pi.set_PWM_dutycycle(pin_forward_right, vitesse-heading_bias)
    pi.set_PWM_dutycycle(pin_backward_left, 0)
    pi.set_PWM_dutycycle(pin_backward_right, 0)

def reculer(vitesse=100):
    pi.set_PWM_dutycycle(pin_forward_left, 0)
    pi.set_PWM_dutycycle(pin_forward_right, 0)
    pi.set_PWM_dutycycle(pin_backward_left, vitesse+heading_bias)
    pi.set_PWM_dutycycle(pin_backward_right, vitesse-heading_bias)

def gauche(vitesse=100):
    pi.set_PWM_dutycycle(pin_forward_left, 0)
    pi.set_PWM_dutycycle(pin_forward_right, vitesse)
    pi.set_PWM_dutycycle(pin_backward_left, vitesse)
    pi.set_PWM_dutycycle(pin_backward_right, 0)

def droite(vitesse=100):
    pi.set_PWM_dutycycle(pin_forward_left, vitesse)
    pi.set_PWM_dutycycle(pin_forward_right, 0)
    pi.set_PWM_dutycycle(pin_backward_left, 0)
    pi.set_PWM_dutycycle(pin_backward_right, vitesse)

def stop():
    pi.set_PWM_dutycycle(pin_forward_left, 0)
    pi.set_PWM_dutycycle(pin_forward_right, 0)
    pi.set_PWM_dutycycle(pin_backward_left, 0)
    pi.set_PWM_dutycycle(pin_backward_right, 0)

def getkey():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  c = None
  try:
    c = sys.stdin.read(1)
  except IOError: pass

  termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

  return c

def getkey_nb():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  c = None

  try:
    c = sys.stdin.read(1)
  except IOError: pass

  termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

  return c

pi = pigpio.pi()

spd = 100

c = 0

keypress_timer = 0
prev_time = time.time_ns()

try:
    while True:
        k = getkey_nb()
        keypress_timer += time.time_ns() - prev_time
        prev_time = time.time_ns()
        #print(keypress_timer/1000000000)

        #print(k)
        if k == 'esc':
            quit()
        if k == 'q' :
            print('Turning LEFT')
            gauche(int(spd/1.5))
            keypress_timer = 0
        if k == 'd' :
            print('Turning RIGHT')
            droite(int(spd/1.5))
            keypress_timer = 0
        if k == 'z' :
            print('Moving FORWARD')
            avancer(spd)
            keypress_timer = 0
        if k == 's' :
            print('Moving BACKWARD')
            reculer(spd)
            keypress_timer=0
        if k == '' and keypress_timer > 0.05*1000000000:
            #print(f'stop count = {c}')
            stop()
            keypress_timer=0
            #print(keypress_timer)
            #c += 1
            #print(c)
            

        time.sleep(0.01)
            #print(k)
except (KeyboardInterrupt, SystemExit):
    os.system('stty sane')
    stop()
    print('stopping.')
