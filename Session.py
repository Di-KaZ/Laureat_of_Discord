from Player import Players

class Session:
    def __init__(self, message, categorys):
        self.message = message
        self.creator = message.author
        self.game_started = False
        self.categorys = categorys
        self.players = None
    
    async def start(self, user, bot_user, ctx):
        self.players = Players(self.message)
        await self.players.init(bot_user)
        self.players.addPlayer(self.creator)
        self.game_started = True
        await ctx.send("Started game with players : [{}]".format(", ".join(self.players.mentions())))
        for player in self.players:
            await player.getUser().send("Hey !")

    async def stop(self, bot_user):
        self.players = Players(self.message)
        await self.players.init(bot_user)
        self.players.addPlayer(self.creator)

    def getOwner(self):
        return self.creator

    def getPlayers(self):
        return self.players