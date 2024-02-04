from math import tan, inf

class CoordinateMap:
    def __init__(self, distance, middle_x, middle_y, screen_width, screen_height):

        # TODO: make sure that increase yaw and pitch correlate to increase in x and y
        
        # calibration_coordinates = [("x", "y", "yaw", "pitch"), ...]
        self.distance = distance
        self.middle_x = middle_x
        self.middle_y = middle_y
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_position(self, x, y, yaw, pitch):
        try:
            projected_x = self.screen_width / 2 + x - self.middle_x + self.distance / tan(yaw)
            projected_y = self.screen_height / 2 + y - self.middle_y + self.distance / tan(pitch)

            if projected_x < 0:
                projected_x = 0
            if projected_x > self.screen_width:
                projected_x = self.screen_width

            if projected_y < 0:
                projected_y = 0
            if projected_y > self.screen_height:
                projected_y = self.screen_height

            print(f"projected_x: {projected_x}, projected_y: {projected_y}")
            
            return (projected_x / self.screen_width, projected_y / self.screen_height)
        except (ZeroDivisionError, ValueError):
            return (0.5, 0.5)