import RPi.GPIO as GPIO
from time import sleep

lin1 = 24
lin2 = 23
len1 = 25
len2 = 20
lin3 = 16
lin4 = 12

rin1 = 27
rin2 = 17
ren1 = 22
ren2 = 26
rin3 = 19
rin4 = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(lin1, GPIO.OUT)
GPIO.setup(lin2, GPIO.OUT)
GPIO.setup(len1, GPIO.OUT)
GPIO.output(lin1, GPIO.HIGH)
GPIO.output(lin2, GPIO.LOW)
GPIO.setup(lin3, GPIO.OUT)
GPIO.setup(lin4, GPIO.OUT)
GPIO.setup(len2, GPIO.OUT)
GPIO.output(lin3, GPIO.LOW)
GPIO.output(lin4, GPIO.HIGH)
lm1 = GPIO.PWM(len1, 1000)
lm2 = GPIO.PWM(len2, 1000)
GPIO.setup(rin1, GPIO.OUT)
GPIO.setup(rin2, GPIO.OUT)
GPIO.setup(ren1, GPIO.OUT)
GPIO.output(rin1, GPIO.HIGH)
GPIO.output(rin2, GPIO.LOW)
GPIO.setup(rin3, GPIO.OUT)
GPIO.setup(rin4, GPIO.OUT)
GPIO.setup(ren2, GPIO.OUT)
GPIO.output(rin3, GPIO.LOW)
GPIO.output(rin4, GPIO.HIGH)
rm1 = GPIO.PWM(ren1, 1000)
rm2 = GPIO.PWM(ren2, 1000)

lm1.start(0)
lm2.start(0)
rm1.start(0)
rm2.start(0)

def motor_drive(motor, speed):


  if motor == "right":
    rm1.ChangeDutyCycle(speed)
    rm2.ChangeDutyCycle(speed)

  if motor == "left":
    lm1.ChangeDutyCycle(speed)
    lm2.ChangeDutyCycle(speed)

def motor_cleanup():
  GPIO.cleanup()
