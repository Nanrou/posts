def find_min_in_rorate(lst):
    if len(lst) > 1:
        start, end = 0, len(lst) - 1
        while lst[start] >= lst[end]:
            if end - start == 1:
                return lst[end]
            mid = (start + end) // 2
            if lst[mid] > lst[start]:
                start = mid
            else:
                end = mid
        return lst[start]
    else:
        return lst


from queue import LifoQueue
from itertools import product


def find_path_in_matrix(matrix, strings):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def mark(m, pos):
        m[pos[0]][pos[1]] = None

    def passbile(m, pos, char):
        return m[pos[0]][pos[1]] is char

    stack = LifoQueue()

    if len(strings) <= 0:
        raise RuntimeError

    for row, col in product(range(len(matrix)), range(len(matrix[0]))):
        if matrix[row][col] == strings[0]:
            origin = (row, col)
            break
    else:
        raise RuntimeError('cant find the origin')

    stack.put((origin, 0, 0))

    while not stack.empty():
        _pos, _nxt, _index = stack.get()
        for i in range(_nxt, len(dirs)):
            nextp = (_pos[0] + dirs[i][0], _pos[1] + dirs[i][1])
            if -1 < nextp[0] < len(matrix) and -1 < nextp[1] < len(matrix[0]):
                if _index == len(strings) - 2 and matrix[nextp[0]][nextp[1]] == strings[_index + 1]:
                    stack.put((_pos, 0, _index))  # 当前位置已经不在栈中了
                    stack.put((nextp, 0, _index + 1))
                    return stack.queue  # 栈中保存着路径
                if passbile(matrix, nextp, strings[_index + 1]):
                    stack.put((_pos, i + 1, _index))
                    mark(matrix, nextp)
                    stack.put((nextp, 0, _index + 1))
                    break
    return False
 
 
def robot_move_range(rows, cols, k):
    """
    mm = [['a', 'b', 't', 'g'], ['c', 'f', 'c', 's'], ['j', 'd', 'e', 'h']]
    ss = 'bfce'
    print(find_path_in_matrix(mm, ss))
    """
    if rows <= 0 or cols <= 0 or k < 0:
        raise RuntimeError
        
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    def check(row, col):
        _sum = 0
        for i in [row, col]:
            while i > 0:
                _sum += i % 10
                i //= 10
        if _sum > k:
            return False
        return True

    def passbile(row, col, visited_lst):
        if -1 < row < rows and -1 < col < cols and check(row, col) and visited[row, col] is None:
            return True               
        return False
        
    def move_core(row, col, visited_lst):
        _count = 0
        if passible(row, col, visited_lst):
            visited_lst[row * cols + col] = True
            _count = 1 + sum([move_core(row + dirs[i][0], col + dirs[i][1], visited_lst) for i in range(4)])
        return _count
        
    visited = []
    for _ in range(rows * cols):
        visited.append(False)
    
    count = move_core(0, 0, visited)
    
    return count
        
def sort_odd_and_even(lst):
    i, j = 0, len(lst) - 1
    while i < j:
        while i < j and lst[j] & 0b1 == 0:
            j -= 1
        while i < j and lst[i] & 0b1 != 0:
            i += 1
        if i < j:
            lst[i], lst[j] = lst[j], lst[i]

def conclude_even(ele):
    if ele & 0b1 == 0:
        return True
    return False

            
def sort_by_some_rule(lst, func):
    i, j = 0, len(lst) - 1
    while i < j:
        while i < j and func(lst[j]):
            j -= 1
        while i < j and not func(lst[i]):
            i += 1
        if i < j:
            lst[i], lst[j] = lst[j], lst[i]

if __name__ == '__main__':
    ll = [i for i in range(10)]
    sort_by_some_rule(ll, conclude_even)
    print(ll)
    
