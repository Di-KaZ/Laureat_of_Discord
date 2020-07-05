from utils import format_tab

class Player:
    def __init__(self, user, categories, num_round):
        self.user = user
        self.categories = categories
        self.num_round = num_round
        self.board = [['' for x in range(len(categories) + 2)] for y in range(int(num_round) + 2)]
        # Inititalize board
        for i, category in enumerate(categories):
            self.board[0][i + 1] = category
        self.board[0][0] = user.name + '#' + user.discriminator
        self.board[0][len(categories) + 1] = 'Points'
        for i in range(1, num_round + 1):
            self.board[i][0] = '?'
            self.board[i][len(categories) + 1] = '?'
        self.message_board = None
        self.board[num_round + 1][len(categories)] = 'TOTAL'
        self.board[num_round + 1][len(categories) + 1] = '?'

    def getUser(self):
        return self.user
        
    def getMention(self):
        return self.user.mention

    def playerIsUser(self, user):
        return self.user == user
    
    async def roundStart(self, letter, num_round):
        self.board[num_round + 1][0] = letter
        if self.message_board == None:
            self.message_board = await self.user.send("```{}```".format("\n".join(format_tab(self.board))))
        else:
            await self.message_board.edit(content="```{}```".format("\n".join(format_tab(self.board))))

    async def addWord(self, num_category, word, actual_round):
        self.board[actual_round + 1][int(num_category)] = word
        if self.message_board:
            await self.message_board.edit(content="```{}```".format("\n".join(format_tab(self.board))))
        return

    async def finishRound(self, actual_round):
        for word in self.board[actual_round + 1]:
            if word == '':
                return False
        await self.message_board.delete(delay=0)
        self.message_board = await self.user.send("```{}```".format("\n".join(format_tab(self.board))))
        return True

    def getWordTab(self):
        return self.board

    def addScoreToRound(self, points, actual_round):
        if self.board[actual_round][len(self.categories) + 1].isalnum():
            prev_round_score = int(self.board[actual_round][len(self.categories) + 1])
        else:
            prev_round_score = 0
        self.board[actual_round][len(self.categories) + 1] = str(prev_round_score + points) 
        self.board[self.num_round + 1][len(self.categories) + 1] = str(self.getScore())

    def getRoundScore(self, actual_round):
        return self.board[actual_round][len(self.categories) + 1]

    def getScore(self):
        score = 0
        for i in range(1, self.num_round + 1):
            if self.board[i][len(self.categories) + 1].isalnum():
                score = score + int(self.board[i][len(self.categories) + 1])
            else:
                continue
        return score

class PlayersManager:
    def __init__(self, invitation, categories, num_round):
        self.categories = categories
        self.invitation = invitation
        self.num_round = num_round

    async def initPlayers(self, bot_user):
        players = []
        message_id = self.invitation.id
        channel = self.invitation.channel
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            if reaction.emoji == "⚡":
                async for user in reaction.users():
                    if user != bot_user and not user in players:
                        players.append(Player(user, self.categories, self.num_round))
        return players

    def addPlayer(self, players, new_user):
        for player in players:
            if new_user == player.getUser():
                return
        players.append(Player(new_user, self.categories, self.num_round))

    async def roundStart(self, players, letter, actual_round):
        for player in players:
            await player.roundStart(letter, actual_round)
    
    async def isPlayersRoundFinish(self, players, actual_round):
        for player in players:
            if await player.finishRound(actual_round):
                for player_two in players:
                    await player_two.getUser().send(f"Le round {actual_round + 1} est terminé {player.getUser().mention} est le premier a l'avoir terminé !")
                return True
        return False

    def getWordScore(self, words, word, num_players):
        if word == '':
            return 0
        word_count = words.count(word)
        if word_count == 1:
            return 2
        if word_count == num_players:
            return 0
        return 1

    """
        recup les mots d'une categorie x pour chaqun des joueurs au round y
        calculer le nombre de fois ou chaque mot apparait
        attribuer le score obtenable pour chaque mots
        donner le score du mots correspondant au player
    """

    def calculate_scores(self, players, actual_round, actual_category):
        words_occurence = []
        words_with_score = []
        for player in players: # les mots de chaque joueurs dans la categorie x au round y
            words_occurence.append(player.getWordTab()[actual_round][actual_category])
        dict_occurence = dict.fromkeys(words_occurence) #sans doublon
        for word in dict_occurence: # on associe mot et score
            if word == '':
                continue
            score = self.getWordScore(words_occurence, word, len(players))
            words_with_score.append((word, score))
        for player in players:
            for word_with_score in words_with_score:
                if player.getWordTab()[actual_round][actual_category] == word_with_score[0]:
                    player.addScoreToRound(word_with_score[1], actual_round)
                    break