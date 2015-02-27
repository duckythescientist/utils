import socket

# the print statement with "~" to start are things that I added

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("edgy.2015.ghostintheshellcode.com", 44440))
"""
~puzzle
---------
|xxxx x |
|x  x x |
| x     |
| x @ xx|
|       |
|  xx   |
|x x x  |
---------
You have a maximum of 3 moves
"""
"""
~puzzle
You hit a mine at X/Y 6/5
"""
"""SD D D AW SSSA DDDS SAA SDD """


def more_recv(s):  # Rely on timeouts to grab all available data
    alldata = ""
    try:
        data = s.recv(4096)
        while data:
            alldata += data
            data = s.recv(4096)
    except:
        pass
    return alldata

def parser(puzzle):  # Get puzzle data from the text
    lines = puzzle.split("\n")
    # print lines
    grid = []
    startr, startc = 0, 0
    curr_r = 0
    for line in lines:
        if line and line[0] == "|":
            grid.append([1 if c=="x" else 0 for c in line if c != "|"])
            startpos = line.find("@") 
            if startpos != -1:
                startr, startc = curr_r, startpos-1
            curr_r += 1
        if line and line.find("have a maximum") != -1:
            moves = [int(s) for s in line.split() if s.isdigit()][0]

    # print grid
    # print startr, startc
    # print moves

    # grid contains a 1 for every X, startr and startc are the @ location
    return grid, startr, startc, moves

# Check if a solution solves the puzzle
# Returns two booleans. The first is if the solution is valid.
# The second boolean is true if the solution failed miserably 
# (either hitting a wall before the pattern repeats or backtracking)
def checker(grid, startr, startc, solution):
    # print "trying:", solution
    maxr = len(grid)
    maxc = len(grid[0])
    currr, currc = startr, startc
    i = 0
    max_steps = maxr*maxc
    visits = set()
    lensol = len(solution)
    while 0 <= currr < maxr and 0 <= currc < maxc and i < max_steps:
        if grid[currr][currc]:
            return False, i < lensol
        if i <= lensol:
            if (currr,currc,) in visits:
                # print "~killed loop"
                return False, True
            if i < lensol:
                visits.add((currr,currc,))
        move = solution[i%lensol]
        if move == "W":
            currr -= 1
        elif move == "A":
            currc -= 1
        elif move == "S":
            currr += 1
        elif move == "D":
            currc += 1
        else:
            print "YOU DONE FUCKED UP"
            return False, True
        i += 1
    if i == max_steps:
        return False, True
    return True, False

def test_things():
    grid = [[1, 1, 1, 1, 0, 1, 0], [1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0]]
    print checker(grid, 3, 3, "SD")
    print checker(grid, 3, 3, "WD")
    print "solution at", do_search(grid, 3, 3, 3)

# BFS from a known starting partial solution
def do_partial_search(grid, startr, startc, maxdepth, startsolution):
    solutions = [startsolution]
    solved = False
    while not solved and len(solutions):    
        new_solutions = []
        # print solutions
        for solution in solutions:
            good, earlyfail = checker(grid, startr, startc, solution)
            if good:
                # print "success"
                return solution
            if len(solution) < maxdepth and not earlyfail:
                for l in "WASD":
                    new_solutions.append(solution + l)
        solutions = new_solutions
    return None

def do_search(grid, startr, startc, maxdepth):
    # Try one start letter at a time because the full BFS overflows the maxlen of a python list
    for attempt in "WASD":
        # print "~Trying", attempt
        solution = do_partial_search(grid, startr, startc, maxdepth, attempt)
        if solution:
            return solution




# Hardcoded solutions for the first few puzzles before they are randomized
solutions = "SD D D AW SSSA DDDS SAA SDD AWAAW AAAASSAA WAAA SDDDDDD S AAAAAAAS".split()

win = 0
# test_things()
# raw_input()
while not win:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("edgy.2015.ghostintheshellcode.com", 44440))
    s.settimeout(0.5)  # IMPORTANT FOR THE more_recv FUNCTION. 0.5 works nicely for me -duck
    print(s.recv(1024))  # get the intro banner
    s.send("EdgesAreFun\n")  # send PW WITH NEWLINE
    chaf = s.recv(4096)  # Game instructions
    print "~chaf"
    print chaf
    count = 0
    while not win:
        count += 1
        puzzle = more_recv(s)  # Grab the puzzle
        print "~puzzle"
        print puzzle
        if not puzzle:
            continue
        if puzzle.find("mine") != -1:  # We hit an X
            # Done goofed
            break
        if puzzle.find("maximum") == -1:  # We didn't see a full puzzle
            # Something happened
            print "~SOMETHING HAPPENED"
            raw_input()

        # if len(solutions) < count:
        #     solutions.append(raw_input())
        # s.send("SDD\n")
        # s.send(solutions[count-1] + "\n")

        if count <= len(solutions):  # Use hardcoded values for the first ones
            s.send(solutions[count-1] + "\n")
        else:
            # print "PANIC"
            solution = do_search(*parser(puzzle))  # parse puzzle, search, get solution
            print "~Solution at", solution
            s.send(solution + "\n")  # Newline is important
        
