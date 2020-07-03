class Session:
    def __init__(self, invitation, num_round, categories):
        self.invitation = invitation
        self.num_round = num_round
        self.categories = categories
        self.owner = invitation.author