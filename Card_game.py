import random
import time
import json

class Cards():
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        return f'{self.rank}{self.suit}'

class Deck(): 
    def __init__(self,list_rank,list_suit):   
        self.cards = []
           
        for suit in list_suit:
            for rank in list_rank:
                self.cards.append(Cards(rank,suit))   

    def shuffle(self):
        random.shuffle(self.cards) 
        # for card in self.cards:
        #     print(card)

class Player():
    def __init__(self,name,money):
        self.name  = name
        self.money = money
        self.cards_on_hand = []

class BlackJack():
    def __init__(self,deck,my_player,dealer,bot_list,hints = False):   
        self.deck = deck 
        self.my_player = my_player
        self.dealer = dealer     
        self.bot_list = bot_list
        self.cards_values = self.get_cards_values()
        self.save_file_name = f'D:\TeachMeSkills\BJ_save\{my_player.name}.json'
        self.hints = hints

    def print_money(self):   
        print_text = ''
        for bot in self.bot_list:
            print_text += f'    {bot.name}: {bot.money}$'
        print(f'Money: {self.my_player.name}: {self.my_player.money}$   {print_text}    Dealer money: {self.dealer.money}$')

    def print_result(self):   
        print_text = ''
        for bot in self.bot_list:
            print_text += f'  {bot.name}: {self.show_sum_cards(bot)} очков'
        print(f'Результат: {self.my_player.name}: {self.show_sum_cards(self.my_player)} очков   {print_text}    {self.dealer.name}: {self.show_sum_cards(self.dealer)} очков')    

    def get_cards_values(self):
        return {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10,"A":11}

    def take_card(self,player,count=1):
        while count != 0:
            player.cards_on_hand.append(self.deck.cards.pop())
            count -=1
        self.show_cards(player)
        self.print_sum_cards(self.show_sum_cards(player))

    def show_cards(self,player): 
        string = '{:^20}'.format(player.name)
        print(string,end = ' ')
        for card in player.cards_on_hand:
            print(card,end = ' ')   

    def show_sum_cards(self,player): 
        sum_cards = 0
        for card in player.cards_on_hand:
            sum_cards += self.cards_values.get(card.rank)
            if card.rank == 'A' and sum_cards > 21:
                sum_cards -= 10     
        return sum_cards

    def show_sum_cards_final(self,player): 
        sum_cards = 0
        for card in player.cards_on_hand:
            sum_cards += self.cards_values.get(card.rank)
            if card.rank == 'A' and sum_cards > 21:
               sum_cards -= 10
        if sum_cards > 21:
            return 0        
        return sum_cards    

    def dealers_brain(self): 
        while self.show_sum_cards(self.dealer) < 17:
            time.sleep(0.3)
            self.take_card(self.dealer)

    def bots_brain(self,bot): 
        while self.show_sum_cards(bot) < 21:
            time.sleep(0.3)
            take_or_not = self.to_be_and_not_to_be(self.show_sum_cards(bot))
            if take_or_not:
                self.take_card(bot)    
            else:
                break    

    def to_be_and_not_to_be(self,sum_cards):
        number_of_cards = len(self.deck.cards) 
        happy_cards = 0
        max_sum = 21 - sum_cards 
        for card in self.deck.cards:
            if self.cards_values.get(card.rank) == 11:
                happy_cards += 1    
            elif self.cards_values.get(card.rank)<=max_sum:
                happy_cards += 1 
        lucky_list = [0]*(number_of_cards-happy_cards) + [1]*happy_cards
        return random.choice(lucky_list) 

    def show_totals(self):
        self.print_result()
        if self.show_sum_cards_final(self.my_player) == 21 and len(self.my_player.cards_on_hand) == 2:
            self.my_player.money += int(self.rate*1.5)
            self.dealer.money -= int(self.rate*1.5)
            print(f"Поздравляем, вы выиграли! {int(self.rate*1.5)}$")    
        else:
            if self.show_sum_cards_final(self.dealer) > self.show_sum_cards_final(self.my_player):
                self.my_player.money -= self.rate
                self.dealer.money += self.rate 
                print(f"Вы проиграли! {self.rate}$")                         
            elif self.show_sum_cards_final(self.dealer) < self.show_sum_cards_final(self.my_player):
                self.my_player.money += self.rate
                self.dealer.money -= self.rate
                print(f"Поздравляем, вы выиграли! {self.rate}$")
            else:
                print(f"У вас ничья с дилером!")  

        for bot in self.bot_list:
            if self.show_sum_cards_final(bot) == 21 and len(bot.cards_on_hand) == 2:
                bot.money += self.rate*1.5
                self.dealer.money -= self.rate*1.5
                print(f"{bot.name} выиграл! {self.rate*1.5}$")
            else:    
                if self.show_sum_cards_final(self.dealer) > self.show_sum_cards_final(bot):
                    bot.money -= self.rate
                    self.dealer.money += self.rate 
                    print(f"{bot.name} проиграл! {self.rate}$")                         
                elif self.show_sum_cards_final(self.dealer) < self.show_sum_cards_final(bot):
                    bot.money += self.rate
                    self.dealer.money -= self.rate
                    print(f"{bot.name} выиграл! {self.rate}$")
                else:
                    print(f"У {bot.name} ничья с дилером!")        

        self.print_money()

    def print_sum_cards(self,sum_cards):
        string = '{:>10} очков'.format(sum_cards)
        print(string)        

    def chance_of_success(self,sum_cards):
        number_of_cards = len(self.deck.cards) 
        happy_cards = 0
        max_sum = 21 - sum_cards 
        for card in self.deck.cards:
            if self.cards_values.get(card.rank) == 11:
                happy_cards += 1    
            elif self.cards_values.get(card.rank)<=max_sum:
                happy_cards += 1 
        chance = happy_cards/number_of_cards*100
        return round(chance,2)

    def input_validation_card(self):
        while True:
            if self.hints:
                print(f'Шанс вытянуть нужную карту = {self.chance_of_success(self.show_sum_cards(self.my_player))}%')
            inp = input(f'Вы хотите взять еще карту (y/n): ')
            if inp in ['n','y']:   
                return True if inp == 'y' else False

    def return_cards_to_deck(self):
        for i in range(len(self.my_player.cards_on_hand)):
            self.deck.cards.append(self.my_player.cards_on_hand.pop())    
        for i in range(len(self.dealer.cards_on_hand)):
            self.deck.cards.append(self.dealer.cards_on_hand.pop())
        for bot in self.bot_list:
            for i in range(len(bot.cards_on_hand)):
                self.deck.cards.append(bot.cards_on_hand.pop())    

        self.deck.shuffle()

    def dealer_playing(self):
        print("Играет дилер:")  
        time.sleep(0.3) 
        self.dealers_brain()
        time.sleep(1)
        self.show_totals()

    def bots_playing(self):    
        for bot in self.bot_list:
            if bot.money >= self.rate:
                print(f"Играет {bot.name}:")  
                time.sleep(0.3) 
                self.bots_brain(bot)
                time.sleep(0.3)
                if self.show_sum_cards(bot) > 21:
                    print("{:^20} перебрал!".format(bot.name))
                else:
                    print("{:^20} пассует!  результат:{} очков".format(bot.name,self.show_sum_cards(bot)))

    # Первоначальный набор карт всеми игроками
    def first_set_of_cards(self):
        print('Идет раздача карт')
        time.sleep(0.3)
        self.take_card(self.my_player,2)
        for bot in self.bot_list:
            time.sleep(0.3)
            if bot.money >= self.rate: 
                self.take_card(bot,2)
        time.sleep(0.3)        
        self.take_card(self.dealer,1)

    def save_file(self):
        my_dict = {}
        my_dict['my_player'] = {'name':self.my_player.name,'money':self.my_player.money}
        my_dict['dealer']    = {'name':self.dealer.name,'money':self.dealer.money}
        my_dict['bot_list']  = [{'name':bot.name,'money':bot.money } for bot in self.bot_list]
        # print(my_dict)
        # with open(self.save_file_name, 'a') as f:
        #     f.write(f'{my_dict}\n')
        with open(self.save_file_name, "w") as write_file:
            json.dump(my_dict, write_file,indent=4)

    @staticmethod
    def input_validation_play():
        while True:
            inp = input(f'Продолжить игру (y/n):')
            if inp in ['n','y']:   
                return True if inp == 'y' else False 

    @staticmethod
    def need_save_game():
        while True:
            inp = input(f'Вы можете сохранить игру и продолжить позже (y/n):')
            if inp in ['n','y']:   
                return True if inp == 'y' else False

    def start_game(self):   
        
        self.rate = int(input("Введите вашу ставку: "))
        if self.my_player.money >= self.rate:
            self.first_set_of_cards() # Первоначальный набор карт всеми игроками
        elif self.my_player.money == 0:   
            print('Вы все просрали!!!') 
            return 0
        else:
            print('У вас нет столько денег!')
            self.start_game()

        # Играете вы
        if self.show_sum_cards(self.my_player) == 21:
            print('Поздравляем вы набрали 21')    
        else:
            while self.input_validation_card():
                time.sleep(0.3)
                self.take_card(self.my_player) 
                if self.show_sum_cards(self.my_player) > 21:
                    print('У вас перебор')
                    break
                elif self.show_sum_cards(self.my_player) == 21:
                    print('Поздравляем вы набрали 21')    
                    break 

        # Играют боты
        self.bots_playing()            

        # Играет дилер
        self.dealer_playing()            

        # Продолжить или закончить игру?
        if self.input_validation_play():
            self.return_cards_to_deck()
            self.start_game() 
        else:
            if self.need_save_game():
                self.save_file()
                # save_game = input('Вы можете сохранить игру и продолжить позже (y/n):')    

def main():
    list_rank = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    if chr(3) == '':
        list_suit = [f'б',f'ч',f'к',f'п']
    else:
        list_suit = [f'{chr(3)}',f'{chr(4)}',f'{chr(5)}',f'{chr(6)}']    

    deck = Deck(list_rank,list_suit)
    deck.shuffle()
 
    my_name = input("Введите ваше имя: ")

    my_player = Player(my_name,100)

    dealer = Player('dealer',10000)

    amount_players = 7
    bot_list = []
    while amount_players not in [0,1,2,3,4,5]:
        amount_players = int(input("Сколько игроков(ботов) будет в игре (максимум 5)?: "))

    for i in range(1,amount_players+1):
        bot_list.append(Player(f'player_bot{i}',random.randrange(100, 200, 10)))

    # Если hints = True, тогда отображается процент вытянуть нужную карту?
    hints = False

    blackjack = BlackJack(deck,my_player,dealer,bot_list,hints)  
    blackjack.print_money()
    blackjack.start_game()
    
if __name__ == '__main__':
    main()
    

      





       

