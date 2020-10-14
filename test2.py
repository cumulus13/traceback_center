import test1
import inspect
c = test1.test1()
c.test_01()

def test2():
	print inspect.stack()[1]

test2()