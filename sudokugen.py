import random
import sys
from sudoku import Sudoku
from sudoku_render import drawsudokuv2

def gensudoku(width,height,diff=0.5):
    print("generating a seed")
    seed=random.randrange(sys.maxsize)
    print(f"seed:{seed}")
    print("making the puzzle...")
    puzzle = Sudoku(width,height,seed=seed,difficulty=diff)
    print(f"Does the puzzle have multiple solutions? {puzzle.has_multiple_solutions()}")
    if puzzle.has_multiple_solutions():
        while puzzle.has_multiple_solutions():
            print("generating a seed")
            seed=random.randrange(sys.maxsize)
            print(f"seed:{seed}")
            diff=random.randint(10,99)/100
            print(f"difficulty:{diff}")
            print("making the puzzle...")
            puzzle = Sudoku(width,height,seed=seed,difficulty=diff)
            print(f"Does the puzzle have multiple solutions? {puzzle.has_multiple_solutions()}")
    print("done (probably)")
    print("rendering the puzzle...")
    sudoku_img = drawsudokuv2(width=puzzle.width, height=puzzle.height,board=puzzle.board)
    print("saving the puzzle...")
    sudoku_img.save(f"sudokus/sudoku_{puzzle.width}x{puzzle.height}_{diff}_{seed}.png")
    print("done")
    print("solving the puzzle")
    solved_puzzle=puzzle.solve(assert_solvable=True)
    print("done")
    print("rendering the solved puzzle")
    solved_sudoku_img = drawsudokuv2(width=solved_puzzle.width,height=solved_puzzle.height,board=puzzle.board,user_board=solved_puzzle.board)
    print("saving the solved puzzle...")
    solved_sudoku_img.save(f"sudokus/solved_sudoku_{puzzle.width}x{puzzle.height}_{diff}_{seed}.png")
    print("done")
    return f"sudokus/sudoku_{puzzle.width}x{puzzle.height}_{diff}_{seed}.png",f"sudokus/solved_sudoku_{puzzle.width}x{puzzle.height}_{diff}_{seed}.png"
#    print("showing the unsolved puzzle")
#    sudoku_img.show()