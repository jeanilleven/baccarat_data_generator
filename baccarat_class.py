import pandas as pd
import random
import datetime, time
from faker import Faker
from math import *
import csv

class Player:
  def __init__(self, name):
    self.name = name
    self.roller = random.choice(range(3))#0 - Low, 1 - Mid, 2 - High
    self.strategy = random.choice(range(4)) # 0 - Martingale, 1 - Fibonacci, 2 - Paroli, 3 - Labouchere 
    self.original_chips = self.generate_original_chips()
    self.total_chips = self.original_chips
    self.goal_chips = self.original_chips + self.original_chips*0.25
    self.starting_bet = self.generate_starting_bet()
    self.original_starting_bet = self.starting_bet
    self.num_of_games = self.generate_num_of_games()
    self.last_active_date = pd.to_datetime(self.random_date("7/25/2021 12:00 AM", "8/25/2021 12:00 AM", random.random()))
    self.num_of_playthroughs = 0
    self.num_of_sessions = 0
    self.labouchere_mainsequence = [self.starting_bet*0.25,self.starting_bet*0.5,self.starting_bet]
  def display_player_details(self):
    print(f"Name: {self.name}\nOriginal Chips: {self.original_chips}\nTotal Chips: {self.total_chips}\nGoal Chips: {self.goal_chips}\nRoller: {self.roller_details()}\nStarting Bet: {self.starting_bet}\nStrategy: {self.strategy_details()}")
  def roller_details(self):
    if self.roller == 0:
      roller = 'Low Roller'
    elif self.roller == 1:
      roller = 'Mid Roller'
    else:
      roller = 'High Roller'
    return roller

  def strategy_details(self):
    if self.strategy==0:
      strategy = 'Martingale'
    elif self.strategy==1:
      strategy = 'Fibonacci'
    elif self.strategy==2:
      strategy = 'Paroli'
    else:
      strategy = 'Labouchere'
    return strategy
  def generate_original_chips(self):
    low_roller = range(100, 201)
    mid_roller = range(500, 2001)
    high_roller = range(2000, 10001)

    if self.roller==0:
      original_chips = self.chips(low_roller)
    elif self.roller==1:
      original_chips = self.chips(mid_roller)
    else:
      original_chips = self.chips(high_roller)
    return original_chips
  def chips(self, chip_range):
        chips = random.choice(chip_range)
        while not (chips%100==0):
            chips = random.choice(chip_range)
        return chips

  def generate_starting_bet(self):
    # low_roller = range(10, 50)
    # mid_roller = range(50, 200)
    # high_roller = range(100, 1000)
    # if self.roller == 0 and self.strategy in range(0, 2):
    #   starting_bet = self.standardize_chips(low_roller)
    # elif self.roller == 1 and self.strategy in range(0, 2):
    #   starting_bet = self.standardize_chips(mid_roller)
    # elif self.roller == 2 and self.strategy in range(0, 2):
    #   starting_bet = self.standardize_chips(high_roller)
    # else:
    #   starting_bet = self.labouchere_mainsequence[0]+self.labouchere_mainsequence[-1] 
    return self.original_chips*0.05
  def standardize_chips(self,bet_range):
      bet = random.choice(bet_range)
      while not (bet%5==0):
          bet = random.choice(bet_range)
      return bet

  def generate_num_of_games(self):
    #return random.choice(range(5, 210))
    return random.choice(range(10, 210))

  def incomplete_playthroughs_and_has_chips(self):
    return True if self.num_of_playthroughs<self.num_of_games and self.total_chips>=self.original_starting_bet else False
  def goal_not_yet_achieved(self):
    return True if self.total_chips<self.goal_chips or self.num_of_playthroughs<10 else False

  def str_time_prop(self,start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))
 
  def random_date(self, start, end, prop):
    return self.str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)
 
