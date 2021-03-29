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
image_user = pygame.image.load('image/user.png') #Юзер
image_dealer = pygame.image.load('image/dealer.png') #Юзер
background = pygame.image.load('image/background.jpg') #Задний фон игры
menu_background = pygame.image.load('image/background_menu.jpg') #Задний фон меню
card_back = pygame.image.load('image/cards/Back Red.png') #Рубашка карты 
chips5 = pygame.image.load('image/chips5.png') 
chips5_1 = pygame.image.load('image/chips5_1.png') 
chips5_2 = pygame.image.load('image/chips5_2.png') 
chips25 = pygame.image.load('image/chips25.png') 
chips25_1 = pygame.image.load('image/chips25_1.png') 
chips25_2 = pygame.image.load('image/chips25_2.png') 
chips100 = pygame.image.load('image/chips100.png') 
chips100_1 = pygame.image.load('image/chips100_1.png') 
chips100_2 = pygame.image.load('image/chips100_2.png') 
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
        self.sum_on_hand = 0
        self.cards_on_hand = []

class Botton():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.inactive_color = (13,162,58)
        self.active_color = (23,204,58)

    def draw(self,x,y,massage = '',action = None,font_size = 30,parametr = None, only_text = True):
        mouse = pygame.mouse.get_pos()    
        click = pygame.mouse.get_pressed()

        if only_text:
            if x < mouse[0] < x+self.width and y < mouse[1] <y+self.height:
                print_text(massage,x,y,font_color = (23,204,58),font_size = font_size)
                if click[0] == 1 :
                    if action is not None:
                        if action == quit:
                            quit()
                            pygame.quit()
                        if parametr is not None:
                            action(parametr)    
                        else:            
                            action()
            else:
                print_text(massage,x,y,font_size = font_size)
        else:      
            if x < mouse[0] < x+self.width and y < mouse[1] <y+self.height:
                pygame.draw.rect(display,self.active_color,(x,y, self.width,self.height))
                if click[0] == 1 :
                    if action is not None:
                        if action == quit:
                            quit()
                            pygame.quit()
                        if parametr is not None:
                            action(parametr)    
                        else:            
                            action()
            else:
                pygame.draw.rect(display,self.inactive_color,(x,y, self.width,self.height))
            print_text(massage,x+10,y+10,font_size = font_size)

