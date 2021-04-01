import pygame
import random
import time
import json
from pygame.locals import *
from moviepy.editor import VideoFileClip

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
image_user = pygame.image.load('image/user.png') # Юзер
image_dealer = pygame.image.load('image/dealer.png') # Дилер
image_bot1 = pygame.image.load('image/bot1.png') # Bot1
image_bot2 = pygame.image.load('image/bot2.png') # Bot2
image_bot3 = pygame.image.load('image/bot3.png') # Bot3
image_bot4 = pygame.image.load('image/bot4.png') # Bot4
background = pygame.image.load('image/background.jpg') #Задний фон игры
menu_background = pygame.image.load('image/background_menu.jpg') #Задний фон меню
card_back = pygame.image.load('image/Cards/Back Red.png') #Рубашка карты 
chips5 = pygame.image.load('image/chips5.png') 
chips5_1 = pygame.image.load('image/chips5_1.png') 
chips5_2 = pygame.image.load('image/chips5_2.png') 
chips25 = pygame.image.load('image/chips25.png') 
chips25_1 = pygame.image.load('image/chips25_1.png') 
chips25_2 = pygame.image.load('image/chips25_2.png') 
chips100 = pygame.image.load('image/chips100.png') 
chips100_1 = pygame.image.load('image/chips100_1.png') 
chips100_2 = pygame.image.load('image/chips100_2.png') 
chips_stack = pygame.image.load('image/chips_stack.png') 

# Звуки
take_card_sound = pygame.mixer.Sound("sound/cardPlace4.wav")
cards_shuffle_sound = pygame.mixer.Sound("sound/cardShuffle.wav")
chips_stack_sound = pygame.mixer.Sound('sound/chipLay1.wav') 
lose_sound = pygame.mixer.Sound('sound/lose sound.wav') 
win_sound = pygame.mixer.Sound('sound/win sound.wav')
draw_sound = pygame.mixer.Sound('sound/draw sound.wav')
menu_music = pygame.mixer.Sound('sound/Opening Menu.wav')
fight_music = pygame.mixer.Sound('sound/fight.mp3')
laughter_sound = pygame.mixer.Sound('sound/laughter.mp3')

background_music_list = []
for i in range(1,11):
    background_music_list.append(pygame.mixer.Sound(f'sound/background_music{i}.mp3'))

