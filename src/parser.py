
from os import kill
import re


PATTERN_NEW_GAME = r'([0-9]*):([0-9]*)\sInitGame:'
PATTERN_SHUTDOWNGAME_GAME = r'([0-9]*):([0-9]*)\sShutdownGame:'
PATTERN_END_GAME = r'([0-9]*):([0-9]*)\s(-{60})'
GAME_NAME = "game_"
KILL_TYPE_WORLD = r'([0-9]*):([0-9]*)\sKill:\s(\d*)\s(\d*)\s(\d*):\s<world>'
KILL_TYPE_BYPLAYER = r'([0-9]*):([0-9]*)\sKill:\s(\d*)\s(\d*)\s(\d*):\s'
    
class Parser:
    
    def __init__(self, log_file_path=''):
        self.log_file_path = log_file_path
        self.result = {}
        self.sorted_result = {}
          
    def __loadFile(self, log_file_path=''):
        log_file_path = log_file_path if log_file_path != '' else self.log_file_path
        file = open(log_file_path, 'r')
        return file.readlines()
    
    def __initGame(self):
        return  {
            "total_kills": 0,
            "players": [],
            "kills": {}
        }
    
    def __keyName(self, index=1):
        if index >0 and index <10:
            return GAME_NAME + '0' + str(index)
        else:
            return GAME_NAME + str(index)
    
    def __setPlayers(self, playersKeys, killers):
        for p in playersKeys:
            killers[p]= 0
            
        return killers
    
    def showResults(self):
        self.sorted_result = {}
        for key in sorted (self.result.keys()) :
            value = self.result[key]
            self.sorted_result[key] = value
            print(key, self.sorted_result[key])
            if self.sorted_result[key]['total_kills'] == 45:
                exit(0)
        
            
    def run(self):
        
        lines = self.__loadFile()
        game = self.__initGame()
        
        had_a_new_game = False
        game_count = 1
        unic_players = {}
        unic_killers = {}
        total_kills = 0
         
        for line in lines:
            
          match_new_game = re.findall(PATTERN_NEW_GAME, str(line))
          match_end_game = re.findall(PATTERN_END_GAME, str(line))
          match_shutdown_game = re.findall(PATTERN_SHUTDOWNGAME_GAME, str(line))
         
          
          if match_new_game:
              had_a_new_game = True              
               
          elif (match_end_game or match_shutdown_game) and  had_a_new_game:
                            
              game['total_kills'] = total_kills
              game['kills']= unic_players            
              game['players'] = list(dict.fromkeys(self.__setPlayers(unic_players.keys(), unic_killers)))
              
              self.result[self.__keyName(game_count)] = game
              game_count+= 1
              game = self.__initGame()
              had_a_new_game = False
              unic_players = {}
              unic_killers = {}
              total_kills = 0
          
          else:
              match_kill_type_world = re.findall(KILL_TYPE_WORLD, str(line))
              match_kill_type_by_player = re.findall(KILL_TYPE_BYPLAYER, str(line))
              
              if match_kill_type_world:
                  # TODO move to function
                  total_kills+= 1
                  keyword = "killed"
                  split_word = "by"
                  start = (line.index(keyword) + len(keyword))
                  player = line[start:].split(split_word)[0].strip()
                   #end todo
                   
                  if player in unic_players.keys():
                      unic_players[player] = unic_players[player] + 1
                  else :
                      unic_players[player] = 1
              
              elif match_kill_type_by_player:
                  
                  new_line = re.sub(KILL_TYPE_BYPLAYER, '', line)
                  
                  # todo move it to function
                  total_kills+= 1
                  keyword = "killed"
                  split_word = "by"
                  start = (line.index(keyword) + len(keyword))
                  
                  player = line[start:].split(split_word)[0].strip()
                  killer = new_line.split(keyword)[0].strip()
                  #end todo
                  
                  if player in unic_players.keys():
                      unic_players[player] = unic_players[player] + 1
                  else :
                      unic_players[player] = 1

                  if (killer in unic_killers.keys()) == False:
                      unic_killers[killer] = 0
                   
                        
               
    