class Session():
  def __init__(self, player):
    self.strategy = player.strategy
    self.original_starting_bet = player.original_starting_bet
    self.starting_bet = player.original_starting_bet
    self.original_chips = player.total_chips
    self.total_chips = player.total_chips
    self.goal_chips = player.goal_chips
    self.name = player.name
    self.num_of_games = player.num_of_games
    self.num_of_playthroughs = player.num_of_playthroughs
    self.list_of_games = []
    self.new_table = self.is_new_table(player.num_of_sessions)
    self.starting_date = player.last_active_date
    self.labouchere_mainsequence = player.labouchere_mainsequence
  
  def play_game(self):
    if self.strategy==0:
      self.martingale()
    elif self.strategy==1:
      self.fibonacci()
    elif self.strategy==2:
      self.paroli()
    else:
      SEQUENCE = self.labouchere()
      return SEQUENCE

  def martingale(self):
    DATE = self.starting_date
    STRATEGY = 'Martingale'
    BET_NUM = len(self.list_of_games)+1
    BET = STARTBET = PREV_BET = self.starting_bet
    CHIPS = self.original_chips
    WIN_STREAK = 0
    print('\nCurrently playing with Martingale System\n')
    while(self.ongoing_game(CHIPS, BET, WIN_STREAK)):
      self.num_of_playthroughs += 1
      print(f"{self.num_of_playthroughs}/{self.num_of_games}")
      WINNING_HAND = self.generate_winning_hand()[0]
      CHOICE = self.generate_choice()
      if self.won(WINNING_HAND, CHOICE):
          STATUS = 'W'
          PROFIT = BET if CHOICE=='Player' else BET*0.95 
          PREV_BET = BET
          BET = STARTBET
          WIN_STREAK+=1
      else:
          STATUS = 'L'
          PROFIT = BET*-1
          PREV_BET = BET
          BET = BET*2
          WIN_STREAK=0
          
      CHIPS += PROFIT
      added_seconds = random.choice(range(45, 76))
      DATE += datetime.timedelta(0, added_seconds)
      
      self.list_of_games.append([DATE, STRATEGY, BET_NUM,  self.name, PREV_BET, CHOICE, WINNING_HAND, STATUS, PROFIT, CHIPS])
      BET_NUM+=1
    self.total_chips = CHIPS
    self.starting_bet = BET
    self.write_to_file()
    self.session_data = pd.DataFrame(self.list_of_games, columns = ['DATE', 'STRATEGY','BET#', 'USERNAME','BET', 'CHOICE', 'WINNING_HAND','STATUS','PROFIT','CHIPS'])
    # print(f'{self.session_data}')
  
  def fibonacci(self):
    DATE = self.starting_date
    STRATEGY = 'Fibonacci'
    BET_NUM = len(self.list_of_games)+1
    BET = STARTBET = PREV_BET= self.starting_bet
    CHIPS = self.original_chips
    WIN_STREAK = 0
    base = STARTBET
    addend = 0
    print('\nCurrently playing with Fibonacci System\n')
    while(self.ongoing_game(CHIPS, BET, WIN_STREAK)):  
      self.num_of_playthroughs += 1
      print(f"{self.num_of_playthroughs}/{self.num_of_games}")
      WINNING_HAND = self.generate_winning_hand()[0]
      CHOICE = self.generate_choice()
      
      if self.won(WINNING_HAND, CHOICE):
        STATUS = 'W'
        PROFIT = BET if CHOICE=='Player' else BET*0.95 
        PREV_BET = BET
        BET = STARTBET
        base = 0
        addend = STARTBET
        WIN_STREAK+=1
      else:
        STATUS = 'L'
        PROFIT = BET*-1
        PREV_BET = BET
        base = addend
        addend = BET 
        BET = base+addend
        WIN_STREAK=0
      
      CHIPS += PROFIT
      added_seconds = random.choice(range(45, 76))
      DATE += datetime.timedelta(0, added_seconds)
      
      self.list_of_games.append([DATE, STRATEGY, BET_NUM,  self.name, PREV_BET, CHOICE, WINNING_HAND, STATUS, PROFIT, CHIPS])
      BET_NUM+=1
    self.total_chips = CHIPS
    self.starting_bet = BET
    self.write_to_file()
    self.session_data = pd.DataFrame(self.list_of_games, columns = ['DATE', 'STRATEGY','BET#', 'USERNAME','BET', 'CHOICE', 'WINNING_HAND','STATUS','PROFIT','CHIPS'])
  
  def paroli(self):
    DATE = self.starting_date
    
    STRATEGY = 'Paroli'
    BET_NUM = len(self.list_of_games)+1
    BET = STARTBET = PREV_BET = self.original_starting_bet
    CHIPS = self.original_chips
    
    WIN_STREAK = 0
    LOSE_STREAK = 0
    print('\nCurrently playing with Paroli System\n')
    while(self.ongoing_game(CHIPS, BET, WIN_STREAK if WIN_STREAK==3 else LOSE_STREAK)):    
      self.num_of_playthroughs += 1
      print(f"{self.num_of_playthroughs}/{self.num_of_games}")
      WINNING_HAND = self.generate_winning_hand()[0]
      CHOICE = self.generate_choice()
      
      if self.won(WINNING_HAND, CHOICE):
        STATUS = 'W'
        PROFIT = BET if CHOICE=='Player' else BET*0.95 
        WIN_STREAK = WIN_STREAK+1 if WIN_STREAK!=3 else 0
        PREV_BET = BET
        BET = BET*2 if WIN_STREAK!=3 else STARTBET  
        LOSE_STREAK = 0
      else:
        WIN_STREAK = 0
        LOSE_STREAK+=1
        STATUS = 'L'
        PROFIT = BET*-1
        PREV_BET = BET
        BET = STARTBET
      
      CHIPS += PROFIT
      added_seconds = random.choice(range(45, 76))
      DATE += datetime.timedelta(0, added_seconds)
      
      self.list_of_games.append([DATE, STRATEGY, BET_NUM,  self.name, PREV_BET, CHOICE, WINNING_HAND, STATUS, PROFIT, CHIPS])
      BET_NUM+=1
    self.starting_bet = BET
    self.total_chips = CHIPS 
    self.write_to_file()
    self.session_data = pd.DataFrame(self.list_of_games, columns = ['DATE', 'STRATEGY','BET#', 'USERNAME','BET', 'CHOICE', 'WINNING_HAND','STATUS','PROFIT','CHIPS'])

  def labouchere(self):
    DATE = self.starting_date

    STRATEGY = 'Labouchere'
    BET_NUM = len(self.list_of_games)+1
    CHIPS = self.original_chips
    
    SEQUENCE = MAINSEQUENCE = self.labouchere_mainsequence
    WIN_STREAK = 0
    LOSE_STREAK = 0
    BET = SEQUENCE[0]+SEQUENCE[-1] 
    print('\nCurrently playing with Labouchere System\n')
    while(self.ongoing_game(CHIPS, BET, WIN_STREAK if WIN_STREAK>LOSE_STREAK else LOSE_STREAK)):
      self.num_of_playthroughs += 1
      print(f"{self.num_of_playthroughs}/{self.num_of_games}")
      
      WINNING_HAND = self.generate_winning_hand()[0]
      CHOICE = self.generate_choice()
      if self.won(WINNING_HAND, CHOICE):
        STATUS = 'W'
        PROFIT = BET if CHOICE=='Player' else BET*0.95 
        SEQUENCE = SEQUENCE[1:-1]
        if not SEQUENCE:
          SEQUENCE = MAINSEQUENCE
        WIN_STREAK+=1
        LOSE_STREAK = 0
      else:
        STATUS = 'L'
        PROFIT = BET*-1
        SEQUENCE.append(SEQUENCE[0]+SEQUENCE[-1])
        WIN_STREAK=0
        LOSE_STREAK+=1
       
      CHIPS += PROFIT
      added_seconds = random.choice(range(45, 76))
      DATE += datetime.timedelta(0, added_seconds)
      self.list_of_games.append([DATE, STRATEGY, BET_NUM,  self.name, BET, CHOICE, WINNING_HAND, STATUS, PROFIT, CHIPS])
      BET_NUM+=1
      BET = SEQUENCE[0]+SEQUENCE[-1]
    self.total_chips = CHIPS    
    self.write_to_file()
    self.session_data = pd.DataFrame(self.list_of_games, columns = ['DATE', 'STRATEGY','BET#', 'USERNAME','BET', 'CHOICE', 'WINNING_HAND','STATUS','PROFIT','CHIPS'])

    return SEQUENCE
  
  def generate_winning_hand(self):
      return random.choices(['Player', 'Banker', 'Tie'], weights = [44.62, 45.86, 9.52])
  def generate_choice(self):
      return random.choice(['Player', 'Banker'])
  def won(self, WINNING_HAND, CHOICE):
      return True if WINNING_HAND==CHOICE else False

  def goal_not_achieved(self, CHIPS, BET, STREAK):
    # return True if CHIPS >= BET and STREAK<3 and CHIPS<self.goal_chips else False
    return True if CHIPS >= BET and STREAK<3 else False
  
  def ongoing_game(self, CHIPS, BET, STREAK):
    temp = self.goal_not_achieved(CHIPS, BET, STREAK)
    return True if self.num_of_playthroughs < self.num_of_games and temp else False
  def is_new_table(self, sessions):
    return True if sessions>0 else False
  def write_to_file(self):
    baccarat_data = open('baccarat_data.csv', 'a+', newline='')
    writer = csv.writer(baccarat_data)
    
    for game in self.list_of_games:
        writer.writerow(game)
    baccarat_data.close()

