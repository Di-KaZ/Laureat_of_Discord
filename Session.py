from Player import Player, PlayersManager
import random
from text import *
from utils import *

class Session:
    def __init__(self, invitation, owner, num_round, categories):
        self.invitation = invitation
        self.num_round = num_round
        self.categories = categories
        self.owner = owner
        self.actual_round = 0
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.categories = categories #numerate_categories(categories)
        self.player_manager = PlayersManager(invitation, categories, num_round)
        self.players = []
    
    async def start(self, bot_user):
        self.players = await self.player_manager.initPlayers(bot_user)
        self.player_manager.addPlayer(self.players, self.owner)
        self.game_started = True
        await self.invitation.channel.send(g_start_session.format(self.owner.mention))
        self.letter = random.choice(self.alphabet) # chosing renadom letter 
        self.alphabet = self.alphabet.replace(self.letter, '') # removing letter from the game
        self.player_manager.roundStart(self.players, self.letter, self.actual_round)
        for player in self.players:
            await player.getUser().send(g_start_session_player.format(self.letter, ', '.join(self.categories)))

    async def stop(self, bot_user):
        await self.player_manager.initPlayers(bot_user)
        self.player_manager.addPlayer(self.players, self.owner)

    def getOwner(self):
        return self.owner

    def getPlayers(self):
        return self.players
    
    def isUserInSession(self, user):
        for player in self.players:
            if user == player.getUser():
                return True
        return False

    async def new_round(self):
        for i in range(1, len(self.categories) + 1):
            self.player_manager.calculate_scores(self.players, self.actual_round + 1, i)
        self.actual_round += 1
        if await self.end_of_game():
            return True
        self.letter = random.choice(self.alphabet) # chosing renadom letter 
        self.alphabet = self.alphabet.replace(self.letter, '') # removing letter from the session
        self.player_manager.roundStart(self.players, self.letter, self.actual_round)
        for player in self.players:
            await player.getUser().send(g_new_round_player.format(player.getRoundScore(self.actual_round), self.actual_round + 1, self.letter, ', '.join(self.categories)))
        return False

    async def end_of_game(self):
        podium = []
        if self.actual_round >= self.num_round:
            for player in self.players:
                podium.append((player.getUser(), player.getScore()))
                await player.getUser().send(g_end_session_player.format(player.getScore(), '\n'.join(format_tab(player.getWordTab()))))
                podium.sort(key=lambda x:x[1], reverse=True)
                podium_final = []
                for elem in podium:
                    podium_final.append(elem[0].name + '#' + elem[0].discriminator + '\t' + str(elem[1]) + ' pts')
            await self.invitation.channel.send(g_end_session.format(self.owner.mention, ', '.join(self.categories), self.num_round, '\n'.join(podium_final)))
            return True
        return False

    async def reciveWord(self, user, message_str):
        for player in self.players:
            if player.playerIsUser(user):
                split_msg = message_str.split()
                if len(split_msg) != 2:
                    temp = await user.send(g_invalid_word.format(message_str))
                    await temp.delete(delay=2)
                    return False
                split_msg[1] = split_msg[1].upper()
                if not split_msg[0].isnumeric() or int(split_msg[0]) > len(self.categories) or not split_msg[1].isalpha() or not split_msg[1].startswith(self.letter):
                    temp = await user.send(g_invalid_word.format(message_str))
                    await temp.delete(delay=2)
                    return False
                print(split_msg[0])
                print(split_msg[1])
                print(self.actual_round)
                player.addWord(split_msg[0], split_msg[1], self.actual_round)
                await player.getUser().send(g_added_word.format(split_msg[1], self.categories[int(split_msg[0]) - 1]))
                if await self.player_manager.isPlayersRoundFinish(self.players, self.actual_round):
                    if await self.new_round():
                        return True
                    return False               
                await player.getUser().send(g_new_round_annonce.format(', '.join(self.categories), self.letter))
        return False
