from typing import Iterator, Iterable


def chunked_list(iterable: Iterable, chunk_size: int) -> Iterator[list]:
    i = 0
    chunk = []
    while i < len(iterable):
        chunk = iterable[i:i+chunk_size]
        yield chunk
        i += chunk_size


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
