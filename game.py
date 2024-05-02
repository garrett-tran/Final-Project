import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time as t
from matplotlib import pyplot as plt
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
class Fruit:
    def __init__(self, type, screen_width=1200, screen_height=700):
        self.type = type
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.transform.scale(pygame.image.load('data/' + self.type + '.png'), (50, 50))
    
        self.start()

    
    def start(self):
        self.x = random.randint(50, self.screen_width-50)
        self.y = random.randint(-150, 0)
    
    def update(self, speed):
        self.y += speed
        if self.y >= self.screen_height:
            self.start()

class Game:
    def __init__(self):
        pygame.init()
        self.fruits = []
        self.apple = Fruit("fruit")
        self.fruits.append(self.apple)
        self.cherry = Fruit("cherry")
        self.fruits.append(self.cherry)
        self.orange = Fruit("orange")
        self.fruits.append(self.orange)
        self.avacado = Fruit("avacado")
        self.fruits.append(self.avacado)
        self.peach = Fruit("peach")
        self.fruits.append(self.peach)
        self.speed = 5
        self.score = 0 

        self.font = pygame.font.Font(None, 35)
        

        width, height = 1200, 700
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Basket Game")
        self.clock = pygame.time.Clock()
    def basket(self):
        # Load the overlay image with an alpha channel (transparency)
        bk = cv2.imread('data/basket.png', -1)
        self.basket = pygame.image.load('data/basket.png')
        # Capture video from the webcam
        video = cv2.VideoCapture(0)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        x1, x2 = 0, 0
        y1, y2 = 0, 0

    
        while True:
            frame = video.read()[1]
            frame = cv2.flip(frame, 1)
            # OpenCV reads images as BGR, we want gray and rgb
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Find faces in the image
            faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minSize=(100,100))

            # Loop through each face found
            for (start_x, start_y, width, height) in faces:

                # Where to place the cowboy hat on the screen
                y1, y2 = start_y-bk.shape[0], start_y
                x1, x2 = start_x, start_x + bk.shape[1]

                # Saving the alpha values (transparencies)
                alpha = bk[:, :, 3] / 255.0

                """ Overlays the image onto the frame (Don't change this)
                for c in range(0, 3):
                    frame[y1:y2, x1:x2, c] = (alpha * bk[:, :, c] +
                                            (1.0 - alpha) * frame[y1:y2, x1:x2, c])
                """
                self.screen.blit(self.basket, (x1,y1))
            pygame.display.flip()
            self.clock.tick(20)
            surf = pygame.surfarray.make_surface(img_rgb)
            surf = pygame.transform.rotate(surf, -90)
            surf = pygame.transform.flip(surf, True, False)
            self.screen.blit(surf, (0,0))
            self.screen.blit(self.font.render("Score: " + str(self.score), True, (255, 0, 0)), (0, 100))

            
            
            for fruit in self.fruits:
                self.screen.blit(fruit.image, (fruit.x, fruit.y))
                fruit.update(self.speed)

                if (fruit.x > x1 and fruit.x < x2)  and (fruit.y > y1 and fruit.y < y1 + 20):
                    fruit.start()
                    self.score +=1
                    self.speed +=0.2
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # Release the capture
                    video.release()
                    cv2.destroyAllWindows()
                    exit()
                    
                # Display the resulting frame
            #cv2.imshow('Cowboy Hat', frame)
            
            # Break the loop when 'q' is pressed
            #if cv2.waitKey(50) & 0xFF == ord('q'):
            #   break

        

if __name__ == "__main__":
    g = Game()
    g.basket()