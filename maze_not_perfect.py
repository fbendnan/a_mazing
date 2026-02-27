import random
class Cell:
    def __init__(self ,row,col):
        self.wall = [1,1,1,1] # Top, Right, Bottom, Left
        self.visit = False
        self.pos = (row,col)
        self.is_42 = False


start = (0,0)
stack = []
arr = []
grid = []
# def ft_show(grid):
#     for x in grid:
#         for arr in x:
#             if arr.wall[0] == 1:
#                 print("-----",end="")
#             else:
#                 print("     ", end="")
#         print()
#         for arr in x:
#             left  = "|" if arr.wall[3] == 1 else " "
#             right = "|" if arr.wall[1] == 1 else " "
#             print(left + "   " + right, end="")
#             # print("|  " if arr.wall[3] == 1 else "   ", end="")
#             # print("  |" if arr.wall[1] == 1 else "   ", end="")
#         print()
#         for arr in x:
#             if arr.wall[2] == 1:
#                 print("_____",end="")
#             else:
#                 print("     ",end="")
#         print()
def ft_show(grid):
    for x in grid:
        # 1. Print TOP walls of the row
        for arr in x:
            # Use + for corners to make it line up
            top = "-----" if arr.wall[0] == 1 else "     "
            print(f"+{top}", end="")
        print("+") # End of top line

        # 2. Print LEFT walls and CONTENT
        for arr in x:
            left = "|" if arr.wall[3] == 1 else " "
            content = " 42 " if arr.is_42 else "    "
            print(f"{left}{content}", end="")
        print("|") # End of middle line

    # 3. Print the very bottom border of the whole maze
    for arr in grid[-1]:
        print("+-----", end="")
    print("+")

def remove_current_wall(row , col , new_row ,new_col,grid):
    if row > new_row:
        grid[row][col].wall[0] = 0
        grid[new_row][new_col].wall[2] = 0
       
    elif row < new_row:
        grid[row][col].wall[2] = 0
        grid[new_row][new_col].wall[0] = 0
      

    elif new_col > col:
        grid[row][col].wall[1] = 0
        grid[new_row][new_col].wall[3] = 0
        
    elif new_col < col:
        grid[row][col].wall[3] = 0
        grid[new_row][new_col].wall[1] = 0
    return 1


def visited_befor_42(grid,width,heigh):
    pattern_42 = [
        [1,0,0,0,1,1,1],
        [1,0,1,0,0,0,1],
        [1,1,1,0,1,1,1],
        [0,0,1,0,1,0,0],
        [0,0,1,0,1,1,1]
    ]
    pattern_rows = len(pattern_42)
    pattern_cols  = len(pattern_42[0])
    start_row = (heigh - pattern_rows) // 2
    start_col = (width - pattern_cols) // 2
    if pattern_rows > heigh or pattern_cols > width:
        print("Pattern too big for the grid!")
        return
    for x in range(pattern_rows):
        for y in range(pattern_cols):
            if pattern_42[x][y] == 1:
                grid[start_row + x][start_col +y].visit = True
                grid[start_row + x][start_col + y].is_42 = True
                # grid[start_row + x][start_col + y].wall = [0,0,0,0]
          
    
def ft_algo(grid,width,heigh):
    global stack
    for i in grid:
        for j in i:
            if j.pos == start:
                j.visit = True
                stack = [j.pos]

    while stack:
        row, col = stack[-1]
        list = [(row+1,col),(row-1,col),(row,col+1),(row,col-1)]
        
        random.shuffle(list)
            
        check = 0
        for neighbor in list:
            new_row, new_col = neighbor 
            if 0 <= new_row < heigh and 0 <= new_col < width:
                if grid[new_row][new_col].visit == False:
                    grid[new_row][new_col].visit = True
                    stack.append((new_row,new_col))
                    check += remove_current_wall(row,col,new_row,new_col,grid)
                    break
                elif random.random() < 0.1 and not grid[new_row][new_col].is_42: 
                    remove_current_wall(row, col, new_row, new_col, grid)
                    
        if check == 0:
            stack.pop()         


def main():
    width = 10
    heigh = 10
    for i in range(width):
        arr = []
        for j in range(heigh):
            arr.append(Cell(i,j))
        grid.append(arr)  
    
    visited_befor_42(grid, width,heigh)     
    ft_algo(grid,width,heigh)
    ft_show(grid)           
main()


# import random
# class Cell:
#     def __init__(self ,row,col):
#         #
#         self.wall = [1,1,1,1] 
#         self.visit = False
#         self.pos = (row,col)

# width = 15
# heigh = 15  
# start = (0,0)
# stack = []
# arr = []
# grid = []
# def ft_show(grid):
#     for x in grid:
#         for arr in x:
#             if arr.wall[0] == 1:
#                 print("-----",end="")
#             else:
#                 print("     ", end="")
#         print()
#         for arr in x:
#             if arr.wall[3] == 1:
#                 print("|  ",end ="")
#             else:
#                 print("   ",end="")
#             if arr.wall[1] == 1:
#                 print("  |",end ="")
#             else:
#                 print("   ",end="")             
#         print()
#         for arr in x:
#             if arr.wall[2] == 1:
#                 print("_____",end="")
#             else:
#                 print("     ",end="")
#         print()
#     # generate_maze(grid)
       


# def remove_current_wall(row , col , new_row ,new_col,grid):
#     if row > new_row:
#         grid[row][col].wall[0] = 0
#         grid[new_row][new_col].wall[2] = 0
       
#     elif row < new_row:
#         grid[row][col].wall[2] = 0
#         grid[new_row][new_col].wall[0] = 0
      
#     elif new_col > col:
#         grid[row][col].wall[1] = 0
#         grid[new_row][new_col].wall[3] = 0
        
#     elif new_col < col:
#         grid[row][col].wall[3] = 0
#         grid[new_row][new_col].wall[1] = 0
#     return 1
# def ft_algo(grid):
#     global stack
#     for i in grid:
#         for j in i:
#             if j.pos == start:
#                 j.visit = True
#                 stack = [j.pos]

#     while stack:
#         row, col = stack[-1]
#         list = [(row+1,col),(row-1,col),(row,col+1),(row,col-1)]
        
#         random.shuffle(list)
            
#         check = 0
#         for neighbor in list:
#             new_row,new_col = neighbor 
#             if 0 <= new_row < heigh and 0 <= new_col < width:
#                 if grid[new_row][new_col].visit == False:
#                     grid[new_row][new_col].visit = True
#                     stack.append((new_row,new_col))
#                     check = remove_current_wall(row,col,new_row,new_col,grid)
#                     break

#         if check == 0:
#             stack.pop()  

#     ft_show(grid)          


# def main():
#     for i in range(width):
#         arr = []
#         for j in range(heigh):
#             arr.append(Cell(i,j))
#         grid.append(arr)
#     # print(grid)       
#     ft_algo(grid)        
# main()
# def create_grid():
#     grid = []
#     for i in range(width):
#         row = []
#         for j in range(heigh):
#             row.append(Cell(i,j))
#         grid.append(row)
#     return grid

# def generate_maze():
#     grid = create_grid()      
#     ft_algo(grid)          

#     cell = []
#     for x in range(width):
#         row = []
#         for y in range(heigh):
#             row.append(grid[x][y].wall)
#         cell.append(row)

#     return cell
# if __name__ == "__main__":
#     main()


    
