import random
import time

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
    def __init__(self,deck,my_player,dealer):   
        self.cards = deck 
        self.dealer = dealer     
        self.my_player = my_player
        self.cards_values = self.get_cards_values()

    def print_money(self):   
        print(f'{self.my_player.name}: {self.my_player.money}   Dealer money: {self.dealer.money}')

    def get_cards_values(self):
        return {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10,"A":11}

    def take_card(self,player,count=1):
        while count != 0:
            player.cards_on_hand.append(self.cards.cards.pop())
            count -=1
        self.show_cards(player)
        self.print_sum_cards(self.show_sum_cards(player))

    def show_cards(self,player): 
        print(f'Player:{player.name}',end = ' ')
        for card in player.cards_on_hand:
            print(card,end = ' ')   

    def show_sum_cards(self,player): 
        sum_cards = 0
        for card in player.cards_on_hand:
            sum_cards += self.cards_values.get(card.rank) 
        return sum_cards

    def show_sum_cards_1(self,player): 
        sum_cards = 0
        for card in player.cards_on_hand:
            sum_cards += self.cards_values.get(card.rank)
        if sum_cards > 21:
            return 0        
        return sum_cards    

    def dealers_brain(self): 
        player_sum = self.show_sum_cards(self.my_player)
        if player_sum <= 21:
            while self.show_sum_cards(self.dealer) < player_sum :
                self.take_card(self.dealer) 

    def show_totals(self):
        if self.show_sum_cards_1(self.dealer) > self.show_sum_cards_1(self.my_player):
            self.my_player.money -= self.rate
            self.dealer.money += self.rate 
            print(f"Вы проиграли! {self.rate}$")                         
        elif self.show_sum_cards_1(self.dealer) < self.show_sum_cards_1(self.my_player):
            self.my_player.money += self.rate
            self.dealer.money -= self.rate
            print(f"Поздравляем, вы выиграли! {self.rate}$")
        self.print_money()

    def print_sum_cards(self,sum_cards):
        print(f'    {sum_cards} очков:')        

    def input_validation_card(self):
        while True:
            inp = input(f'Вы хотите взять еще карту (y/n):')
            if inp in ['n','y']:   
                return True if inp == 'y' else False

    def input_validation_play(self):
        while True:
            inp = input(f'Продолжить игру (y/n):')
            if inp in ['n','y']:   
                return True if inp == 'y' else False            
     
    def return_cards_to_deck(self):
        for i in range(len(self.my_player.cards_on_hand)):
            self.cards.cards.append(self.my_player.cards_on_hand.pop())    
        for i in range(len(self.dealer.cards_on_hand)):
            self.cards.cards.append(self.dealer.cards_on_hand.pop())
        self.cards.shuffle()

    def start_game(self):   
        
        self.rate = int(input("Введите вашу ставку: "))
        if self.my_player.money >= self.rate:
            self.take_card(self.my_player,2)    
        if self.show_sum_cards(self.my_player) == 21:
            print('Поздравляем вы набрали 21')    
        else:
            while self.input_validation_card():
                self.take_card(self.my_player) 
                if self.show_sum_cards(self.my_player) > 21:
                    print('У вас перебор')
                    break
                elif self.show_sum_cards(self.my_player) == 21:
                    print('Поздравляем вы набрали 21')    
                    break 

        print("Карты берет дилер:")  
        time.sleep(2) 
        if self.dealer.money > self.rate:
            self.take_card(self.dealer,2)
        time.sleep(2)
        self.dealers_brain()
        time.sleep(2)
        self.show_totals()

        if self.input_validation_play():
            self.return_cards_to_deck()
            self.start_game() 

def main():
    list_rank = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    list_suit = [chr(3),chr(4),chr(5),chr(6)]

    deck = Deck(list_rank,list_suit)
    deck.shuffle()
 
    my_name = input("Введите ваше имя: ")
    my_player = Player(my_name,100)

    dealer = Player('dealer',10000)

    blackjack = BlackJack(deck,my_player,dealer)  
    blackjack.print_money()
    blackjack.start_game()
    
if __name__ == '__main__':
    main()

        





       

