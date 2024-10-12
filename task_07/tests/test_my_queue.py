from my_queue import MyQueue


def test_my_queue():
    q = MyQueue[int]()
    q.push(1)
    q.push(2)
    q.push(3)
    assert q.pop() == 1
    q.push(4)
    assert q.pop() == 2
    assert q.pop() == 3
    q.push(5)
    assert q.pop() == 4
    assert q.peek() == 5
    assert not q.is_empty()
    assert q.pop() == 5
    assert q.is_empty()
