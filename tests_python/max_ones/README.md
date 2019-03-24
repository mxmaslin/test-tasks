# Максимальный массив единиц

Дан массив из единиц и нулей. Нужно определить, какой максимальный по длине подинтервал
единиц можно получить, удалив один элемент массива.


```python
def max_ones(int_list):
    pass


if __name__ == '__main__':
    assert max_ones([0, 0]) == 0
    assert max_ones([1, 0]) == 1
    assert max_ones([1, 1]) == 2
    assert max_ones([1, 0, 1, 0]) == 2
    assert max_ones([0, 1, 0, 1]) == 2
    assert max_ones([1, 0, 0, 1, 0]) == 1
    assert max_ones([0, 1, 1, 0, 1]) == 3
    assert max_ones([1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]) == 6
    assert max_ones([0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]) == 1
    assert max_ones([1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1]) == 5
    assert max_ones([0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0]) == 2
```

[**Решение**](https://github.com/mxmaslin/Test-tasks/blob/master/tests_python/max_ones/max_ones.py 'Решение задачи о максимальном массиве единиц')