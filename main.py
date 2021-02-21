from game import Game

g = Game()

while g.running:
    g.clock.tick(g.FPS)
    g.curr_menu.display_menu()
    g.game_loop()