class BlackJack():
    def __init__(self,deck,user,dealer,bot_list,hints = False):   
        self.deck = deck 
        self.user = user
        self.dealer = dealer     
        self.bot_list = bot_list
        self.user_list = []
        self.hints = hints

        self.user_list.append(user)
        self.user_list.append(dealer) 
        for bot in bot_list:
            self.user_list.append(bot)

    def start_game(self):   
        self.show_users()

    def show_users(self):
        self.number_chips = 0
        self.rate = 0
        self.list_chips= []

        game = True
        display.blit(background,(0,0))
        button_play  = Botton(190,50)
        button_clear = Botton(100,50)

        button_05 = Botton(100,100)
        button_25 = Botton(100,100)
        button_100 = Botton(100,100)

        # user
        display.blit(image_user,(500,700))
        print_text(f'{self.user.name}',500,700,(10,180,250),font_size = 30)
        print_text(f'{self.user.money}$',500,750,(200,204,58),font_size = 30)

        # dealer
        display.blit(image_dealer,(1000,0))
        print_text(f'{self.dealer.name}',1000,0,(10,180,250),font_size = 30)
        print_text(f'{self.dealer.money}$',1000,50,(200,204,58),font_size = 30)

        while game:
            mouse = pygame.mouse.get_pos()    
            click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    pygame.quit()
                    
            if self.rate > 0:
                button_play.draw(712,845,'Lets go',self.start_round,only_text = False)
                button_clear.draw(910,845,'Clear',self.clear,only_text = False)

            if 5 <= self.user.money:
                if 700 < mouse[0] < 791 and 700 < mouse[1] <791:
                    display.blit(chips5_1,(700,700))
                    if click[0] == 1:
                        button_05.draw(700,700, action=self.chips_on_table, parametr=(chips5_2,5))
                else:                
                    display.blit(chips5,(700,700))

            if 25 <= self.user.money:
                if 800 < mouse[0] < 891 and 700 < mouse[1] <791:
                    display.blit(chips25_1,(800,700))
                    if click[0] == 1 :
                        button_25.draw(800,700, action=self.chips_on_table, parametr=(chips25_2,25))
                else:                
                    display.blit(chips25,(800,700)) 
    
            if 100 <= self.user.money:
                if 900 < mouse[0] < 991 and 700 < mouse[1] <791:
                    display.blit(chips100_1,(900,700))
                    if click[0] == 1:
                        button_100.draw(900,700,action=self.chips_on_table, parametr=(chips100_2,100))
                else:                
                    display.blit(chips100,(900,700)) 
               
            pygame.display.update()

    def refresh_window(self):

        # background
        display.blit(background,(0,0))

        # user
        display.blit(image_user,(500,700))
        print_text(f'{self.user.name}',500,700,(10,180,250),font_size = 30)
        print_text(f'{self.user.money}$',500,750,(200,204,58),font_size = 30)

        # dealer
        display.blit(image_dealer,(1000,0))
        print_text(f'{self.dealer.name}',1000,0,(10,180,250),font_size = 30)
        print_text(f'{self.dealer.money}$',1000,50,(200,204,58),font_size = 30)

        # others
        print_text(f'{self.rate}$',900,600,(255,255,255),font_size = 30)
        n = 0
        for i in self.list_chips:
            display.blit(i,(800,600-n*4))   
            n+=1

    def chance_of_success(self):
        number_of_cards = len(self.deck.cards) 
        happy_cards = 0
        max_sum = 21 - self.user.sum_on_hand 
        for card in self.deck.cards:
            if card.rank == 11:
                happy_cards += 1    
            elif card.rank<=max_sum:
                happy_cards += 1 
        chance = happy_cards/number_of_cards*100
        return round(chance,2)

    def chips_on_table(self,parametr):
        pygame.time.delay(300)
        display.blit(parametr[0],(800,600-self.number_chips*4))  
        self.number_chips += 1
        self.user.money -= parametr[1]
        self.rate +=parametr[1]
        self.list_chips.append(parametr[0])
        self.refresh_window() 

    def start_round(self):

        game = True

        display.blit(background,(0,0))  

        pygame.mixer.Sound.play(cards_shuffle)  
        for i in range(52):
            pygame.display.update()
            time.sleep(0.05)
            display.blit(card_back,(1400,350-i*4))
            
        button_take_card = Botton(190,50)
        button_skip = Botton(100,50)

        print_text(f'{self.user.name}',500,700,(10,180,250),font_size = 30)
        print_text(f'{self.user.money}$',500,750,(200,204,58),font_size = 30)

        self.first_move()
        
        while game:
            mouse = pygame.mouse.get_pos()    
            click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    pygame.quit()
             
            if self.user.sum_on_hand < 21: 
                button_take_card.draw(712,845,'Take card',action = self.take_card,only_text = False, parametr=self.user)
            else:
                self.skip()    

            button_skip.draw(910,845,'Skip',action = self.skip,only_text = False)
            pygame.display.update()    

    def clear(self):
        self.user.money += self.rate
        self.rate = 0
        self.list_chips = []
        self.refresh_window()
        self.show_users()

    def first_move(self):
        self.take_card(self.user,2)
        self.take_card(self.dealer,1)

    def dealers_brain(self): 
        while self.dealer.sum_on_hand < 17:
            time.sleep(0.3)
            self.take_card(self.dealer)

    def skip(self):

        # dealer
        self.dealers_brain()

        self.show_result()
        pygame.display.update()
        time.sleep(1)

        self.show_totals()
        time.sleep(5)

        self.return_cards_to_deck()

        self.show_users()

    def return_cards_to_deck(self):
        for i in range(len(self.user.cards_on_hand)):
            self.deck.cards.append(self.user.cards_on_hand.pop())    
        for i in range(len(self.dealer.cards_on_hand)):
            self.deck.cards.append(self.dealer.cards_on_hand.pop())
        # for bot in self.bot_list:
        #     for i in range(len(bot.cards_on_hand)):
        #         self.deck.cards.append(bot.cards_on_hand.pop())    

        self.deck.shuffle()    

    def show_totals(self):

        if self.user.final_sum_on_hand == 21 and len(self.user.cards_on_hand) == 2:

            if (int(self.rate*0.5) + self.rate*2)%5:
                rate = (int(self.rate*0.5) + self.rate*2)    
                rate += 5-(int(self.rate*0.5) + self.rate*2)%5
            else:
               rate = (int(self.rate*0.5) + self.rate*2) 

            self.user.money += rate
            self.dealer.money -= rate
            print_text(f'Congratulation, you won! {int(rate)}$',500,450,(50,255,50),font_size = 50) 
        else:
            if self.user.final_sum_on_hand < self.dealer.final_sum_on_hand:
                # self.user.money -= self.rate*2
                self.dealer.money += self.rate 
                print_text(f'You lose! {int(self.rate)}$',600,450,(255,50,50),font_size = 50)                          
            elif self.user.final_sum_on_hand > self.dealer.final_sum_on_hand:
                self.user.money += self.rate*2
                self.dealer.money -= self.rate
                print_text(f'Congratulation, you won! {int(self.rate*2)}$',500,450,(50,255,50),font_size = 50)
            else:
                self.user.money += self.rate
                print_text(f'Draw!',700,450,(255,255,255),font_size = 50)  
        pygame.display.update()

        # for bot in self.bot_list:
        #     if self.show_sum_cards_final(bot) == 21 and len(bot.cards_on_hand) == 2:
        #         bot.money += self.rate*1.5
        #         self.dealer.money -= self.rate*1.5
        #         print(f"{bot.name} выиграл! {self.rate*1.5}$")
        #     else:    
        #         if self.show_sum_cards_final(self.dealer) > self.show_sum_cards_final(bot):
        #             bot.money -= self.rate
        #             self.dealer.money += self.rate 
        #             print(f"{bot.name} проиграл! {self.rate}$")                         
        #         elif self.show_sum_cards_final(self.dealer) < self.show_sum_cards_final(bot):
        #             bot.money += self.rate
        #             self.dealer.money -= self.rate
        #             print(f"{bot.name} выиграл! {self.rate}$")
        #         else:
        #             print(f"У {bot.name} ничья с дилером!")        

    def show_result(self):

        # background
        display.blit(background,(0,0))

        # user
        display.blit(image_user,(500,700))
        print_text(f'{self.user.name}',500,700,(10,180,250),font_size = 30)
        print_text(f'{self.user.money}$',500,750,(200,204,58),font_size = 30)

        # dealer
        display.blit(image_dealer,(1000,0))
        print_text(f'{self.dealer.name}',1000,0,(10,180,250),font_size = 30)
        print_text(f'{self.dealer.money}$',1000,50,(200,204,58),font_size = 30)

        # others
        print_text(f'{self.rate}$',900,600,(255,255,255),font_size = 30)
        n = 0
        for i in self.list_chips:
            display.blit(i,(800,600-n*4))   
            n+=1

        for id_user in self.user_list:
            position = 0
            for i in id_user.cards_on_hand:
                if id_user == self.user:
                    display.blit(i.image,(670+position,700))
                    position += 50 
                elif id_user == self.dealer:
                    display.blit(i.image,(900+position,50))
                    position -= 50    

            position_deck = 0
            for i in range(len(self.deck.cards)):
                display.blit(card_back,(1400,350-position_deck*4))
                position_deck +=1

            sum_on_hand = 0
            for i in id_user.cards_on_hand:
                if i.rank == 11:
                    if 21>= sum_on_hand+i.rank:
                        sum_on_hand += i.rank
                    else:    
                        sum_on_hand += 1 
                else:        
                    sum_on_hand += i.rank  
            if sum_on_hand > 21:
                id_user.final_sum_on_hand = 0
            else:                       
                id_user.final_sum_on_hand = sum_on_hand
            id_user.sum_on_hand = sum_on_hand    

            if id_user == self.user:
                print_text(f'score:{sum_on_hand}',750+position,700,(255,255,255),font_size = 30)
                if self.hints and id_user.sum_on_hand < 21:
                    chance = self.chance_of_success()
                    print_text(f'change of success:{chance}%',750+position,730,(255,255,255),font_size = 30)
            elif id_user == self.dealer:    
                print_text(f'score:{sum_on_hand}',750+position,100,(255,255,255),font_size = 30)

    def take_card(self,user,number = 1):
        pygame.mixer.Sound.play(take_card_sound)  
        pygame.time.delay(300)

        for i in range(1,number+1):
            user.cards_on_hand.append(self.deck.cards.pop())
            self.show_result()
            pygame.display.update()
            time.sleep(1)

