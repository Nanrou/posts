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
		
	
if __name__ == '__main__':
	mm = [['a', 'b', 't', 'g'], ['c', 'f', 'c', 's'], ['j', 'd', 'e', 'h']]
	ss = 'bfce'
	print(find_path_in_matrix(mm, ss))