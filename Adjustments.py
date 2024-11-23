import numpy as np

XValues = np.array(list(map(float, input("Valori X: ").split(','))))
YValues = np.array(list(map(float, input("Valori Y: ").split(','))))

s0 = len(XValues)
s1 = np.sum(XValues)
s2 = np.sum(XValues**2)
s3 = np.sum(XValues**3)
s4 = np.sum(XValues**4)

t0 = np.sum(YValues)
t1 = np.sum(XValues * YValues)
t2 = np.sum(XValues**2 * YValues)

print("s:", s0, s1, s2, s3, s4)
print("t:", t0, t1, t2)


## Calculare dreapta
SistemEc1 = np.array([[s0, s1], [s1, s2]])
SistemEc2 = np.array([t0, t1])
a0, a1 = np.linalg.solve(SistemEc1, SistemEc2)
print(f"a0 = {a0:.5f}")
print(f"a1 = {a1:.5f}")
print("Dreapta: y =", f"{a0:.5f}", "+", f"{a1:.5f}" + "x")
print()


## Calculare Parabola
MDelta = np.matrix([[s0, s1, s2], [s1, s2, s3], [s2, s3, s4]])
Ma = [
    np.matrix([[t0, s1, s2], [t1, s2, s3], [t2, s3, s4]]),  #Ma0
    np.matrix([[s0, t0, s2], [s1, t1, s3], [s2, t2, s4]]),  #Ma1
    np.matrix([[s0, s1, t0], [s1, s2, t1], [s2, s3, t2]])   #Ma2
]

Delta = round(np.linalg.det(MDelta), 3)
print("Delta =", Delta)
for i in range(3):
    print(Ma[i])
    np.printoptions
    Ma[i] = round(np.linalg.det(Ma[i]), 3)
    print("Delta a" + str(i) + " =", Ma[i])

for i in range(3):
    Ma[i] = np.divide(Ma[i], Delta)
    print("a" + str(i) + " =", Ma[i])

print("Parabola: y =", str(Ma[0]), "+", str(round(Ma[1], 3)) + "x", "+", str(round(Ma[2], 3)) + "x^2")
