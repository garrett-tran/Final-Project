import cv2
import random
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1200
class Fruit:
    def __init__(self, type):
        self.type = type
        self.image = pygame.transform.scale(pygame.image.load('data/' + self.type + '.png'), (50, 50))
    
        self.start()
    
    # Resets fruits to a random height and width after they are collected or fall to the bottom
    def start(self):
        self.x = random.randint(50, SCREEN_WIDTH-50)
        self.y = random.randint(-500, 0)
    
    #Moves fruits down the screen every tick
    def update(self, speed):
        self.y += speed
        

class Game:
    def __init__(self):
        pygame.init()
        self.speed = 3
        self.score = 0 
        self.lives = 10
        self.font = pygame.font.Font(None, 35)
        self.key = pygame.transform.scale(pygame.image.load('data/key.png'), (100, 300))

        #Creating fruit objects and adding them to a list
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
        

       

        self.mode = self.apple
        

        width, height = 1200, 700
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Basket Game")
        self.clock = pygame.time.Clock()
    def basket(self):
        """ Lines 60-90 adapted from cowboy hat lab code"""
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

                y1, y2 = start_y-bk.shape[0], start_y
                x1, x2 = start_x, start_x + bk.shape[1]

                # Saving the alpha values (transparencies)
                alpha = bk[:, :, 3] / 255.0

                self.screen.blit(self.basket, (x1,y1))
                self.screen.blit(pygame.transform.scale_by(self.mode.image, 1.75), (x1+50, y1+5))
            pygame.display.flip()
            self.clock.tick(20)

            #Logic for displaying webcam using pygame
            surf = pygame.surfarray.make_surface(img_rgb)
            surf = pygame.transform.rotate(surf, -90)
            surf = pygame.transform.flip(surf, True, False)
            self.screen.blit(surf, (0,0))

            #Logic for displaying UI
            self.screen.blit(self.font.render("Score: " + str(self.score), True, (255, 0, 0)), (0, 10))
            self.screen.blit(self.font.render("Lives: " + str(self.lives), True, (255, 0, 0)), (0, 40))
            self.screen.blit(self.key, (0,70))

            
            #Logic for reseting fruit both after it is collected or if it falls to the bottom
            for fruit in self.fruits:
                self.screen.blit(fruit.image, (fruit.x, fruit.y))
                fruit.update(self.speed)

                if (fruit.x > x1 and fruit.x < x2)  and (fruit.y > y1 and fruit.y < y1 + 20) and self.mode == fruit:
                    fruit.start()
                    self.score +=1
                    self.speed +=0.2
                if fruit.y >= SCREEN_HEIGHT:
                    self.lives -=1
                    if self.lives == 0:
                        print("Score: " + str(self.score))
                        exit(0)
                        
                    fruit.start()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # Release the capture
                    video.release()
                    cv2.destroyAllWindows()
                    exit()
                if event.type == pygame.KEYDOWN:
                    #Logic for changing between being able to collect each fruit
                    if event.key == pygame.K_1:
                        self.mode = self.apple
                    if event.key == pygame.K_2:
                        self.mode = self.cherry
                    if event.key == pygame.K_3:
                        self.mode = self.orange
                    if event.key == pygame.K_4:
                        self.mode = self.avacado
                    if event.key == pygame.K_5:
                        self.mode = self.peach
                    

        

if __name__ == "__main__":
    g = Game()
    g.basket()