def print_text(message,x,y,font_color=(255,255,255),font_type = 'Broadway',font_size = 30):
    font_type = pygame.font.SysFont(font_type,font_size)
    text = font_type.render(message,1,font_color)
    display.blit(text,(x,y))

def show_menu():

    start_botton = Botton(360,60)
    quit_botton = Botton(130,60)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pygame.quit()

        display.blit(menu_background,(200,100))
        start_botton.draw(650,300,'Start game',menu_number_of_players,60)
        quit_botton.draw(740,400,'Quit',quit,60)
        pygame.display.update()

def menu_number_of_players():
    global user_name
    global hints

    user_name = get_user_name()

    botton_players0 = Botton(70,50)
    botton_players1 = Botton(70,50)
    botton_players2 = Botton(70,50)
    botton_players3 = Botton(70,50)
    botton_players4 = Botton(70,50)

    botton_hints_yes = Botton(70,50)
    botton_hints_no  = Botton(70,50)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pygame.quit()

        display.blit(menu_background,(200,100))

        print_text('Use hints?',250,200,(255,255,255),font_size = 50)
        if hints:
            botton_players3.draw(550,190,'yes',use_hints,60,parametr=True)
        else:
            botton_players4.draw(550,190,'no',use_hints,60,parametr=False)

        print_text('How many bot players will be in the game?',250,400,(255,255,255),font_size = 50)
        botton_players0.draw(550,500,'0',init_start_game,60,0)
        botton_players1.draw(650,500,'1',init_start_game,60,1)
        botton_players2.draw(750,500,'2',init_start_game,60,2)
        botton_players3.draw(850,500,'3',init_start_game,60,3)
        botton_players4.draw(950,500,'4',init_start_game,60,4)
        
        pygame.display.update()

