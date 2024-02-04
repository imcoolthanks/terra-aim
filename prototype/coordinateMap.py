from math import tan, inf

class CoordinateMap:
    def __init__(self, distance, screen_width, screen_height):

        # TODO: make sure that increase yaw and pitch correlate to increase in x and y
        
        # calibration_coordinates = [("x", "y", "yaw", "pitch"), ...]
        self.distance = distance
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_position(self, x, y, yaw, pitch):
        try:
            projected_x = self.screen_width / 2 + self.distance / tan(yaw)
            projected_y = self.screen_height / 2 + self.distance / tan(pitch)

            print(f"projected_x: {projected_x}, projected_y: {projected_y}")
            
            return (projected_x / self.screen_width, projected_y / self.screen_height)
        except (ZeroDivisionError, ValueError):
            return (0.5, 0.5)