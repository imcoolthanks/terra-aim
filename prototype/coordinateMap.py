from math import tan, inf

class CoordinateMap:
    def __init__(self, calibration_coordinates, distance: int):

        # TODO: make sure that increase yaw and pitch correlate to increase in x and y
        
        # calibration_coordinates = [("x", "y", "yaw", "pitch"), ...]
        self.distance = distance

        #     -----------------------(x2, y2)
        #    |                           |
        #    |                           |
        #    |                           |
        #    |                           |
        # (x1, y1)----------------------- 


        self.x1, self.y1, self.origin_yaw, self.origin_pitch = calibration_coordinates[0]
        
        try:
            self.x2 = calibration_coordinates[1][0] + self.distance / tan(calibration_coordinates[1][2] - self.origin_yaw)
            self.y2 = calibration_coordinates[1][1] + self.distance / tan(calibration_coordinates[1][3] - self.origin_pitch)
        except (ZeroDivisionError, ValueError):
            self.x2 = 100
            self.y2 = 100

    def get_position(self, x, y, yaw, pitch):

        try:
            (projected_x, projected_y) = (x + self.distance / tan(yaw - self.origin_yaw), y + self.distance / tan(pitch - self.origin_pitch))

            print(f"projected_x: {projected_x}, projected_y: {projected_y}")
            
            return ((projected_x - self.x1) / (self.x2 - self.x1),
                    (projected_y - self.y1) / (self.y2 - self.y1))
        except (ZeroDivisionError, ValueError):
            return (0.5, 0.5)