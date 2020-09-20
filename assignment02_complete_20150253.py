# -*- coding:utf-8 -*-

import sys
import pygame
import pygame.sprite

class Shape(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        
        self.__image = image
        self.__rect = self.__image.get_rect().move(x, y)
    
    @property
    def image(self):
        return self.__image
    
    @property
    def rect(self):
        return self.__rect
    
    @image.setter
    def image(self, image):
        self.__image = image
    
    @rect.setter
    def rect(self, rect):
        self.__rect = rect
        
        
class Tile(Shape):    
    def __init__(self, x, y):        
        super().__init__(pygame.image.load('image/b_tile.png'), x, y)
    
    @staticmethod 
    def get_tiles(start_x, start_y, file_name):
        tile_size = 50                              # tile 크기 설정
        x, y = (start_x, start_y)                   # tile의 최초 위치 지정
        wall_tiles = []        
        
        in_file = open(file_name, 'r')              # tile 위치 정보 파일 열기  
        for row in in_file :             
            for kind in row :                
                if kind == 'b' :
                    tile = Tile(x, y)
                    wall_tiles.append(tile)
                x += tile_size
            y += tile_size
            x = start_x
                              
        return wall_tiles          
   
class Board(Shape):
    def __init__(self, x, y):
        super().__init__(pygame.image.load('image/board.png'), x, y)

class Gem(Shape): 
    def __init__(self, x, y):
        gem_image_files = ['image/gem01.png', 'image/gem02.png', 'image/gem03.png'] 
        self.__images = [pygame.image.load(file) for file in gem_image_files] 
        self.image_index = 0       

        super().__init__(self.__images[self.image_index], x, y)
        
        self.__current_time = 0
        self.__animation_time = 3
        
    def update(self):
        dt = 0.1
        
        self.__current_time += dt
        if self.__current_time > self.__animation_time :
            self.__current_time = 0
        
        self.image_index = int(self.__current_time)
        self.__image = self.__images[self.image_index]
        
    @property
    def images(self):
        return self.__images
    
    @property
    def current_time(self):
        return self.__current_time
    
    @property
    def animation_time(self):
        return self.__animation_time
    
    @images.setter
    def images(self, images):
        self.__images = images
    
    @current_time.setter
    def current_time(self, current_time):
        self.__current_time = current_time
    
    @animation_time.setter
    def animation_time(self, animation_time):
        self.__animation_time = animation_time


class Pacman(Shape):
    def __init__(self, x, y):
        pacman_image_files = ['image/right_open.png', 'image/right_close.png', 'image/left_open.png', 'image/left_close.png',
                                'image/down_open.png', 'image/down_close.png', 'image/up_open.png', 'image/up_close.png'] 
        self.__images = [pygame.image.load(file) for file in pacman_image_files] 
        self.__image_index = 0
        self.__direction = 0

        super().__init__(self.__images[self.__image_index], x, y)
        
        self.__current_time = 0
        self.__animation_time = 2
    
    
    def update(self):  
        dt = 0.1
        
        self.__current_time += dt
        if self.__current_time > self.__animation_time :
            self.__current_time = 0
        
        self.__image_index = int(self.__current_time) + self.__direction
        self.image = self.__images[self.__image_index]   



    def move(self, board, tiles, gem):
        x, y = self.rect.x, self.rect.y
        delta = 5
        key = pygame.key.get_pressed()
        
        if not self.rect.colliderect(gem.rect):
            if key[pygame.K_DOWN]:
                self.__direction = 4
                self.rect.y += delta
            elif key[pygame.K_UP]:              
                self.__direction = 6
                self.rect.y -= delta
            elif key[pygame.K_RIGHT]:
                self.__direction = 0    
                self.rect.x += delta
            elif key[pygame.K_LEFT]:
                self.__direction = 2
                self.rect.x -= delta        
        else:
            return True
        
        if (board.rect.contains(self.rect) == False) | (self.rect.collidelist(tiles) != -1):
            self.rect.x = x
            self.rect.y = y


        return False

    @property
    def images(self):
        return self.__images
    
    @property
    def images_index(self):
        return self.__images_index
    
    @property
    def direction(self):
        return self.__direction
    
    @property
    def current_time(self):
        return self.__current_time
    
    @property
    def animation_time(self):
        return self.__animation_time

    @images.setter
    def images(self, images):
        self.__images = images
        
    @images_index.setter
    def images_index(self, images_index):
        self.__images_index = images_index
        
    @direction.setter
    def direction(self, direction):
        self.__direction = direction
    
    @current_time.setter
    def current_time(self, current_time):
        self.__current_time = current_time
    
    @animation_time.setter
    def animation_time(self, animation_time):
        self.__animation_time = animation_time
        
class Game: 
    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((600, 600))

    def play(self):
        board_x, board_y = (25, 25)
                
        board = Board(board_x, board_y)        
        tiles = Tile.get_tiles(board_x, board_y, 'data/stage01.data')
        gem = Gem(525, 525)
        pacman = Pacman(board_x+2, board_y+2)
                                
        all_group = pygame.sprite.Group(board)
        all_group.add(tiles)
        all_group.add(gem)         
        all_group.add(pacman)
        
        all_group.draw(self.screen)
        
        clock = pygame.time.Clock()
        find_gem = False        
        while not find_gem :
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); 
                    sys.exit()   
                         
            find_gem = pacman.move(board, tiles, gem)                            

            all_group.update()                                        
            all_group.draw(self.screen)
                        
            pygame.display.update()
            pygame.display.flip()
        

def main():
    game = Game()
    game.play()

main()
            