def use_hints(hint):
    global hints
    pygame.time.delay(300)
    if hint:
        hints = False
    else:
        hints = True    

def init_start_game(number_of_bots):  
    global hints

    user = Player(user_name,130)
    dealer = Player('dealer',10000)

    bot_list = []
    for i in range(1,number_of_bots+1):
        bot_list.append(Player(f'player_bot{i}',random.randrange(1000, 5000, 5)))

    cards_list = []
    for j in ['Clubs ','Diamond ','Hearts ','Spades ']:
        cards_list += [(pygame.image.load('image/cards/'+j+str(i)+'.png'),10 if i>10 else 11 if i==1 else i) for i in range(1,14)]

    deck = Deck(cards_list)
    deck.shuffle()

    # Если hints = True, тогда отображается процент вытянуть нужную карту
    # use_hints = True

    blackjack = BlackJack(deck,user,dealer,bot_list,hints)  
    blackjack.start_game()

def get_user_name():

    font = pygame.font.SysFont('BroadWay', 50)
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
                    if name != '':
                        return name
            elif event.type == QUIT:
                quit()
                pygame.quit()

        # textrect = Rect(0, 0, 100, FONT_SIZE)
        display.blit(menu_background,(200,100))

        print_text('Enter your name:',400,400,(255,255,255),font_size = 50)
        # for i in names:
        #     text = font.render(i[:-1], True, (255,0,0), (0,0,0))
        #     display.blit(text, textrect)
        #     textrect.centery += FONT_SIZE

        block = font.render(name, True, (23,204,58))
        # rect = block.get_rect()
        # rect.center = display.get_rect().center
        display.blit(block, (900,400))
        pygame.display.update()

if __name__ == '__main__':
    hints = False
    # number_of_cards_in_hand = 0
    # number_of_cards = 52
    # user_name = 'user'

    show_menu()
    pygame.quit()

