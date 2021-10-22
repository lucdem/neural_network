from typing import List


def matrix_sum(m1, m2):
	__m_check_size(m1, m2)
	res = [None] * len(m1)
	for i in range(len(m1)):
		row = [None] * len(m1[0])
		for k in range(len(m1[0])):
			row[k] = m1[i][k] + m2[i][k]
		res[i] = row
	return res


def __m_check_size(m1, m2):
	if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
		raise Exception("Vectors have different lenghts")


def __vec_check_size(vec1, vec2):
	if len(vec1) != len(vec2):
		raise Exception("Vectors have different lenghts")


def vec_sum(vec1, vec2) -> List[float]:
	__vec_check_size(vec1, vec2)
	size = len(vec1)
	results = [0.0] * size
	for i in range(size):
		results[i] = vec1[i] + vec2[i]
	return results


def vec_element_wise_multiplication(vec1, vec2) -> List[float]:
	__vec_check_size(vec1, vec2)
	size = len(vec1)
	results = [0.0] * size
	for i in range(size):
		results[i] = vec1[i] * vec2[i]
	return results
