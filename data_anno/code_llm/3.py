import numpy as np

class PIDController:
    """
    Generic PID controller class for various control systems.
    """

    def __init__(self, kp, ki=0, kd=0, error_limit=1, deriv_limit=1, integral_limit=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_limit = error_limit
        self.deriv_limit = deriv_limit
        self.integral_limit = integral_limit
        self.reset()

    def reset(self):
        self.integral = 0
        self.prev_error = 0
        self.last_time = 0

    def update(self, error, dt):
        """
        Updates the PID controller with the current error and time step.
        """
        if dt == 0:
            return 0  # Avoid division by zero

        self.integral += error * dt
        if self.integral_limit is not None:
            self.integral = np.clip(self.integral, -self.integral_limit, self.integral_limit)

        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        output = self.kp * np.clip(error, -self.error_limit, self.error_limit) + self.ki * self.integral \
            + self.kd * np.clip(derivative, -self.deriv_limit, self.deriv_limit)
        return output


class DroneVelocityFixedHeightController:
    """
    PID controller for fixed-height velocity control of a drone.
    """

    def __init__(self):
        gains = {"kp_att_y": 1, "kd_att_y": 0.5, "kp_att_rp": 0.5, "kd_att_rp": 0.1,
                 "kp_vel_xy": 2, "kd_vel_xy": 0.5, "kp_z": 10, "ki_z": 5, "kd_z": 5}

        self.vx_pid = PIDController(gains["kp_vel_xy"], kd=gains["kd_vel_xy"])
        self.vy_pid = PIDController(gains["kp_vel_xy"], kd=gains["kd_vel_xy"])
        self.alt_pid = PIDController(gains["kp_z"], gains["ki_z"], gains["kd_z"], integral_limit=2)
        self.pitch_pid = PIDController(gains["kp_att_rp"], kd=gains["kd_att_rp"])
        self.roll_pid = PIDController(gains["kp_att_rp"], kd=gains["kd_att_rp"])
        self.yaw_pid = PIDController(gains["kp_att_y"], kd=gains["kd_att_y"])

        self.last_time = 0  

    def control(self, dt, desired_vx, desired_vy, desired_yaw_rate, desired_altitude, 
                      actual_roll, actual_pitch, actual_yaw_rate, actual_altitude, actual_vx, actual_vy):

        # Velocity Control
        desired_pitch = self.vx_pid.update(desired_vx - actual_vx, dt)
        desired_roll = -self.vy_pid.update(desired_vy - actual_vy, dt)

        # Altitude Control
        alt_command = self.alt_pid.update(desired_altitude - actual_altitude, dt) + 48

        # Attitude Control
        roll_command = self.roll_pid.update(desired_roll - actual_roll, dt)
        pitch_command = -self.pitch_pid.update(desired_pitch - actual_pitch, dt)
        yaw_command = self.yaw_pid.update(desired_yaw_rate - actual_yaw_rate, dt)

        # Motor mixing
        m1 = alt_command - roll_command + pitch_command + yaw_command
        m2 = alt_command - roll_command - pitch_command - yaw_command
        m3 = alt_command + roll_command - pitch_command + yaw_command
        m4 = alt_command + roll_command + pitch_command - yaw_command

        # Limit the motor command
        m1 = np.clip(m1, 0, 600)
        m2 = np.clip(m2, 0, 600)
        m3 = np.clip(m3, 0, 600)
        m4 = np.clip(m4, 0, 600)

        return [m1, m2, m3, m4]
    

pid = DroneVelocityFixedHeightController()
motor_outputs = pid.control(0.032, 0.2, 0, 0, 0, 0, 0, 0, 1.0, 0, 0)
print("\nMotor outputs are: ", motor_outputs, "\n")