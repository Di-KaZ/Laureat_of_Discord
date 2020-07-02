from Player import Players
import random

class Session:
    def __init__(self, message, categorys):
        self.message = message
        self.creator = message.author
        self.game_started = False
        self.categorys = categorys
        self.players = None
        self.users = None
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
              
    async def start(self, user, bot_user, ctx):
        self.players = Players(self.message)
        await self.players.init(bot_user)
        self.players.addPlayer(self.creator)
        self.game_started = True
        await ctx.send("Started game with players : [{}]".format(", ".join(self.players.mentions())))
        self.users = self.players.getUsers()
        self.game_started = True
        self.letter = random.choice(self.alphabet) # chosing renadom letter 
        self.alphabet = self.alphabet.replace(self.letter, '') # removing letter from the game
        for user in self.users:
            await user.send("Game as Started !\nThe first letter is : **{}**\nCategory are [**{}**]\nTo enter a word in a category just type 1 to 6 (order of category) and your word".format(self.letter, ', '.join(self.categorys)))


    async def stop(self, bot_user):
        self.players = Players(self.message)
        await self.players.init(bot_user)
        self.players.addPlayer(self.creator)

    def getOwner(self):
        return self.creator

    def getPlayers(self):
        return self.players
    
    def getUsers(self):
        return self.users

    async def reciveWord(self, user, message_str):
        for player in self.players.getplayers():
            if player.user_is_player(user):
                split_msg = message_str.split()
                split_msg[1] = split_msg[1].upper()
                if len(split_msg) != 2 or not split_msg[0].isnumeric() or int(split_msg[0]) > len(self.categorys) or not split_msg[1].isalpha() or not split_msg[1].startswith(self.letter):
                    temp = await user.send(f"**Invalid input ~~{message_str}~~**")
                    temp.delete(delay=5)
                    return
                await player.register_word(split_msg[0], split_msg[1])
                await user.send(f"**{split_msg[1]}** added in category **{self.categorys[int(split_msg[0]) - 1]}**.")                