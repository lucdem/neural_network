from typing import Iterator, Tuple, List, TypeVar


__T = TypeVar('__T')


def reverse_list_enumerate(l: List[__T]) -> Iterator[Tuple[int, __T]]:
	size = len(l)
	for i in range(-1, -(size + 1), -1):
		yield i, l[i]