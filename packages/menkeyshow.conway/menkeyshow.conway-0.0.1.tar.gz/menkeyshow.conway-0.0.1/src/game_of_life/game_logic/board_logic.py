import numpy as np

#TODO: dictionary for alive and dead? => numbers? naaah
class board_logic(object):
    def __init__(self, board_size=(10,10), wrap_around_borders=True, board_state=None):
        self.board_size = board_size
        self.wrap_around_borders = wrap_around_borders

        # init board_state
        if(board_state is None):
            self.set_state(np.zeros(self.board_size, dtype=int))
        else:
            self.set_state(board_state)

    def set_state(self, state):
        """ Sets self.board_state and checks correct size."""
        if(np.shape(state) == self.board_size):
            self.board_state = np.array(state)
        else:
            raise Exception('The entered board-state doesn\'t '
                            'match the given size: %s.' % str(self.board_size))

    def get_number_neighbours_of_cell(self, x_cell, y_cell):
        """Return number of alive neighbour cells."""
        alive_neighbours = 0
        
        # neighbour indices
        x_indices = [x_cell-1, x_cell, x_cell+1]
        y_indices = [y_cell-1, y_cell, y_cell+1]


        #TODO: use functional programming ^^^^^^
        #x_indices = list(filter(lambda x: x < 0 and x > self.size[0], x_indices))
        #y_indices = list(filter(lambda y: y < 0 and y > self.size[1], y_indices))
            
        # correct indices for cell neighbours based on wrap_around_borders
        #TODO: this so far only works for x,y same size..
        if self.wrap_around_borders:
            for indices in [x_indices, y_indices]:
                if -1 in indices:
                    indices.remove(-1)
                    indices.append(self.board_size[0] - 1)
                if self.board_size[0] in indices:
                    indices.remove(self.board_size[0])
                    indices.append(0)
        else:
            for indices in [x_indices, y_indices]:
                if -1 in indices:
                    indices.remove(-1)
                if self.board_size[0] in indices:
                    indices.remove(self.board_size[0])

        # check each neighbour status and add to counter
        for x in x_indices:
            for y in y_indices:
                alive_neighbours = alive_neighbours + self.board_state[x][y]

        # dont count own value
        alive_neighbours = alive_neighbours - self.board_state[x_cell][y_cell]

        return alive_neighbours

    def next_state_of_cell(self, x_cell, y_cell):
        """ Calculates next cell state and returns its value."""
        neighbours = self.get_number_neighbours_of_cell(x_cell, y_cell)
        if(self.board_state[x_cell][y_cell] == 1):
            # Any live cell with more than three live neighbours dies, 
            # as if by overpopulation.
            if(neighbours > 3):
                return 0
            # Any live cell with fewer than two live neighbours dies,
            # as if by underpopulation.
            elif(neighbours < 2):
                return 0
            # Any live cell with two or three live neighbours lives
            # on to the next generation.
            else:
                return 1
        if(self.board_state[x_cell][y_cell] == 0):
            # Any dead cell with exactly three live neighbours becomes a live cell, 
            # as if by reproduction.
            if(neighbours == 3):
                return 1
            else:
                return 0
        
    def calculate_next_board_state(self):
        """Calculates next board state and updates self.state via set_state()"""
        new_board_state = np.zeros_like(self.board_state)

        for x in range(self.board_size[0]):
            for y in range(self.board_size[0]):
                new_board_state[x][y] = self.next_state_of_cell(x,y)
        
        self.set_state(new_board_state)




if __name__ == "__main__":
    game = board_logic()
    print(game.board_state)
    game2 = board_logic(
            board_state= [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0]])
    print(game2.board_state)
    game2.calculate_next_board_state()
    print(game2.board_state)
    def faulty_state():
        game2 = board_logic(
            board_state= [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1,2,3]])
        print(game2.board_state)
    #faulty_state()

