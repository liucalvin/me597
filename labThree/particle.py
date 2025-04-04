
from mapUtilities import *
from utilities import *
from numpy import cos, sin
import numpy as np


class particle:

    def __init__(self, pose, weight):
        self.pose = pose
        self.weight = weight

    def motion_model(self, v, w, dt):
        #TODO: Implement the motion model for the particle
        """
        v: linear velocity
        w: angular velocity
        dt: time step
        """
        delta_theta = w * dt
        """
        noisev = np.random.normal(scale=0.01)
        noisew = np.random.normal(scale=0.01)
        noiset = np.random.normal(scale=0.01)

        vp = v + noisev
        wp = w + noisew
        
        self.pose[0] += (v / w) * (np.sin(self.pose[2] + delta_theta) - np.sin(self.pose[2]))
        self.pose[1] += (v / w) * (np.cos(self.pose[2]) - np.cos(self.pose[2] + delta_theta))
        self.pose[2] += delta_theta
        """
        
        self.pose[0] += v*dt*np.cos(self.pose[2]+(delta_theta/2))
        self.pose[1] += v*dt*np.sin(self.pose[2]+(delta_theta/2))
        self.pose[2] += delta_theta

    # TODO: You need to explain the following function to TA
    def calculateParticleWeight(self, scanOutput: LaserScan, mapManipulatorInstance: mapManipulator, laser_to_ego_transformation: np.array):

        T = np.matmul(self.__poseToTranslationMatrix(), laser_to_ego_transformation)

        _, scanCartesianHomo = convertScanToCartesian(scanOutput)
        scanInMap = np.dot(T, scanCartesianHomo.T).T

        likelihoodField = mapManipulatorInstance.getLikelihoodField()
        cellPositions = mapManipulatorInstance.position_2_cell(
            scanInMap[:, 0:2])

        lm_x, lm_y = likelihoodField.shape

        cellPositions = cellPositions[np.logical_and.reduce(
                (cellPositions[:, 0] > 0, -cellPositions[:, 1] > 0, cellPositions[:, 0] < lm_y,  -cellPositions[:, 1] < lm_x))]

        log_weights = np.log(
            likelihoodField[-cellPositions[:, 1], cellPositions[:, 0]])
        log_weight = np.sum(log_weights)
        weight = np.exp(log_weight)
        weight += 1e-10

        self.setWeight(weight)

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def setPose(self, pose):
        self.pose = pose

    def getPose(self):
        return self.pose[0], self.pose[1], self.pose[2]

    def __poseToTranslationMatrix(self):
        x, y, th = self.getPose()

        translation = np.array([[cos(th), -sin(th), x],
                                [sin(th), cos(th), y],
                                [0, 0, 1]])

        return translation
