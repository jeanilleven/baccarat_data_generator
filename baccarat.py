import pandas as pd
import random
import datetime
from faker import Faker
from math import *
import csv

pd.set_option('display.max_rows', 100)

class Session:
    def __init__(self, is_new_session):
        self.generate_player_details()
        self.generate_games()
        self.starting_bet = self.generate_start_bet(is_new_session)
        self.list_of_games = []
        self.session_data=[]
        
    def display_details(self):
        print(f'Player: {self.name}\nChips: {self.original_chips}\nSystem: {self.system}\nGames: {self.num_of_games}\nStarting bet: {self.starting_bet}')
    
    def generate_start_bet(self):
        low_roller = range(10, 50)
        mid_roller = range(50, 200)
        high_roller = range(100, 1000)
        if self.roller == 0:
            self.starting_bet = self.standardize_chips(low_roller)
        elif self.roller == 1:
            self.starting_bet = self.standardize_chips(mid_roller)
        else:
            self.starting_bet = self.standardize_chips(high_roller)
#         self.starting_bet = 10

    def standardize_chips(self,bet_range):
        bet = random.choice(bet_range)
        while not (bet%5==0):
            bet = random.choice(bet_range)
        return bet
    
    def play_game(self):
        if self.system==0:
            self.martingale()
        elif self.system==1:
            self.fibonacci()
        elif self.system==2:
            self.paroli()
        else:
            self.labouchere()
        
    def martingale(self):
        DATE = datetime.datetime.now()
        STRATEGY = 'Martingale'
        BET_NUM = len(self.list_of_games)+1
        BET = STARTBET = PREV_BET = self.starting_bet
        CHIPS = self.original_chips
        
        print('\nCurrently playing with Martingale System\n')
        while(BET_NUM<=self.num_of_games):
            WINNING_HAND = self.generate_winning_hand()[0]
            CHOICE = self.generate_choice()
            
            if self.won(WINNING_HAND, CHOICE):
                STATUS = 'W'
                PROFIT = BET if CHOICE=='Player' else BET*0.95 
                PREV_BET = BET
                BET = STARTBET
            else:
                STATUS = 'L'
                PROFIT = BET*-1
                PREV_BET = BET
                BET = BET*2
                
            CHIPS += PROFIT
                
            added_seconds = random.choice(range(45, 76))
            DATE += datetime.timedelta(0, added_seconds)
            
            self.list_of_games.append([DATE, STRATEGY, BET_NUM,  self.name, PREV_BET, CHOICE, WINNING_HAND, STATUS, PROFIT, CHIPS])
            BET_NUM+=1
        self.write_to_file()
        self.session_data = pd.DataFrame(self.list_of_games, columns = ['DATE', 'STRATEGY','BET#', 'USERNAME','BET', 'CHOICE', 'WINNING_HAND','STATUS','PROFIT','CHIPS'])
        print(f'{self.session_data}')

    def fibonacci(self):
        DATE = datetime.datetime.now()
        STRATEGY = 'Fibonacci'
        BET_NUM = len(self.list_of_games)+1
        BET = STARTBET = PREV_BET= self.starting_bet
        CHIPS = self.original_chips
        
        base = STARTBET
        addend = 0
        print('\nCurrently playing with Fibonacci System\n')
        while(BET_NUM<=self.num_of_games):  
            WINNING_HAND = self.generate_winning_hand()[0]
            CHOICE = self.generate_choice()
            
            if self.won(WINNING_HAND, CHOICE):
                STATUS = 'W'
                PROFIT = BET if CHOICE=='Player' else BET*0.95 
                PREV_BET = BET
                BET = STARTBET
                base = 0
                addend = STARTBET
            else:
                STATUS = 'L'
                PROFIT = BET*-1
                PREV_BET = BET
                base = addend
                addend = BET 
                BET = base+addend
            
            CHIPS += PROFIT
            added_seconds = random.choice(range(45, 76))
            DATE += datetime.timedelta(0, added_seconds)
            
            self.list_of_games.append([DATE, STRATEGY, BET_NUM,  self.name, PREV_BET, CHOICE, WINNING_HAND, STATUS, PROFIT, CHIPS])
            BET_NUM+=1
        self.write_to_file()
        self.session_data = pd.DataFrame(self.list_of_games, columns = ['DATE', 'STRATEGY','BET#', 'USERNAME','BET', 'CHOICE', 'WINNING_HAND','STATUS','PROFIT','CHIPS'])
        print(f'{self.session_data}')

    def paroli(self):
        DATE = datetime.datetime.now()
        STRATEGY = 'Paroli'
        BET_NUM = len(self.list_of_games)+1
        BET = STARTBET = PREV_BET = self.starting_bet
        CHIPS = self.original_chips
        
        STREAK = 0
        print('\nCurrently playing with Paroli System\n')
        while(BET_NUM<=self.num_of_games):    
            WINNING_HAND = self.generate_winning_hand()[0]
            CHOICE = self.generate_choice()
            
            if self.won(WINNING_HAND, CHOICE):
                STATUS = 'W'
                PROFIT = BET if CHOICE=='Player' else BET*0.95 
                STREAK = STREAK+1 if STREAK!=3 else 0
                PREV_BET = BET
                BET = BET*2 if STREAK!=3 else STARTBET  
            else:
                STREAK = 0
                STATUS = 'L'
                PROFIT = BET*-1
                PREV_BET = BET
                BET = STARTBET
            
            CHIPS += PROFIT
                
            added_seconds = random.choice(range(45, 76))
            DATE += datetime.timedelta(0, added_seconds)
            
            self.list_of_games.append([DATE, STRATEGY, BET_NUM,  self.name, PREV_BET, CHOICE, WINNING_HAND, STATUS, PROFIT, CHIPS])
            BET_NUM+=1
        self.write_to_file()
        self.session_data = pd.DataFrame(self.list_of_games, columns = ['DATE', 'STRATEGY','BET#', 'USERNAME','BET', 'CHOICE', 'WINNING_HAND','STATUS','PROFIT','CHIPS'])
        print(f'{self.session_data}')
        
    def labouchere(self):
        DATE = datetime.datetime.now()
        STRATEGY = 'Labouchere'
        BET_NUM = len(self.list_of_games)+1
        CHIPS = self.original_chips
        
        SEQUENCE = MAINSEQUENCE = [10, 20, 30]
        
        print('\nCurrently playing with Labouchere System\n')
        while(BET_NUM<=self.num_of_games):
            if not SEQUENCE:
                SEQUENCE = [10,20,30]
            
            BET = SEQUENCE[0] + SEQUENCE[-1]
            WINNING_HAND = self.generate_winning_hand()[0]
            CHOICE = self.generate_choice()
            
            if self.won(WINNING_HAND, CHOICE):
                STATUS = 'W'
                PROFIT = BET if CHOICE=='Player' else BET*0.95 
                SEQUENCE = SEQUENCE[1:-1]
            else:
                STATUS = 'L'
                PROFIT = BET*-1
                if SEQUENCE:
                    seq_item = SEQUENCE[0]+SEQUENCE[-1]
                    SEQUENCE.append(seq_item)
            print(SEQUENCE)    
            CHIPS += PROFIT
            
            added_seconds = random.choice(range(45, 76))
            DATE += datetime.timedelta(0, added_seconds)
            self.list_of_games.append([DATE, STRATEGY, BET_NUM,  self.name, BET, CHOICE, WINNING_HAND, STATUS, PROFIT, CHIPS])
            BET_NUM+=1
            
        self.write_to_file()
        self.session_data = pd.DataFrame(self.list_of_games, columns = ['DATE', 'STRATEGY','BET#', 'USERNAME','BET', 'CHOICE', 'WINNING_HAND','STATUS','PROFIT','CHIPS'])
        print(f'{self.session_data}')
    def generate_winning_hand(self):
        return random.choices(['Player', 'Banker', 'Tie'], weights = [4.462, 4.586, 0.952])
    def generate_choice(self):
        return random.choice(['Player', 'Banker'])
    def won(self, WINNING_HAND, CHOICE):
        return True if WINNING_HAND==CHOICE else False

    def chips(self, chip_range):
        chips = random.choice(chip_range)
        while not (chips%100==0):
            chips = random.choice(chip_range)
        return chips
    
    def generate_player_details(self):  
        self.name = Faker().name()
        self.roller = random.choice(range(0, 3))#0 - Low, 1 - Mid, 2 - High
        self.system = random.choice(range(4)) # 0 - Martingale, 1 - Fibonacci, 2 - Paroli, 3 - Labouchere 
        low_roller = range(100, 501)
        mid_roller = range(500, 2001)
        high_roller = range(2000, 10001)

        if self.roller==0:
            self.original_chips = self.chips(low_roller)
        elif self.roller==1:
            self.original_chips = self.chips(mid_roller)
        else:
            self.original_chips = self.chips(high_roller)
        
    def generate_games(self):
        self.num_of_games = random.choice(range(5, 210))
    
    def write_to_file(self):
        baccarat_data = open('baccarat_data.csv', 'a+', newline='')
        writer = csv.writer(baccarat_data)
        
        for game in self.list_of_games:
            writer.writerow(game)
        baccarat_data.close()

for i in range(3):
    session = Session()
    session.display_details()
    session.play_game()