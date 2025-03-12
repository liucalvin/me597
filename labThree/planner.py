
from math import sin,cos, atan2,atan
import math

POINT_PLANNER=0; TRAJECTORY_PLANNER=1

PARABOLA=0; SIGMOID=1

class planner:

    def __init__(self, type_, mapName="room"):

        self.type=type_
        self.mapName=mapName

    
    def plan(self, startPose, endPose):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(endPose)
        
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner(startPose, endPose)
        

    def point_planner(self, endPose):
        return (endPose[0], endPose[1])


    def trajectory_planner(self, startPose, endPose):
        # Temporary trajectory planner
        # For lab3, we only need to connect the start and end points with a straight line in the resolution of 0.2
        interpolation_resolution=0.2
        x0, y0 = startPose[0], startPose[1]
        x1, y1 = endPose[0], endPose[1]
        dx, dy = x1-x0, y1-y0
        distance = math.sqrt(dx*dx + dy*dy)
        steps = int(distance/interpolation_resolution)
        interpolated_points = []
        for i in range(steps):
            interpolated_points.append([x0 + dx/steps*i, y0 + dy/steps*i])
        return interpolated_points
    