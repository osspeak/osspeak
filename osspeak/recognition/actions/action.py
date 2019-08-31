class Action:
    
    def __init__(self, pieces):
        self.pieces = pieces

    def perform(self):
        for piece in self.pieces:
            piece.perform()