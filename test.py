from traceback_center import TracebackCenter
import sys
sys.excepthook = TracebackCenter.get_traceback
try:
	print(sys.argv[1])
except:
	pass
print(sys.argv[2])
# print(dir(sys))
# print("-"*100)
# TracebackCenter.get_traceback()
# try:
# 	print("sys.last_traceback =", sys.exc_traceback)
# except:
# 	pass
# try:
# 	print("sys.last_value     =", sys.exc_value)
# except:
# 	pass
# try:
# 	print("sys.last_type      =", sys.exc_type)
# except:
# 	pass