import time, sys, os
from .game_logic.board_logic import board_logic
from .gui.gui import gui

__version__ = "0.0.1"


def start_game():
    "Starts a game"
    game_logic = board_logic(board_size=(15,15))
    game_gui = gui(game_logic.board_state)

    #TODO: use events and eventlisteners!
    while(game_gui.app_running):
        game_gui.root.update()
        game_gui.root.update_idletasks()
        game_gui.update_cell_buttons() #update gui

        
        while(game_gui.auto_update_state):
            game_gui.root.update()
            game_gui.root.update_idletasks()

            game_logic.set_state(game_gui.board_state) # GUI => LOGIC
            game_logic.calculate_next_board_state() # LOGIC calculates
            game_gui.board_state = game_logic.board_state # LOGIC => GUI
            game_gui.update_cell_buttons() # GUI update
            #time.sleep(0.1)
            
if __name__ == "__main__":
    start_game()
