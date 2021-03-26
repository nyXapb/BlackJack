import pygame

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
card_back = pygame.image.load('image/cards/Back Red.png') #Рубашка карты 
A5 = pygame.image.load('image/Clubs 11.png') 

# Звуки
take_card_sound = pygame.mixer.Sound("sound/cardPlace4.wav")

# Видео

card_width = 50
card_height = 100

b2_x = display_width //2 -200
b2_y = display_height - A5.get_height() - 200

# cards_png = []
# for j in ['Clubs ','Diamond ','Hearts ','Spades ']:
#     cards_png += ['image/cards/'+j+str(i)+'.png' for i in range(1,14)]
# print(cards_png)
# RED = (255,0,0)

# button = pygame.Rect(712, 845, 100, 25)
# button = pygame.image.load('image/buttons.png')

# Buttonify('image/cards/Clubs 11.png',(0,0), display)

# f = pygame.font.SysFont(None,48)
# text = f.render('Возьмите карту',1,RED)
# rect = text.get_rect()


# Верхнее меню
# info = pygame.Surface((800, 30))
score_f = pygame.font.SysFont('Arial', 32)
# lifes_f = pygame.font.SysFont('Arial', 32)  

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
                        action()    
                    else:            
                        action(parametr)
        else:
            pygame.draw.rect(display,self.inactive_color,(x,y, self.width,self.height))
        print_text(massage,x+10,y+10,font_size = font_size)    

def print_text(message,x,y,font_color=(0,0,0),font_type = 'Arial',font_size = 30):
    font_type = pygame.font.SysFont(font_type,font_size)
    text = font_type.render(message,1,font_color)
    display.blit(text,(x,y))

def show_menu():

    menu_background = pygame.image.load('image/background_menu.jpg')

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
    # position = number_of_cards_in_hand*-25 
    position = 0
    for i in range(number_of_cards_in_hand):
        display.blit(A5,(b2_x+position,b2_y))
        position += 50

    number_of_cards -= 1
    for i in range(number_of_cards):
        display.blit(card_back,(1400,350-i*5))

def skip():
    pass

def menu_number_of_players():
    menu_background = pygame.image.load('image/background_menu.jpg')

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
        # botton_number_of_players.draw(250,300,'How many bot players will there be in the game?',None,60)
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
    pass


def start_game():

    game = True

    # display.fill([255, 255, 255])
    display.blit(background,(0,0))  
    # display.blit(text,(0,0))
    # display.blit(text, rect)
    # display.blit(A5,(b2_x,b2_y))
    for i in range(52):
        display.blit(card_back,(1400,350-i*4))
    # display.blit(button,(712,845))
    # pygame.draw.rect(display, [255, 255, 255], button) 

    button_take_card = Botton(120,50)
    button_skip = Botton(120,50)

    while game:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = event.pos  # gets mouse position

                # if button.collidepoint(mouse_pos):
                #     display.blit(background,(0,0))
                    
                #     number_of_cards_in_hand +=1
                #     position = number_of_cards_in_hand*-25 
                #     # position = 0
                #     for i in range(number_of_cards_in_hand):
                #         display.blit(A5,(b2_x+position,b2_y))
                #         position += 50
                    
                #     number_of_cards -= 1
                #     for i in range(number_of_cards):
                #         display.blit(card_back,(1400,350-i*5))

        button_take_card.draw(712,845,'Take card',take_card)
        button_skip.draw(852,845,'Skip',skip)
        # pygame.draw.rect(display, [255, 255, 255], rect)
        # info.blit(lifes_f.render ('Lifes: ' +str(5), 1, (210, 120, 200)), (600, 0))
        # info.blit(score_f.render ('Score: ' +str(4), 1, (210, 120, 200)), (5, 0))
        # display.blit(info, (0,0))

        pygame.display.update()

# blackjack()    

if __name__ == '__main__':
    number_of_cards_in_hand = 0
    number_of_cards = 52
    show_menu()

