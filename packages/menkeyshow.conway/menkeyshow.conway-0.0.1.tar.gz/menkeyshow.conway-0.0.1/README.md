# Conway's Game_of_Life
Python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

Conway's Game of Life is an automaton simulation with rather simple rules and a so called zero-player game.
After marking the status (alive/dead) of the cells, the programm simulates the life according to the following rules:

<ol>
<li>Any live cell with fewer than two live neighbours dies, as if by underpopulation.</li>
<li>Any live cell with two or three live neighbours lives on to the next generation.</li>
<li>Any live cell with more than three live neighbours dies, as if by overpopulation.</li>
<li>Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.</li>
</ol>


![](https://i.imgur.com/HLyO5s1.png)
