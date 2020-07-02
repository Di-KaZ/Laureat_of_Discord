from numpy import matrix

class Player:
    def __init__(self, user, categorys, ground):
        self.user = user
        self.categorys = categorys
        self.round = ground
        self.score = 0
        self.words = [['' for x in range(len(categorys) + 1)] for y in range(int(ground) + 1)]
        for i, category in enumerate(categorys):
            self.words[0][i + 1] = category

    def getUser(self):
        return self.user
        
    def getMention(self):
        return self.user.mention

    def user_is_player(self, user):
        return self.user == user
    
    def round_start(self, letter, ground):
        self.words[ground + 1][0] = letter

    async def register_word(self, category_num, word, actual_round):
        self.words[actual_round + 1][int(category_num)] = word
        return
    
    def finish_round(self, actual_round):
        for word in self.words[actual_round + 1]:
            if word == '':
                return False
        return True

    def getWordTab(self):
        return self.words

    def addScore(self, points):
        self.score += points

class Players:
    def __init__(self, message, categorys, ground):
        self.players = []
        self.categorys = categorys
        self.message = message
        self.ground = ground

    async def init(self, bot_user):
        message_id = self.message.id
        channel = self.message.channel
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            if reaction.emoji == "⚡":
                async for user in reaction.users():
                    if user != bot_user and not user in self.players:
                        self.players.append(Player(user, self.categorys, self.ground))

    def addPlayer(self, user):
        for player in self.players:
            if user == player.getUser():
                return
        self.players.append(Player(user, self.categorys, self.ground))

    def getUsers(self):
        users = []
        for player in self.players:
            users.append(player.getUser())
        return users

    def getplayers(self):
        return self.players

    def mentions(self):
        mentions = []
        for player in self.players:
            mentions.append(player.getMention())
        return mentions

    def round_start(self, letter, ground):
        for player in self.players:
            player.round_start(letter, ground)
    
    async def is_players_round_finish(self, actual_round):
        for player in self.players:
            if player.finish_round(actual_round):
                for user in self.getUsers():
                    await user.send(f"Le round {actual_round + 1} est terminé {player.getUser().mention} est le premier a l'avoir terminé !")
                return True
        return False
    def get_word_score(self, words, word, num_players):
        word_count = words.count(word)
        if word_count == 1:
            return 2
        if word_count == num_players:
            return 0
        return 1

    def calculate_scores(self):
        occurence = []
        acutal_round = 1
        actual_category = 1
        for player in self.players:
            if acutal_round >= self.ground:
                return
            if actual_category >= len(self.categorys):
                actual_category = 1
                acutal_round += 1
                dict_occurence = dict.fromkeys(occurence)
                word_with_score = []
                for word in dict_occurence:
                    score = self.get_word_score(occurence, word, len(self.players))
                    word_with_score.append((word, score))
            occurence.append(player.getWordTab()[acutal_round][actual_category])

# Lol mdr ye
# aha mdr de