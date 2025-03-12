# Type of planner
import numpy as np

POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        print("point planner")
        return x, y

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self, trajectory_type="sigmoid"):
        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]
        trajectory = []

        if trajectory_type == "parabola":
            x_values = np.linspace(0.0, 1.5, num=20)
            trajectory = [[x, x**2] for x in x_values]

        elif trajectory_type == "sigmoid":
            x_values = np.linspace(0.0, 2.5, num=20)
            trajectory = [[x, 2 / (1 + np.exp(-2 * x)) - 1] for x in x_values]
        print(f"traj type {type(trajectory)}")
        return trajectory

