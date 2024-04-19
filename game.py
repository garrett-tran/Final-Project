import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time as t

class Ball:
    def __init__(self, color, screen_width=600, screen_height=400):
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.respawn()

    def respawn(self):
        pass
    
    def draw(self):
        pass

class Game:
    def __init__(self):
        pass
    def draw_basket(self):
        pass
    def run(self):
        pass