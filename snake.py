from pygame.locals import *
import pygame
import random

class Player:
    def __init__(self, dir):
        self.x = 400
        self.y = 300
        self.size = 20
        self.speed = 20
        self.direction = dir
        self.body = [[self.x, self.y]]
        self.length = 1
        
    #probably not necessary to have these functions but OO ideology says I should have them so here they are
    def moveRight(self):
        self.direction = 'right'

    def moveLeft(self):
        self.direction = 'left'

    def moveUp(self):
        self.direction = 'up'

    def moveDown(self):
        self.direction = 'down'

    def returnLoc(self):
        return self.loc

class Apple:
    size = 20
    x = random.randint(1, 39)*20
    y = random.randint(1, 29)*20
    color = (200, 0, 0)

    def new_loc(self):
        self.x = random.randint(1, 39)*20
        self.y = random.randint(1, 29)*20

class App:

    windowWidth = 800
    windowHeight = 640
    player = 0
    length = 1
    tail = 0
    clock = 0
    font = None

    def __init__(self):
        self._running = True
        self.player = Player('right')
        self.apple = Apple()
        self._display_surf = None
        self._image_surf = None
        
    def on_init(self):
        #initiallization stuff
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 35)
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('Snake')
        self._running = True
        
   #I don't remember why this is here but I'm scared to remove it     
   #def on_event(self, event):
    #   if event.type == QUIT:
    #      self._running = False


    def update_player_pos(self):
         if self.clock % 5 == 0:

                #checks direction player is moving
                if self.player.direction == 'right':
                    
                    #new location of player head
                    new = [self.player.body[0][0] + self.player.speed, self.player.body[0][1]]
                        
                    #player self collission    
                    if ( new in self.player.body):
                        self._running = False
                        
                    #removing tail once new head is added
                    self.player.body.insert(0, new)
                    if(len(self.player.body) > self.length):
                        del self.player.body[self.length]

                if self.player.direction == 'left':
                    
                    
                    new = [self.player.body[0][0] - self.player.speed, self.player.body[0][1]]

                    if (new in self.player.body):
                        self._running = False

                    self.player.body.insert(0, new)
                    if(len(self.player.body) > self.length):
                        del self.player.body[self.length]
                            
                if self.player.direction == 'up':
                    
                    new = [self.player.body[0][0], self.player.body[0][1] - self.player.speed]

                    if ( new in self.player.body):
                        self._running = False

                    self.player.body.insert(0, new)
                    if(len(self.player.body) > self.length):
                        del self.player.body[self.length]
                        
                if self.player.direction == 'down':
                    

                    new = [self.player.body[0][0], self.player.body[0][1]+self.player.speed]

                    if ( new in self.player.body):
                        self.running = False
                        
                    self.player.body.insert(0, new)
                    if(len(self.player.body) > self.length):
                        del self.player.body[self.length]


    def on_loop(self):
        
        #apple collission logic
        if self.player.body[0][0]== self.apple.x and self.player.body[0][1] == self.apple.y:
                self.length += 1
                self.apple.new_loc()
                if ([self.apple.x, self.apple.y] in self.player.body):
                    while ([self.apple.x, self.apple.y] in self.player.body):
                        self.apple.new_loc()

        #player border collission
        if self.player.body[0][0] > 780 or self.player.body[0][0] < 0 or self.player.body[0][1] < 0 or self.player.body[0][1] > 580:
                self._running = False

       

    def on_render(self):
        #weird pygame display surface and text stuff
        self._display_surf.fill((100,100,100))
        textsurface = self.myfont.render('Score: ', False, (250, 250, 250))
        score = self.myfont.render(str(self.length-1), False, (250, 250, 250))
        self._display_surf.blit(textsurface,(0, 600))
        self._display_surf.blit(score,(120, 600))

        #render grid
        for y in range(30):
            for x in range(40):
                pygame.draw.rect(self._display_surf, (50, 50, 50), (x*20, y*20, self.player.size, self.player.size), 1)

        #render apple 
        pygame.draw.rect(self._display_surf, self.apple.color, (self.apple.x, self.apple.y, self.apple.size, self.apple.size), 0)

        #renders players body 
        for segment in self.player.body:
            if segment[0] >= 0 and segment[0] <= 780 and segment[1] >= 0 and segment[1] <= 580:
                pygame.draw.rect(self._display_surf, (0, 0, 0), (segment[0], segment[1], self.player.size, self.player.size), 0)
        
        pygame.display.flip()

    def on_cleanup():
        pygame.quit()

    def on_execute(self):  
             
        if self.on_init() == False:
            self._running = False

        while(self._running):
            if self.clock > 120:
                self.clock = 0

            self.clock += 1
            self.update_player_pos()

            #Get key inputs
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if(keys[K_d]):
                if self.player.x < 780 and self.player.direction != "left":
                    self.player.moveRight()
                    
            if(keys[K_a]):
                if self.player.x > 0 and self.player.direction != "right":
                    self.player.moveLeft()
                    
            if(keys[K_w]):
                if self.player.y > 0 and self.player.direction != "down":
                    self.player.moveUp()
                    
            if(keys[K_s]):
                if self.player.y < 580 and self.player.direction != 'up':
                    self.player.moveDown()
                    
            if(keys[K_ESCAPE]):
                self._running = False

            self.on_loop()  
            self.on_render()
        
        print(str(self.length-1))
        self.on_cleanup()
        
if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
