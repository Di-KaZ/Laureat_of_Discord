from Player import Players
import random

def pretty2dtab(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return table

class Session:
    def __init__(self, message, creator, ground, categorys):
        self.message = message
        self.round = int(ground)
        self.creator = creator
        self.game_started = False
        self.categorys = categorys
        self.display_categorys = []
        self.players = None
        self.users = None
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.actual_round = 0
        for i, category in enumerate(self.categorys):
            self.display_categorys.append(str(i + 1) + '.' + category)

    async def start(self, user, bot_user, ctx):
        self.players = Players(self.message, self.categorys, self.round)
        await self.players.init(bot_user)
        self.players.addPlayer(self.creator)
        self.game_started = True
        await ctx.send("La partie de {} a commencé, les joueurs sont [{}]".format(self.creator.mention, ", ".join(self.players.mentions())))
        self.users = self.players.getUsers()
        self.letter = random.choice(self.alphabet) # chosing renadom letter 
        self.alphabet = self.alphabet.replace(self.letter, '') # removing letter from the game
        self.players.round_start(self.letter, self.actual_round)
        for user in self.users:
            await user.send("La partie a commencé !\nLa première lettre est : **{}**\nLes categories sont [**{}**]\nPour remplir une categorie faite le numero de la categorie suivit du mot.".format(self.letter, ', '.join(self.display_categorys)))

    async def stop(self, bot_user):
        self.players = Players(self.message, self.categorys, self.round)
        await self.players.init(bot_user)
        self.players.addPlayer(self.creator)

    def getOwner(self):
        return self.creator

    def getPlayers(self):
        return self.players
    
    def getUsers(self):
        return self.users

    async def new_round(self):
        for i in range(1, len(self.categorys) + 1):
            self.players.calculate_scores(self.actual_round + 1, i)
        self.actual_round += 1
        if await self.end_of_game():
            return True
        self.letter = random.choice(self.alphabet) # chosing renadom letter 
        self.alphabet = self.alphabet.replace(self.letter, '') # removing letter from the game
        self.players.round_start(self.letter, self.actual_round)
        players = self.players.getplayers()
        for player in players:
            await player.getUser().send("Ton score est de **{} pts**\n===== **Round {}** =====\nLa lettre est : **{}**\nLes catégories sont [**{}**]\nPour remplir une categorie faite le numero de la categorie suivit du mot.".format(player.getScore(), self.actual_round + 1, self.letter, ', '.join(self.display_categorys)))
        return False

    async def end_of_game(self):
        podium = []
        if self.actual_round >= self.round:
            players = self.players.getplayers()
            for player in players:
                podium.append((player.getUser(), player.getScore()))
                await player.getUser().send("La Partie est terminé ton score est de **{} pts**\n voici ton tableau ->\n```{}```".format(player.getScore(), '\n'.join(pretty2dtab(player.getWordTab()))))
                podium.sort(key=lambda x:x[1], reverse=True)
                podium_final = []
                for elem in podium:
                    podium_final.append(elem[0].name + '#' + elem[0].discriminator + '\t' + str(elem[1]) + ' pts')
            await self.message.channel.send("La partie de {} avec les catégories [**{}**] est terminé ({} rounds)\n```\t=====\tscores\t=====\t\n{}\n```=====\tboards\t=====\n".format(self.creator.mention, ', '.join(self.categorys), self.round, '\n'.join(podium_final), ))
            for player in self.players.getplayers():
                await self.message.channel.send("```{}```".format('\n'.join(pretty2dtab(player.getWordTab()))))
            return True

    async def reciveWord(self, user, message_str):
        for player in self.players.getplayers():
            if player.user_is_player(user):
                split_msg = message_str.split()
                if len(split_msg) != 2:
                    temp = await user.send(f"La conbinaison n'est pas valide **~~{message_str}~~**")
                    await temp.delete(delay=2)
                    return
                split_msg[1] = split_msg[1].upper()
                if not split_msg[0].isnumeric() or int(split_msg[0]) > len(self.categorys) or not split_msg[1].isalpha() or not split_msg[1].startswith(self.letter):
                    temp = await user.send(f"La conbinaison n'est pas valide **~~{message_str}~~**")
                    await temp.delete(delay=2)
                    return
                await player.register_word(split_msg[0], split_msg[1], self.actual_round)
                await user.send(f"**{split_msg[1]}** à été ajouté a votre catégorie** {self.categorys[int(split_msg[0]) - 1]}**.")
                if await self.players.is_players_round_finish(self.actual_round):
                    if await self.new_round():
                        return True
                    return False               
                await user.send("Les catégories sont [**{}**], La lettre est : **{}**".format(', '.join(self.display_categorys), self.letter))
        return False