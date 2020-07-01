class Player:
    def __init__(self, user):
        self.user = user
        self.score = 0
        self.words = []

    def getUser(self):
        return self.user
        
    def getMention(self):
        return self.user.mention

class Players:
    def __init__(self, message):
        self.players = []
        self.message = message

    async def init(self, bot_user):
        message_id = self.message.id
        channel = self.message.channel
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            if reaction.emoji == "⚡":
                async for user in reaction.users():
                    if user != bot_user and not user in self.players:
                        self.players.append(Player(user))

    def addPlayer(self, user):
        if not user in self.players:
            self.players.append(Player(user))

    def getUsers(self):
        users = []
        for player in self.players:
            users.append(player.getUser())
        return users

    def mentions(self):
        mentions = []
        for player in self.players:
            mentions.append(player.getMention())
        return mentions