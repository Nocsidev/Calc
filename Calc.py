from sympy import *

init_printing()

Functia = input("Functia: ")
Legatura = input("Legatura: ")
DifDe0 = input("Diferite De 0? ")

def PrintDerivat(Var, Derivat):
    print("Derivat cu", Var + ":", end = " ")
    pprint(Derivat, use_unicode=False)

x, y, z = symbols('x,y,z')
Functia = sympify(Functia)
PctMinim, PctMaxim = False, False

f_x = diff(Functia, x)
f_y = diff(Functia, y)
f_z = diff(Functia, z)
PrintDerivat("x", f_x)
PrintDerivat("y", f_y)

Ec1 = Eq(f_x, 0)
Ec2 = Eq(f_y, 0)
Ec3 = Eq(f_z, 0)

FilteredPctStat = []
if not DifDe0:
    if f_z != 0:
        PrintDerivat("z", f_z)
        PctStat = solve((Ec1, Ec2, Ec3), (x, y, z))      
        for i in range(len(PctStat)):
            FilteredPctStat.append((PctStat[x], PctStat[y], PctStat[z]))  
    else:
        PctStat = solve((Ec1, Ec2), (x, y))
        for i in range(len(PctStat)):
            FilteredPctStat.append((PctStat[x], PctStat[y]))
else:
    if f_z != 0:
        PctStat = [sol for sol in solve((Ec1, Ec2, Ec3), (x, y, z)) if sol[0] != 0 and sol[1] != 0 and sol[2] != 0]
        for sol in PctStat:
            if all(val.is_rational or val.evalf().is_real for val in sol):
                FilteredPctStat.append(sol)
    else:
        PctStat = [sol for sol in solve((Ec1, Ec2), (x, y)) if sol[0] != 0 and sol[1] != 0]
        for sol in PctStat:
            if all(val.is_rational or val.evalf().is_real for val in sol):
                FilteredPctStat.append(sol)


PctStat = FilteredPctStat

print("Puncte Stationare:", end= " ")
pprint(PctStat)

f_xx = diff(f_x, x)
f_yy = diff(f_y, y)
f_zz = diff(f_z, z)
f_xy = diff(f_x, y)
f_yz = diff(f_y, z)
f_zx = diff(f_z, x)
PrintDerivat("xx", f_xx)
PrintDerivat("yy", f_yy)
PrintDerivat("xy", f_xy)

if not Legatura:
    Hessiana = Matrix([[f_xx, f_xy], [f_xy, f_yy]])
    #print(Hessiana)
    #print(Hessiana.subs(PctStat)) #Inlocuieste x si y cu punctele stationare

    for i in range(len(PctStat)):
        H1 = f_xx.subs({x: PctStat[i][0], y: PctStat[i][1]})

        if f_z != 0: #Daca avem Z
            PrintDerivat("zz", f_zz)
            PrintDerivat("zx", f_zx)
            PrintDerivat("zy", f_yz)

            H1 = f_xx.subs({x: PctStat[i][0], y: PctStat[i][1], z: PctStat[i][2]})
            H2 = Matrix([[Hessiana[0, 0], Hessiana[0, 1]], [Hessiana[1, 0], Hessiana[1, 1]]]).subs({x: PctStat[i][0], y: PctStat[i][1], z: PctStat[i][2]}).det()
            H3 = Hessiana.subs({x: PctStat[i][0], y: PctStat[i][1], z: PctStat[i][2]}).det()
            print("H3=", end=" ")
            pprint(H3)
            if H1 > 0 and H2 > 0 and H3 > 0:
                PctMinim = PctStat[i]
            elif H1 < 0 and H2 > 0 and H3 < 0:
                PctMaxim = PctStat[i]
        else:
            H2 = Matrix([[Hessiana[0, 0], Hessiana[0, 1]], [Hessiana[1, 0], Hessiana[1, 1]]]).subs({x: PctStat[i][0], y: PctStat[i][1]}).det()           
            if H1.is_positive and H2.is_positive:
                PctMinim = PctStat[i]
            elif H1.is_negative and H2.is_positive:
                PctMaxim = PctStat[i]

        print("H1 =", end=" ")
        pprint(H1)
        print("H2 =", end=" ")
        pprint(H2)

    if PctMinim:
        print("Punct de Minim:", end=" ")
        pprint(PctMinim)
        print("fmin =", end=" ")
        if f_z != 0: #Daca avem Z
            pprint(Functia.subs({x: PctMinim[0], y: PctMinim[1], z: PctMinim[2]}))
        else:
            pprint(Functia.subs({x: PctMinim[0], y: PctMinim[1]}))
    if PctMaxim:
        print("Punct de Maxim:", end=" ")
        pprint(PctMaxim)
        print("fmax =", end=" ")
        if f_z != 0: #Daca avem Z
            pprint(Functia.subs({x: PctMaxim[0], y: PctMaxim[1], z: PctMaxim[2]}))
        else:
            pprint(Functia.subs({x: PctMaxim[0], y: PctMaxim[1]}))



input()
