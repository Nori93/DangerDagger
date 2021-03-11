from game import Game
import sys

app = Game(__file__)

while app.running:
    app.clock.tick(app.FPS)
    app.curr_menu.display_menu()
    app.game_loop()
