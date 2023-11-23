def make_board():
    board = [[["-"]*3 for _ in range(3)] for _ in range(9)]
    return board

def print_board(board):
    n = 0
    for _ in range(3):
        print("-"*21)
        for i in range(3):
            for j in range(3):
                print("|",end="")
                for k in range(3):
                    if k == 2:
                        print(f"{board[j+n][i][k]}",end="")
                    else:
                        print(f"{board[j+n][i][k]} ",end="")
                print(f"|",end="")
            print()
        n += 3
    print("-"*21)

def take_line_element():
    position = int(input("choose tile (1-9): "))
    while position not in range(1,10):
        print("invalid tile")
        position = int(input("choose tile (1-9): "))
    line = (position-1)//3
    if line==-1:line=0
    
    if position in [1,4,7]: element=0
    elif position in [2,5,8]: element=1
    else: element = 2
    next_board = position-1
    return line, element, next_board

def take_mini():
    mini = int(input("choose small board (1-9): "))
    while (mini not in range(1,10)) or (board_won[mini]==(True,"X")) or\
        (board_won[mini]==(True,"O")) or (board_won[mini]=="Tie"):
        print("invalid board")
        mini = int(input("choose small board (1-9): "))
    return mini

def initial_turn():
    mini = take_mini()-1
    line, element, next_board = take_line_element()

    while board[mini][line][element] != "-":
        print("invalid tile")
        line, element, next_board = take_line_element()
    
    board[mini][line][element] = "X"
    return next_board

def turn_w_mini(turn):
    mini = take_mini()-1
    line, element, next_board = take_line_element()
    while board[mini][line][element] != "-":
        print("invalid tile")
        line, element, next_board = take_line_element()
    if turn=="X":
        board[mini][line][element] = "X"
    else:
        board[mini][line][element] = "O"
    return next_board

def turn_n_mini(mini, turn):
    line, element, next_board = take_line_element()
    
    while board[mini][line][element] != "-":
        print("invalid tile")
        line, element, next_board = take_line_element()
    
    if turn=="X":
        board[mini][line][element] = "X"
    else:
        board[mini][line][element] = "O"
    return next_board

def check_mini(turn):
    X_won = [["\\"," ","/"],[" ","X"," "],["/"," ","\\"]]
    O_won = [[" ","_"," "],["/"," ","\\"],["\\","_","/"]]
    tie = [[" "," "," "],["t","i","e"],[" "," "," "]]
    for num,mini in enumerate(board):
        columns = [[mini[i][j] for i in range(3)] for j in range(3)]
        diagonals = [[mini[i][j] for i,j in enumerate(range(3))],\
            [mini[i][j] for i,j in enumerate(range(2,-1,-1))]]
        total_combinations = mini+columns+diagonals
        for combination in total_combinations:
            if (len(set(combination)) == 1 and combination[1] != "-"):
                board_won[num+1] = (True,turn)
        if mini==X_won:
            board_won[num+1] = (True,"X")
        elif mini==O_won:
            board_won[num+1] = (True,"O")
        elif "-" not in mini[0] and "-" not in mini[1] and\
            "-" not in mini[2] and mini != X_won and mini != O_won:
            board_won[num+1] = "Tie"
            
    for i in board_won.keys():
        if board_won[i]!=False:
            if board_won[i][1]=="X":
                board[i-1] = X_won
            elif board_won[i][1]=="O":
                board[i-1] = O_won
            elif board_won[i]=="Tie":
                board[i-1] = tie

def check_board():
    global board_won, game_over, game_final
    board = [mini for mini in board_won.values()]
    board = [[board[i+j] for i in range(3)] for j in range(0,7,3)]
    columns = [[board[i][j] for i in range(3)] for j in range(3)]
    diagonals = [[board[i][j] for i,j in enumerate(range(3))],\
        [board[i][j] for i,j in enumerate(range(2,-1,-1))]]
    total_combinations = board+columns+diagonals
    for combination in total_combinations:
        if len(set(combination)) == 1 and combination[1]!=False and combination[1]!="Tie":
            print(f"{combination[1][1]} won the game")
            game_over = True
            if combination[1][1]=="X": game_final=1
            else: game_final=-1
            return game_over
    c = 0
    for mini in board_won.values():
        if mini != False: c+=1
    if c == 9:
        print(f"it's a tie")
        game_over = True
        game_final = 0
        return game_over
    return False

def play(next_board, turn):
    global board_won, board, game_over
    print(f"turn: {turn}")
    if board_won[next_board+1]!=False:
        check_mini(turn)
        print_board(board)
        print(f"next board: any")
        next_board = turn_w_mini(turn)  
        check_mini(turn)  
    else:
        print_board(board)
        print(f"next board: {next_board+1}")
        next_board = turn_n_mini(next_board, turn)
        check_mini(turn)
        
    if turn == "X": turn = "O"
    else: turn = "X"
    
    return next_board, turn

def game():
    global board, game_over, board_won, game_final
    
    board = make_board()
    game_over = False
    board_won = {mini:False for mini in range(1,10)}
    game_final = ""

    print_board(board)
    turn = "X"
    print(f"turn:{turn}")
    next_board = initial_turn()
    print_board(board)
    print(f"next board: {next_board+1}")
    turn = "O"
    
    while game_over == False:
        game_over = check_board()
        if game_over==True:
            break
        next_board, turn = play(next_board, turn)
        print("")
        
    print_board(board)
    print("Game Over")
    return game_final

game_final = game()