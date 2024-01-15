import cv2
import picamera2
import numpy as np
import main as motors

import RPi.GPIO as gp  
import pigpio
from time import sleep
import math

def nothing(x):
    pass

randomNum = 0

viewX = 320
viewY = 240
centerX = viewX / 2
camera_fov = 53.5
longestLength = 34
distanceTolerance = 5

servo = 18
servoAngle = 90
pixelTolerance = 10
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 50 )
pwm.set_servo_pulsewidth( servo, servoAngle / 180.0 * 2000 + 500)

# lower_pinkish_red = np.array([150, 50, 50])
# upper_pinkish_red = np.array([180, 255, 255])

winName = "frame"
cv2.namedWindow(winName)
# H, S,V are for Lower Boundaries
#H2,S2,V2 are for Upper Boundaries
cv2.createTrackbar('eps',winName,0,10000,nothing)
cv2.createTrackbar('R1',winName,0,255,nothing)
cv2.createTrackbar('G1',winName,0,255,nothing)
cv2.createTrackbar('B1',winName,0,255,nothing)
cv2.createTrackbar('R2',winName,0,255,nothing)
cv2.createTrackbar('G2',winName,0,255,nothing)
cv2.createTrackbar('B2',winName,0,255,nothing)

try:
    with picamera2.Picamera2() as picam2:
        config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (viewX, viewY)}, lores={"size": (320, 240), "format": "YUV420"})
        picam2.configure(config)

        (w0, h0) = picam2.stream_configuration("main")["size"]
        (w1, h1) = picam2.stream_configuration("lores")["size"]

        picam2.start(show_preview=False)

        while True:
            frame = picam2.capture_array("main")

            eps = (10000 - cv2.getTrackbarPos('eps', winName)) / 10000.0
            R1 = cv2.getTrackbarPos('R1', winName)
            G1 = cv2.getTrackbarPos('G1', winName)
            B1 = cv2.getTrackbarPos('B1', winName)
            R2 = cv2.getTrackbarPos('R2', winName)
            G2 = cv2.getTrackbarPos('G2', winName)
            B2 = cv2.getTrackbarPos('B2', winName)

            # lower_pinkish_red = np.array([R1, G1, B1])
            # upper_pinkish_red = np.array([R2, G2, B2])
            lower_pinkish_red = np.array([135, 155, 110])
            upper_pinkish_red = np.array([200, 255, 255])

            eps = 0.025

            # Convert the frame to grayscale (AprilTags work better in grayscale)

            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            # contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsvFrame, lower_pinkish_red, upper_pinkish_red)
            result = cv2.bitwise_and(frame, frame, mask=mask)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            avgX = 0
            maxLength = 0
            for contour in contours:
                # x, y, w, h = cv2.boundingRect(contour)
                # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                epsilon = eps * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                lengths = []
                tempStart = (0, 0)
                tempEnd = (0, 0)
                for i in range(len(approx)):
                    start_point = tuple(approx[i][0])
                    tempStart = start_point
                    end_point = tuple(approx[(i + 1) % len(approx)][0])
                    tempEnd = end_point

                    combinedLengths = tuple(np.subtract(start_point, end_point))
                    x = abs(start_point[0] - end_point[0])
                    y = abs(start_point[1] - end_point[1])
                    avgX = avgX + start_point[0] + end_point[0]
                    # lengths.append((0.41421356237 * x) + y)
                    maxLength = max(maxLength, math.sqrt(pow(x, 2) + pow(y, 2)))
                    # print(lengths[i])
                avgX = avgX * 1.0 / len(approx)


                # Draw the lines of the quadrilateral
                cv2.polylines(frame, [approx], True, (0, 255, 0), 2)
                # print(maxLength)
                # cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

            # if (avgX < centerX - pixelTolerance):
                # servoAngle = servoAngle + 1
            # elif (avgX  > centerX + pixelTolerance):
                # servoAngle = servoAngle - 1

            if (servoAngle > 180):
                servoAngle = 180
            if(servoAngle < 0):
                servoAngle = 0

            speedLeft = servoAngle / 90.0
            speedRight = (180 - servoAngle) / 90.0
            maxSpeed = max(speedLeft, speedRight)
            speedLeft = speedLeft * 100.0 / maxSpeed
            speedRight = speedRight * 100.0 / maxSpeed

            # servoAngle = (x + w/2.0) * 53.5 / viewX + 63.25
            # print(servoAngle)
            pwm.set_servo_pulsewidth( servo, servoAngle / 180.0 * 2000 + 500)

            speedLeft = 100.0
            speedRight = 100.0

            if (longestLength - maxLength > distanceTolerance and maxLength > 0):
                # if (speedLeft > speedRight):
                #     speedLeft = 100
                #     speedRight = 0
                # else:
                #     speedRight = 100
                #     speedLeft = 0
                motors.motor_drive("left", speedLeft)
                motors.motor_drive("right", speedRight)
                # print("DRIVE!!!\n", randomNum)
                # randomNum += 1
            else:
                motors.motor_drive("left", 0)
                motors.motor_drive("right", 0)

            motors.motor_drive("left", 0)
            motors.motor_drive("right", 100)
            

            # edges = cv2.Canny(mask, 50, 150)
            # lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=50)
            # for line in lines:
            #     rho, theta = line[0]
            #     a = np.cos(theta)
            #     b = np.sin(theta)
            #     x0 = a * rho
            #     y0 = b * rho
            #     x1 = int(x0 + 1000 * (-b))
            #     y1 = int(y0 + 1000 * (a))
            #     x2 = int(x0 - 1000 * (-b))
            #     y2 = int(y0 - 1000 * (a))
            #     cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Display the frame with detections
            cv2.imshow(winName, frame)
            cv2.imshow("mask", mask)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

except KeyboardInterrupt:
    # Close the OpenCV window
    cv2.destroyAllWindows()
    motors.motor_cleanup()

    pwm.set_PWM_dutycycle( servo, 0 )
    pwm.set_PWM_frequency( servo, 0 )
    pwm.write(servo, 0)
    pwm.stop()