# Видео
video_casino = VideoFileClip('video\casino.mp4')

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
    def __init__(self,name,money,image):
        self.name  = name
        self.money = money
        self.image = image
        self.rate = 0
        self.sum_on_hand = 0
        self.final_sum_on_hand = 0
        self.list_chips = []
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
        pygame.mixer.Sound.play(fight_music)
        display.blit(background,(0,0))
        pygame.display.update()
        print_text(f'We are a team of super heroes who must beat the casino',100,50,(255,255,255),font_size = 50)
        pygame.display.update()
        for i in range(1,9):
            time.sleep(1.5)
            display.blit(pygame.image.load(f'image/bot{i*100}.png'),(100,100))
            pygame.display.update()
        
        time.sleep(3)
        pygame.mixer.Sound.play(laughter_sound) 
        print_text(f'ha-ha-ha-ha-ha-ha',600,300,(255,50,50),font_size = 70)
        pygame.display.update()
        time.sleep(3)
        display.blit(pygame.image.load(f'image/boss.png'),(900,100))
        pygame.display.update()
        time.sleep(3)
        print_text(f'I`m waiting for you and your money!!!',100,500,(255,50,50),font_size = 70)
        pygame.display.update()
        time.sleep(5)

        display.blit(background,(0,0))
        for i in range(5,0,-1):
            time.sleep(1)
            display.blit(background,(0,0))
            print_text(f'Let`s go! {i}',500,300,(255,255,255),font_size = 120)   
            pygame.display.update() 
       
        time.sleep(1)
        pygame.mixer.Sound.stop(fight_music)
        self.show_users()

    def show_users(self):

        pygame.mixer.Sound.stop(background_music_list[0])
        random.shuffle(background_music_list)
        pygame.mixer.Sound.play(background_music_list[0])

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

        self.bot_rates()    

        while game:
            mouse = pygame.mouse.get_pos()    
            click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.need_save_game()
                    quit()
                    pygame.quit()
                    
            if self.rate > 0:
                button_play.draw(912,845,'Lets go',self.start_round,only_text = False)
                button_clear.draw(1110,845,'Clear',self.clear,only_text = False)

            if 5 <= self.user.money:
                if 900 < mouse[0] < 991 and 700 < mouse[1] <791:
                    display.blit(chips5_1,(900,700))
                    if click[0] == 1:
                        button_05.draw(900,700, action=self.chips_on_table, parametr=(chips5_2,5))
                else:                
                    display.blit(chips5,(900,700))

            if 25 <= self.user.money:
                if 1000 < mouse[0] < 1091 and 700 < mouse[1] <791:
                    display.blit(chips25_1,(1000,700))
                    if click[0] == 1 :
                        button_25.draw(1000,700, action=self.chips_on_table, parametr=(chips25_2,25))
                else:                
                    display.blit(chips25,(1000,700)) 
    
            if 100 <= self.user.money:
                if 1100 < mouse[0] < 1191 and 700 < mouse[1] <791:
                    display.blit(chips100_1,(1100,700))
                    if click[0] == 1:
                        button_100.draw(1100,700,action=self.chips_on_table, parametr=(chips100_2,100))
                else:                
                    display.blit(chips100,(1100,700)) 
               
            pygame.display.update()

    def refresh_window(self):

        # background
        display.blit(background,(0,0))

        # user
        display.blit(image_user,(700,700))
        print_text(f'{self.user.name}',700,700,(10,180,250),font_size = 30)
        print_text(f'{self.user.money}$',700,750,(200,204,58),font_size = 30)

        # dealer
        display.blit(image_dealer,(1000,0))
        print_text(f'{self.dealer.name}',1000,0,(10,180,250),font_size = 30)
        print_text(f'{self.dealer.money}$',1000,50,(200,204,58),font_size = 30)
        display.blit(chips_stack,(1200,20))

        # bots ['Eva','Victoria','Mike']
        position = 0
        for bot in self.bot_list:
            display.blit(bot.image,(50,0+position))
            print_text(f'{bot.name}',50,0+position,(10,180,250),font_size = 30)
            print_text(f'{bot.money}$',50,50+position,(200,204,58),font_size = 30)
            position +=300

        # chips
        print_text(f'{self.rate}$',1100,600,(255,255,255),font_size = 30)
        n = 0
        for i in self.list_chips:
            display.blit(i,(1000,600-n*4))   
            n+=1

        position = 0
        for i in range(len(self.bot_list)): 
            print_text(f'{self.bot_list[i].rate}$',430,40+position,(255,255,255),font_size = 30)
            n = 0
            for chip in self.bot_list[i].list_chips: 
                display.blit(chip,(330,40+position-n*4))
                n+=1
            position +=300    

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
        pygame.mixer.Sound.play(chips_stack_sound)
        pygame.time.delay(300)

        self.user.money -= parametr[1]
        self.rate +=parametr[1]
        self.list_chips.append(parametr[0])
        self.refresh_window() 

    def bot_rates(self):

        for bot in self.bot_list:
            bot.list_chips = [] 

            if random.randrange(5, 200, 5) > bot.money:
                bot.rate = 5  
            else:        
                bot.rate = random.randrange(5, 200, 5)
            rate = bot.rate

            while rate !=0:
                if rate - 100 >= 0:
                    bot.list_chips.append(chips100_2)
                    bot.money -= 100
                    rate -= 100

                elif rate - 25 >= 0:   
                    bot.list_chips.append(chips25_2)
                    bot.money -= 25
                    rate -= 25  

                else:   
                    bot.list_chips.append(chips5_2)
                    bot.money -= 5
                    rate -= 5  
        self.refresh_window() 

    def start_round(self):

        game = True

        display.blit(background,(0,0))  

        pygame.mixer.Sound.play(cards_shuffle_sound)  
        for i in range(52):
            pygame.display.update()
            time.sleep(0.05)
            display.blit(card_back,(1400,350-i*4))
            
        button_take_card = Botton(190,50)
        button_skip = Botton(100,50)

        print_text(f'{self.user.name}',700,700,(10,180,250),font_size = 30)
        print_text(f'{self.user.money}$',700,750,(200,204,58),font_size = 30)

        self.first_move()
        
        while game:
            mouse = pygame.mouse.get_pos()    
            click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.need_save_game()
                    quit()
                    pygame.quit()
             
            if self.user.sum_on_hand < 21: 
                button_take_card.draw(912,845,'Take card',action = self.take_card,only_text = False, parametr=self.user)
            else:
                self.skip()    

            button_skip.draw(1110,845,'Skip',action = self.skip,only_text = False)
            pygame.display.update()    

    def clear(self):
        self.user.money += self.rate
        self.rate = 0
        self.list_chips = []
        self.refresh_window()
        self.show_users()

    def first_move(self):
        self.take_card(self.user,2)

        for bot in self.bot_list:
            self.take_card(bot,2)

        self.take_card(self.dealer,1)

    def dealer_brain(self): 
        while self.dealer.sum_on_hand < 17:
            time.sleep(0.3)
            self.take_card(self.dealer)

    def bots_brain(self,bot): 
        while bot.sum_on_hand < 21:
            time.sleep(0.3)
            take_or_not = self.to_be_and_not_to_be(bot.sum_on_hand)
            if take_or_not:
                self.take_card(bot)    
            else:
                break    

    def to_be_and_not_to_be(self,sum_cards):
        number_of_cards = len(self.deck.cards) 
        happy_cards = 0
        max_sum = 21 - sum_cards 
        for card in self.deck.cards:
            if card.rank == 11:
                happy_cards += 1    
            elif card.rank <=max_sum:
                happy_cards += 1 
        lucky_list = [0]*(number_of_cards-happy_cards) + [1]*happy_cards
        return random.choice(lucky_list)

    def skip(self):

        # bots
        for bot in self.bot_list:
            if bot.money >= self.rate:
                self.bots_brain(bot)
        # self.show_result()    

        # dealer
        self.dealer_brain()

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
        for bot in self.bot_list:
            for i in range(len(bot.cards_on_hand)):
                self.deck.cards.append(bot.cards_on_hand.pop())    

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
            print_text(f'YOU WON! {int(rate)}$',700,450,(50,255,50),font_size = 60) 
            pygame.mixer.Sound.play(win_sound)
        else:
            if self.user.final_sum_on_hand < self.dealer.final_sum_on_hand:
                # self.user.money -= self.rate*2
                self.dealer.money += self.rate 
                print_text(f'You lose! {int(self.rate)}$',700,450,(255,50,50),font_size = 50)  
                pygame.mixer.Sound.play(lose_sound)
                time.sleep(2)
                if self.user.money == 0:
                    pygame.display.set_caption('You lost everything! Good by))')
                    video_casino.preview()
                    quit()
                    pygame.quit()

            elif self.user.final_sum_on_hand > self.dealer.final_sum_on_hand:
                self.user.money += self.rate*2
                self.dealer.money -= self.rate
                print_text(f'YOU WON! {int(self.rate*2)}$',700,450,(50,255,50),font_size = 60)
                pygame.mixer.Sound.play(win_sound)
            else:
                self.user.money += self.rate
                print_text(f'Draw!',750,450,(255,255,255),font_size = 50)  
                pygame.mixer.Sound.play(draw_sound)

        position = 0
        for bot in self.bot_list:
            if bot.sum_on_hand == 21 and len(bot.cards_on_hand) == 2:
                if (int(bot.rate*0.5) + bot.rate*2)%5:
                    rate = (int(bot.rate*0.5) + bot.rate*2)    
                    rate += 5-(int(bot.rate*0.5) + bot.rate*2)%5
                else:
                    rate = (int(bot.rate*0.5) + bot.rate*2)
                bot.money += rate
                self.dealer.money -= rate
                print_text(f'{bot.name} Win! {int(bot.rate)}$',200,260+position,(50,255,50),font_size = 30)
            else:    
                if bot.final_sum_on_hand < self.dealer.final_sum_on_hand:
                    # bot.money -= bot.rate
                    self.dealer.money += bot.rate 
                    print_text(f'{bot.name} Lose! {int(bot.rate)}$',200,260+position,(255,50,50),font_size = 30)
                        
                elif bot.final_sum_on_hand > self.dealer.final_sum_on_hand:
                    bot.money += bot.rate*2
                    self.dealer.money -= bot.rate
                    print_text(f'{bot.name} Win! {int(bot.rate)}$',200,260+position,(50,255,50),font_size = 30)
                else:
                    bot.money += bot.rate
                    print_text(f'{bot.name} Draw! {int(bot.rate)}$',200,260+position,(255,255,255),font_size = 30)      
            position +=300
        pygame.display.update()    

    def show_result(self):

        # background
        display.blit(background,(0,0))

        # user
        display.blit(image_user,(700,700))
        print_text(f'{self.user.name}',700,700,(10,180,250),font_size = 30)
        print_text(f'{self.user.money}$',700,750,(200,204,58),font_size = 30)

        # dealer
        display.blit(image_dealer,(1000,0))
        print_text(f'{self.dealer.name}',1000,0,(10,180,250),font_size = 30)
        print_text(f'{self.dealer.money}$',1000,50,(200,204,58),font_size = 30)
        display.blit(chips_stack,(1200,20))

        # bots ['Eva','Victoria','Mike']
        position = 0
        for i in range(len(self.bot_list)):
            display.blit(self.bot_list[i].image,(50,0+position))
            print_text(f'{self.bot_list[i].name}',50,0+position,(10,180,250),font_size = 30)
            print_text(f'{self.bot_list[i].money}$',50,50+position,(200,204,58),font_size = 30)
            position +=300

        # chips
        print_text(f'{self.rate}$',1100,600,(255,255,255),font_size = 30)
        n = 0
        for i in self.list_chips:
            display.blit(i,(1000,600-n*4))   
            n+=1

        position = 0
        for i in range(len(self.bot_list)): 
            print_text(f'{self.bot_list[i].rate}$',430,40+position,(255,255,255),font_size = 30)
            n = 0
            for chip in self.bot_list[i].list_chips: 
                display.blit(chip,(330,40+position-n*4))
                n+=1
            position +=300   

        for id_user in self.user_list:
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

        # cards user
        position = 0
        for i in self.user.cards_on_hand:
            display.blit(i.image,(870+position,700))
            position += 50
        print_text(f'score: {self.user.sum_on_hand}',860,650,(255,255,255),font_size = 30)
        if self.hints and id_user.sum_on_hand < 21:
            chance = self.chance_of_success()
            print_text(f'change of success: {chance}%',950+position,730,(255,255,255),font_size = 30)    

        # cards bots
        position_bot = 0
        for bot in self.bot_list:
            position_card = 0
            for i in bot.cards_on_hand:
                display.blit(i.image,(300+position_card,130+position_bot))
                position_card += 50
            print_text(f'score:{bot.sum_on_hand}',300,90+position_bot,(255,255,255),font_size = 30)    
            position_bot +=300  
            
        # cards dealer
        position = 0
        for i in self.dealer.cards_on_hand:
            display.blit(i.image,(900+position,50))
            position -= 50
        print_text(f'score:{self.dealer.sum_on_hand}',850,0,(255,255,255),font_size = 30)    

        position_deck = 0
        for i in range(len(self.deck.cards)):
            display.blit(card_back,(1400,350-position_deck*4))
            position_deck +=1

    def take_card(self,user,number = 1):
        for i in range(1,number+1):
            pygame.mixer.Sound.play(take_card_sound)  
            # pygame.time.delay(150)

            user.cards_on_hand.append(self.deck.cards.pop())
            self.show_result()
            pygame.display.update()
            time.sleep(0.7)

    def save_file(self,save):
        if save:
            my_dict = {}
            my_dict[f'{self.user.name}'] = {
                'money':self.user.money,
                'dealer':self.dealer.money,
                'bot_list':[bot.money for bot in self.bot_list]
                }

            print(my_dict)
            with open('save.json', "a") as write_file:
                json.dump(my_dict, write_file,indent=4)

    def need_save_game(self):
        pygame.mixer.Sound.stop(background_music_list[0])
        display.blit(background,(0,0))
        pygame.display.update()
        botton_yes = Botton(70,50)
        botton_no  = Botton(70,50)

        print_text(f'Save the game?:',450,330,(255,255,255),font_size = 60)
        botton_yes.draw(900,330,'yes',action = self.save_file,font_size = 60,parametr=True) 
        botton_no.draw(1000,330,'no',action = self.save_file,font_size =60,parametr=False)
        pygame.display.update()
        time.sleep(5)

