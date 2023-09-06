class Team:
    def __init__(self, name: str, url: str):
        self.plays = False
        self.time = None
        self.name = name
        self.url = url

    def getname(self) -> str:
        return self.name

    def geturl(self) -> str:
        return self.url

    def setplays(self, juega):
        self.plays = juega

    def settime(self, time):
        self.time = time
