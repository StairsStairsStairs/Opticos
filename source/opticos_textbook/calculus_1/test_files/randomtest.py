import sys
import math
print('math' in sys.modules)
#del sys.modules["math"]
del math
print(math.cos(2))
print("e")
print('math' in sys.modules)