from gameClass import Game
from playerClass import Player

def main():
    player = Player()
    game = Game(player=player)
    game.draw()

if __name__ == "__main__":
    main()