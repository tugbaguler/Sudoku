import time

# create 2D integer array and define length of the initial sudoku table
N = 9
def initial_sudoku_table():
    initial_sudoku_board = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]

    for row in range(N):
        for column in range(N):
            # to create variable set in CSP
            var = Variable(row, column, initial_sudoku_board[row][column])
            initial_sudoku_board[row][column] = var

    return initial_sudoku_board

# Prints the sudoku on the screen in grid format at the beginning and after it is solved.
def print_sudoku_table(table):
    for row in range(N):
        if row in [N/3, N/3+3]:
            print("--------------------------")
        for column in range(N):
            if column in [N/3, N/3+3]:
                print(' | ', table[row][column].value, end=' ')
            else:
                print(table[row][column].value, end=' ')
        print(end='\n')

def is_valid_input(empty_variable, number, board):
    row_x_position = empty_variable.row
    column_y_position = empty_variable.col

    # control columns
    for column in range(N):
        if (column == column_y_position):
            continue
            # Using number for control the cell value
        if (board[row_x_position][column].value == number):
            return False

    # control rows
    for row in range(N):
        if (row == row_x_position):
            continue
        if (board[row][column_y_position].value == number):
            return False

    # control each 3*3 subsquare in the sudoku table
    box_x  = row_x_position / 3
    box_y = column_y_position / 3
    top_left_row = int(box_x) * 3
    top_left_col = int(box_y) * 3
    control_row = [top_left_row, top_left_row + 1, top_left_row + 2]
    control_column = [top_left_col, top_left_col + 1, top_left_col + 2]
    for r in control_row:
        for c in control_column:
            if (r == row_x_position and c == column_y_position):
                continue
            if (board[r][c].value == number):
                return False
    # If control_cell_value is valid input into board return True
    return True


# Recursive Backtracking Solver
def Backtracking_Search(csp):
    if csp.is_complete(csp.board):  # if assignment is complete
        return True  # return assignment

    empty_variable = csp.find_empty_areas(csp.board)
    if empty_variable == None:
        return False

    for domain_variable in empty_variable.domain:  # for each value in Order-Domain-Value(variable, assignment, csp) do
        valid = is_valid_input(empty_variable, domain_variable, csp.board)
        if valid:  # if value is consistent with assignment given Constraints[csp] then
            csp.board[empty_variable.row][empty_variable.col].value = domain_variable  # add {variable = value} to assignment

            # result = Recursive-backtracking(assignment, csp) / if result is not failure then
            if Backtracking_Search(csp):
                return True  # return result
            evaluate = Variable(empty_variable.row, empty_variable.col, 0)
            csp.board[empty_variable.row][empty_variable.col] = evaluate  # remove {variable = value} from assignment

    return False  # return FAILURE


# this is a class to represent csp
class CSP:
    def __init__(self, table):
        self.board = table

    # finds the next empty variable to be assigned in the table
    def find_empty_areas(self, table):
        for row in table:
            for variable in row:
                # represents zero empty spaces
                if variable.value == 0:
                    return variable

    # check if the table is solved
    def is_complete(self, table):
        for row in range(N):
            for column in range(N):
                # If there is zero in the table, sudoku has not been solved yet.
                if table[row][column].value == 0:
                    return False

                if (table, row, column) == False:
                    return False

        return True

# to define empty cells and which numbers can be selected for this empty cell
class Variable:
    # define constructor
    def __init__(self, row, col, value=0):
        self.value = value
        self.row = row
        self.col = col
        self.domain = self.initial_domain(value)

    # initializes domain of the variable
    # to find domains of empty cell
    def initial_domain(self, value):
        domain = []
        for i in range(1, 10):  # The domains that can take value are determined
            if i != value:
                domain.append(i)

        return domain


def main():
    # create a 2D lists of variables
    board = initial_sudoku_table()

    # create CPS instance to represent the board
    csp = CSP(board)

    start_time = time.time()

    # solution is boolean value. True when there's a solution.
    solution = Backtracking_Search(csp)

    print("\n Initial Sudoku Table")
    print_sudoku_table(initial_sudoku_table())

    print("\n Solution")
    if solution == True:
        print_sudoku_table(csp.board)
        print("\n Total time:  %s seconds" % (time.time() - start_time))
    else:
        print("Sudoku provided has no solution")
        print("\n Total time:  %s seconds" % (time.time() - start_time))

if __name__ == "__main__":
    main()