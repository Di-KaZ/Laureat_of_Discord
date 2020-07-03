class Category:
    def __init__(self, num, name):
        self.num = str(num)
        self.name = name
    
    def getFormatName(self):
        return self.num + '. ' + self.name

    def getName(self):
        return self.name