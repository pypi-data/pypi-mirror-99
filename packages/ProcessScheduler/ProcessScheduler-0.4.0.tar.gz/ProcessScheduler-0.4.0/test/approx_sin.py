from math import sin, factorial

x = 2.5
print("Exact sin x:", sin(x))

def approx_sin(x):
	a_s = x - x ** 3 / (factorial(3)) + x ** 5 / factorial(5)
	return a_s

print("Approx sin:", approx_sin((x)))