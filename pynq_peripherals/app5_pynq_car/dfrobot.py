class PynqCar():
    def __init__(self, left_motor, right_motor):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.speed = 0
        self.speed_offset = 0
        self.speed_diff = 0
        self.stop()
        
    def set_speed(self, speed):
        if (abs(speed)+abs(self.speed_offset)+abs(self.speed_diff) < 100):
            self.speed = speed
            left_speed = self.speed+self.speed_offset+self.speed_diff
            right_speed = self.speed-self.speed_offset-self.speed_diff
            if left_speed < 0:
                self.left_motor.backward()
                self.left_motor.set_speed(0-left_speed)
            else:
                self.left_motor.forward()
                self.left_motor.set_speed(left_speed)
            if right_speed < 0:
                self.right_motor.backward()
                self.right_motor.set_speed(0-right_speed)
            else:
                self.right_motor.forward()
                self.right_motor.set_speed(right_speed)
        else:
            print("Error: Speed must be -100 to 100")
            
    def stop(self):
        self.right_motor.set_speed(0)
        self.left_motor.set_speed(0)
        
    def steering(self, diff):
        self.speed_diff = diff
        self.set_speed(self.speed)