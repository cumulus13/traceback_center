import inspect

class test1():
	def test_01(self):
		print("TEST 01")
		print("FILE =", __file__)
		print dir(inspect.stack()[1])
		stack = inspect.stack()[1]
		print stack
		# print inspect.getsourcefile(stack)