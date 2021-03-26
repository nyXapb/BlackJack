import pygame
import random
import time
import json
from pygame.locals import *

pygame.init()

# Картинка и название окна
pygame.display.set_caption('BlackJack')
icon = pygame.image.load('image/icon.png')
pygame.display.set_icon(icon)

# Размер окна
display_width = 1680
display_height = 900
display = pygame.display.set_mode((display_width,display_height))

# Картинки
background = pygame.image.load('image/background.jpg') #Задний фон 
menu_background = pygame.image.load('image/background_menu.jpg')
card_back = pygame.image.load('image/cards/Back Red.png') #Рубашка карты 
chips10 = pygame.image.load('image/chips10.png') #Фишки
chips11 = pygame.image.load('image/chips11.png')
A5 = pygame.image.load('image/Clubs 11.png') 

# Звуки
take_card_sound = pygame.mixer.Sound("sound/cardPlace4.wav")
cards_shuffle = pygame.mixer.Sound("sound/cardShuffle.wav")

# Видео

class Cards():
    def __init__(self,image,rank):
        self.image = image
        self.rank = rank

class Deck(): 
    def __init__(self,cards_list):   
        self.cards = []
           
        for image,rank in cards_list:
            self.cards.append(Cards(image,rank))   

    def shuffle(self):
        random.shuffle(self.cards) 

class Player():
    def __init__(self,name,money):
        self.name  = name
        self.money = money
        self.cards_on_hand = []

class Botton():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.inactive_color = (13,162,58)
        self.active_color = (23,204,58)

    def draw(self,x,y,massage,action = None,font_size = 30,parametr = None):
        mouse = pygame.mouse.get_pos()    
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x+self.width and y < mouse[1] <y+self.height:
            pygame.draw.rect(display,self.active_color,(x,y, self.width,self.height))
            if click[0] == 1 :
                if action is not None:
                    if action == quit:
                        quit()
                    if parametr is not None:
                        action(parametr)    
                    else:            
                        action()
        else:
            pygame.draw.rect(display,self.inactive_color,(x,y, self.width,self.height))
        print_text(massage,x+10,y+10,font_size = font_size)    

def print_text(message,x,y,font_color=(0,0,0),font_type = 'Arial',font_size = 30):
    font_type = pygame.font.SysFont(font_type,font_size)
    text = font_type.render(message,1,font_color)
    display.blit(text,(x,y))

def show_menu():

    start_botton = Botton(300,70)
    quit_botton = Botton(130,70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        display.blit(menu_background,(200,100))
        start_botton.draw(650,300,'Start game',menu_number_of_players,60)
        quit_botton.draw(740,400,'Quit',quit,60)
        pygame.display.update()

def take_card():

    global number_of_cards_in_hand
    global number_of_cards

    pygame.mixer.Sound.play(take_card_sound)  
    pygame.time.delay(300)

    display.blit(background,(0,0))
    number_of_cards_in_hand  +=1             
    position = 0
    for i in range(number_of_cards_in_hand):
        display.blit(A5,(650+position,700))
        position += 50
    print_text(f'score:15',750+position,700,(255,255,255),font_size = 30)    

    number_of_cards -= 1
    for i in range(number_of_cards):
        display.blit(card_back,(1400,350-i*4))

def skip():
    pass

def menu_number_of_players():
    global user_name

    user_name = get_user_name()

    botton_players0 = Botton(70,70)
    botton_players1 = Botton(70,70)
    botton_players2 = Botton(70,70)
    botton_players3 = Botton(70,70)
    botton_players4 = Botton(70,70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        display.blit(menu_background,(200,100))
        print_text('How many bot players will there be in the game?',250,300,(255,255,255),font_size = 50)
        botton_players0.draw(550,400,'0',pre_start_game,60,0)
        botton_players1.draw(650,400,'1',pre_start_game,60,1)
        botton_players2.draw(750,400,'2',pre_start_game,60,2)
        botton_players3.draw(850,400,'3',pre_start_game,60,3)
        botton_players4.draw(950,400,'4',pre_start_game,60,4)
        pygame.display.update()

def pre_start_game(number_of_bots):        
    if number_of_bots == 1:
        pass
    start_game()

def start_game():
    global user_name

    cards_list = []
    for j in ['Clubs ','Diamond ','Hearts ','Spades ']:
        cards_list += [('image/cards/'+j+str(i)+'.png',10 if i>10 else 11 if i==1 else i) for i in range(1,14)]

    deck = Deck(cards_list)
    deck.shuffle()

    my_player = Player(user_name,100)

    dealer = Player('dealer',10000)

    game = True

    display.blit(background,(0,0))  

    # pygame.mixer.Sound.play(cards_shuffle)  
    for i in range(52):
        # pygame.display.update()
        # time.sleep(0.05)
        display.blit(card_back,(1400,350-i*4))
        
    button_take_card = Botton(120,50)
    button_skip = Botton(120,50)

    while game:

        mouse = pygame.mouse.get_pos()    
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        button_take_card.draw(712,845,'Take card',take_card)
        button_skip.draw(852,845,'Skip',skip)
        print_text(f'user :{my_player.name}',500,700,(255,255,255),font_size = 30)
        print_text(f'money:{my_player.money}$',500,750,(255,255,255),font_size = 30)

        if 700 < mouse[0] < 800 and 650 < mouse[1] <700:
            display.blit(chips11,(700,600))
            # if click[0] == 1 :
            #     if action is not None:
            #         if action == quit:
            #             quit()
            #         if parametr is not None:
            #             action(parametr)    
            #         else:            
            #             action()
        else:                
            display.blit(chips10,(700,650))
        
        pygame.display.update()

FONT_SIZE = 60

def get_user_name():

    # print_text('Enter your name:',250,700,(255,255,255),font_size = 50)
    font = pygame.font.SysFont('Arial', 50)
    name = ""
    while True:
        # namefile = open('test.txt', 'r')
        # names = namefile.readlines()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.unicode.isalpha():
                    if event.unicode == 3:
                        name += 0
                    else:
                        name += event.unicode
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.key == K_RETURN:
                    return name
            elif event.type == QUIT:
                quit()

        textrect = Rect(0, 0, 100, FONT_SIZE)
        display.blit(menu_background,(200,100))

        print_text('Enter your name:',400,400,(255,255,255),font_size = 50)
        # for i in names:
        #     text = font.render(i[:-1], True, (255,0,0), (0,0,0))
        #     display.blit(text, textrect)
        #     textrect.centery += FONT_SIZE

        block = font.render(name, True, (255, 255, 255))
        # rect = block.get_rect()
        # rect.center = display.get_rect().center
        display.blit(block, (800,400))
        pygame.display.update()
        # pygame.display.flip()

if __name__ == '__main__':
    number_of_cards_in_hand = 0
    number_of_cards = 52
    user_name = 'user'
    # print(cards_png)

    show_menu()
    # pygame.quit()

