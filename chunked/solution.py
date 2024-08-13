from typing import Iterator, Iterable


def chunked_list(iterable: Iterable, chunk_size: int) -> Iterator[list]:
    for i in range(0, len(iterable), chunk_size):
        chunk = iterable[i:i+chunk_size]
        yield chunk


list_to_chunk, size = [1, 2, 3, 4], 2
result = list(chunked_list(iterable=list_to_chunk, chunk_size=size))
assert result == [[1, 2], [3, 4]]

list_to_chunk, size = [1, 2, 3, 4, 5], 2
result = list(chunked_list(iterable=list_to_chunk, chunk_size=size))
assert result == [[1, 2], [3, 4], [5]]

list_to_chunk, size = [1, 2, 3, 4], 3
result = list(chunked_list(iterable=list_to_chunk, chunk_size=size))
assert result == [[1, 2, 3], [4]]

list_to_chunk, size = [1, 2, 3, 4], 1
result = list(chunked_list(iterable=list_to_chunk, chunk_size=size))
assert result == [[1], [2], [3], [4]]

list_to_chunk, size = [], 1
result = list(chunked_list(iterable=list_to_chunk, chunk_size=size))
assert result == []
