from baccarat_class import Player, Session
import pandas as pd
import random
import datetime
from faker import Faker
from math import *
import csv
from random import shuffle, seed
from faker.providers.person.en import Provider
import numpy as np

names = pd.read_csv('uniquenames.csv')['Username'].values
random.shuffle(names)
names = names[:10000]
for name in names:
  player = Player(name)
  player.display_player_details()
  
  while player.incomplete_playthroughs_and_has_chips() and player.goal_not_yet_achieved():
    player.num_of_sessions+=1
    table = Session(player)
    sequence = table.play_game()
    player.total_chips = table.total_chips
    player.num_of_playthroughs=table.num_of_playthroughs

    added_seconds = random.choice(range(350, 500))
    player.last_active_date = table.list_of_games[-1][0]
    player.last_active_date += datetime.timedelta(0, added_seconds)
    
    player.display_player_details()
    print(f"\nTables Played: {player.num_of_sessions}\nTotal PlayThroughs: {player.num_of_games}\nTotal Games Played: {player.num_of_playthroughs}\n**")
    
    if player.strategy==3 and player.total_chips<sequence[0]+sequence[-1]: 
      break