def print_text(message,x,y,font_color=(255,255,255),font_type = 'Broadway',font_size = 30):
    font_type = pygame.font.SysFont(font_type,font_size)
    text = font_type.render(message,1,font_color)
    display.blit(text,(x,y))

def show_menu():

    pygame.mixer.Sound.play(menu_music)
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
    # botton_players4 = Botton(70,50)

    botton_hints_yes = Botton(70,50)
    botton_hints_no  = Botton(70,50)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pygame.quit()

        display.blit(menu_background,(200,100))

        print_text('Use hints?',250,200,(10,180,250),font_size = 50)
        if hints:
            botton_hints_yes.draw(550,190,'yes',use_hints,60,parametr=True)
        else:
            botton_hints_no.draw(550,190,'no',use_hints,60,parametr=False)

        print_text('How many bot players will be in the game?',250,400,(10,180,250),font_size = 50)
        botton_players0.draw(550,500,'0',init_start_game,60,0)
        botton_players1.draw(650,500,'1',init_start_game,60,1)
        botton_players2.draw(750,500,'2',init_start_game,60,2)
        botton_players3.draw(850,500,'3',init_start_game,60,3)
        
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

    pygame.mixer.Sound.stop(menu_music)

    user = Player(user_name,2000,image_user)
    dealer = Player('Dealer',10000,image_dealer)

    bot_list = []
    bot_name = ['Eva','Victoria','Mike','Sophia']
    for i in range(0,number_of_bots):
        bot_list.append(Player(f'{bot_name[i]}',random.randrange(1000, 5000, 5),pygame.image.load('image/bot'+str(i+1)+'.png')))

    cards_list = []
    for j in ['Clubs ','Diamond ','Hearts ','Spades ']:
        cards_list += [(pygame.image.load('image/cards/'+j+str(i)+'.png'),10 if i>10 else 11 if i==1 else i) for i in range(1,14)]

    deck = Deck(cards_list)
    deck.shuffle()

    # Если hints = True, тогда отображается процент вытянуть нужную карту
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

        print_text('Enter your name:',400,400,(10,180,250),font_size = 50)
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
    show_menu()
    pygame.quit()

