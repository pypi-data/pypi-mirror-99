import tkinter as tk
import numpy as np
#from ..grid.grid import gamegrid
#TODO: dictionary for colours => cell_status

class gui(object):
    """ Main windows for game of life.

    Handles board state and updates of cells.
    """
    def __init__(self, board_state):
        self.board_state = board_state
        self.board_size = (np.shape(self.board_state)[0],
                            np.shape(self.board_state)[1])
        self.auto_update_state = False
        self.app_running = True

        self.init_main_window()

    def init_main_window(self):
        # root window
        self.root = tk.Tk()
        self.root.title("Conway's Game of Life")

        # frame for all cell buttons
        self.master = tk.Frame(self.root)
        self.master.pack()

        # Buttons
        self.auto_update_button = tk.Button(self.root, text="Start", 
                                        command=(lambda:self.auto_update_toggle()))
        self.auto_update_button.pack()
        self.initialize_cell_buttons()

    def initialize_cell_buttons(self):
        """ Creates tk Buttons and stores them in self.buttons.

        Each button is assigned a cell with it's corresponding indices.
        """
        self.cell_buttons = np.zeros_like(self.board_state, dtype=object)

        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                # each frame holds its button
                cellframe = tk.Frame(self.master, height=20, width=20)
                cellframe.grid_propagate(False) # disables resizing of frame
                cellframe.columnconfigure(0, weight=1) # enables button to fill frame
                cellframe.rowconfigure(0,weight=1) # any positive number would do the trick  
                cellframe.grid(row=x, column=y) # place frame according to boardstate

                cellbutton = tk.Button(cellframe, bg='gray25', 
                                    command=(lambda x=x, y=y: self.cell_button_press(x,y)))
                cellbutton.grid(sticky='wens') # expanding buttons

                # save buttons for later configurations
                self.cell_buttons[x][y] = cellbutton

    def update_cell_buttons(self):
        """ Updates the colours of each Button.

        Cell status is retrieved via self.state.
        """
        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                cell_status = self.board_state[x][y]
                if cell_status == 1:
                    self.cell_buttons[x][y].config(bg='red2')
                if cell_status == 0:
                    self.cell_buttons[x][y].config(bg='gray25')

    def cell_button_press(self, x, y):
        """ On button press updates board_state.
        """
        button = self.cell_buttons[x][y]
        cell_status = self.board_state[x][y]
        if cell_status == 1:
            button.config(bg='gray25')
            self.board_state[x][y] = 0
        if cell_status == 0:
            button.config(bg="red2")
            self.board_state[x][y] = 1
    
    def set_state(self, board_state):
        """ Set board_state and update cell buttons.
        """
        #TODO: try catch, size of board_state has to remain the same
        self.board_state = board_state
        self.update_cell_buttons()
    
    def auto_update_toggle(self):
        """ Decide to auto update cells, or not.
        """
        self.auto_update_state = not self.auto_update_state
        if self.auto_update_state:
            self.auto_update_button.config(text="Pause")
        else:
            self.auto_update_button.config(text="Start")


if __name__ == "__main__":
    game_gui = gui(board_state=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0]])
    game_gui.update_cell_buttons()

    while(game_gui.app_running):
    
        game_gui.root.update()
        game_gui.root.update_idletasks()
        while(game_gui.auto_update_state):
            game_gui.root.update()
            game_gui.root.update_idletasks()
            game_gui.update_cell_buttons()
