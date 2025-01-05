# "The Little Sibling" – A Mini Autonomous Car

## Description

"The Little Sibling" is a mini autonomous car designed and built with a **Raspberry Pi**, **Python**, and **OpenCV**. The car tracks and follows users wearing specific attributes (e.g., a colored object, a specific pattern, or a custom feature), using object detection and tracking algorithms powered by OpenCV. The camera, mounted on a servo motor, is controlled to adjust the car's view, allowing it to detect and follow the user as they move.

The car is equipped with motors controlled via **PWM (Pulse Width Modulation)** signaling, which allows precise control of its movement.

### Features:
- **3D-printed mini autonomous car**: Custom designed chassis and parts for the car.
- **Object detection and tracking**: Uses a camera and OpenCV to detect and follow specific user attributes (e.g., colors or patterns).
- **Camera mounted on a servo motor**: Adjusts the camera's view to track the user more effectively.
- **PWM motor control**: Controls the car’s movements (forward, backward, turns) using PWM signals.

## Technologies Used:
- **Python**: Programming language used for the control system and object detection algorithms.
- **OpenCV**: Library for computer vision and image processing tasks like object detection and tracking.
- **Raspberry Pi**: The computing platform that controls the car and processes the camera feed.
- **3D Printing**: Used to create the chassis and parts of the car.
- **PWM**: Used to control the motors and drive the car's movements.

## How to Run

To run this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/little-sibling-autonomous-car.git
    cd little-sibling-autonomous-car
    ```

2. Set up the Raspberry Pi:
    - Install **Python 3** and necessary libraries:
        ```bash
        sudo apt update
        sudo apt install python3-opencv python3-pip
        pip3 install RPi.GPIO
        ```

3. Connect the camera to the Raspberry Pi and mount it to a servo motor for adjusting the camera's angle.

4. Build and run the project:
    - Start the script to launch the car:
        ```bash
        python3 car_control.py
        ```

5. The car will begin detecting and tracking the specified attributes and follow the user accordingly.

## Project Structure

- `car_control.py`: Main script to control the car and process the camera feed.
- `servo_control.py`: Script to manage the servo motor and camera movement.
- `assets/`: Folder for any visual assets or example images used in object detection.
- `README.md`: Project description and instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

