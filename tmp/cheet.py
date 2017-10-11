from queue import LifoQueue
from copy import deepcopy

def block(matrix, pos):
    i, j = pos
    for col in range(len(matrix)):  # 横向封锁
        if col == j:
            continue
        matrix[i][col] = 2
        if i+(col-j) >= 0 and i+(col-j) < len(matrix):  # 右斜线
            matrix[i+(col-j)][col] = 2

    for row in range(len(matrix)):  # 纵向封锁
        if row == i:
            continue
        matrix[row][j] = 2   
        if j-(row-i) >= 0 and j-(row-i) < len(matrix):  # 左斜线
            matrix[row][j-(row-i)] = 2
    return matrix


def queen(n=4):  # n == 1 or n > 3
    assert int(n) > 3 or int(n) == 1
    stack = LifoQueue()  # 在循环内还是外
    for col in range(n):
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        matrix[0][col] = 1
        block(matrix, (0, col))  
        stack.put((deepcopy(matrix), (0, col)))  # 将开始状态压入栈,连矩形也要压进去,回溯的时候只有坐标是没用的
        while not stack.empty():
            _matrix, pos = stack.get()           
            _matrix[pos[0]][pos[1]] = 1
            block(_matrix, pos)  # 标记空位
            
            for row in range(pos[0]+1, n+1):  # 判断之后的每一行
                if 0 in _matrix[row]:  # 如果有空位
                    for _col, ele in enumerate(_matrix[row]):
                        if ele == 0:
                            stack.put((deepcopy(_matrix), (row, _col)))  # 所有新位置入栈
                            
                    if row == n - 1:  # 最后一行了
                        print(_matrix)
                        return
                    break
                else:  # 没有空位就回溯
                    print('track back')
                    break
        else:
            print('flase')
            return
            

def queen_one(A, cur=0):  
    """
    基于深度优先搜索。
    一维数组中的元素A[i]代表的是第i行，第A[i]列。
    
    外层的循环是为了循环完该行的所有位置。
    内层的循环则是比较该行，与之前行的关系。
    
    理解好其核心是，一旦内层的判断通过，就会以此为起点，向下一行出发。（就是深度优先）
    结束的条件是到达最后一行，因为是先判断再到达，所以一旦到达，就说明最后一行是满足要求的。
    
    最后的输出就是满足条件的，八皇后的位置。
    """

    if cur==len(A):  
        print(A)  
    else:  
        for col in range(len(A)):  
            A[cur] = col #表示把第cur行的皇后放在col列上  
            for r in range(cur):  
                if A[r]==col or r-A[r]==cur-A[cur] or r+A[r]==cur+A[cur]:#判断是否跟前面的皇后冲突  
                    break  
            else:
                print('*'*10, 'end one loop', '*'*10)
                queen_one(A, cur+1)  

"""
举一反三：对于这种在可以利用二维数组来存储，但每行只用了一个位置的关系，都可以用一位数组来代替，来达到空间复杂度上的优化。
我最开始的做法是自己建立了一个栈来储存信息，而后面这个做法则是利用了程序的运行栈来保存信息。
前者并不是递归，后者是递归。
递归就是利用程序的运行栈的。

"""
                
                
    
if __name__ == '__main__':
    #matrix = [[0 for _ in range(4)] for _ in range(4)]
    #for line in block(matrix, (0, 0)):
    #    print(line)
    queen_one([None]*8)  