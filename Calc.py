from sympy import *

init_printing()

Functia = input("Functia: ")
Legatura = input("Legatura: ")
DifDe0 = input("Diferite De 0? ")
MaiMareCa0 = input("Mai mare ca 0? ")

def PrintDerivat(Var, Derivat):
    print("Derivat cu", Var + ":", end = " ")
    pprint(Derivat, use_unicode=False)


x, y, z, lam = symbols('x,y,z, lambda')
Functia = sympify(Functia)
Legatura = sympify(Legatura)
PctMinim, PctMaxim = False, False

if not Legatura:
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
else:

    dx, dy, dz = symbols("dx, dy, dz")

    L = Functia + lam * Legatura
    L_x = diff(L, x)
    L_y = diff(L, y)
    L_z = diff(L, z)
    L_lam = diff(L, lam)

    FilteredPctStat = []  
    SistemEc = [L_x, L_y, L_z, L_lam] if 'z' in str(L) else [L_x, L_y, L_lam]
    pprint(SistemEc)

    if not MaiMareCa0 and not DifDe0:
        PctStat = solve(SistemEc, (x, y, z, lam) if 'z' in str(L) else (x, y, lam))
        if isinstance(PctStat, dict):
            FilteredPctStat.append(PctStat)
        elif isinstance(PctStat, list):
            for sol in PctStat:
                if len(sol) == 3:
                    FilteredPctStat.append({x: sol[0], y: sol[1], lam: sol[2]})
                else:
                    FilteredPctStat.append({x: sol[0], y: sol[1], z: sol[2], lam: sol[3]})            
    elif MaiMareCa0:
        PctStat = solve(SistemEc, (x, y, z, lam) if 'z' in str(L) else (x, y, lam))
        if isinstance(PctStat, dict):
            FilteredPctStat.append(PctStat)
        elif isinstance(PctStat, list):
            for sol in PctStat:

                if len(sol) == 3:
                    if sol[0].is_real and sol[0] > 0 and sol[1].is_real and sol[1] > 0:
                        FilteredPctStat.append({x: sol[0], y: sol[1], lam: sol[2]})
                else:
                    if sol[0].is_real and sol[0] > 0 and sol[1].is_real and sol[1] > 0 and sol[2].is_real and sol[2] > 0:
                        FilteredPctStat.append({x: sol[0], y: sol[1], z: sol[2], lam: sol[3]}) 
    else:
        PctStat = solve(SistemEc, (x, y, z, lam) if 'z' in str(L) else (x, y, lam))
        if isinstance(PctStat, dict):
            FilteredPctStat.append(PctStat)
        elif isinstance(PctStat, list):
            for sol in PctStat:

                if len(sol) == 3:
                    if sol[0].is_real and sol[0] != 0 and sol[1].is_real and sol[1] != 0:
                        FilteredPctStat.append({x: sol[0], y: sol[1], lam: sol[2]})
                else:
                    if sol[0].is_real and sol[0] != 0 and sol[1].is_real and sol[1] != 0 and sol[2].is_real and sol[2] != 0:
                        FilteredPctStat.append({x: sol[0], y: sol[1], z: sol[2], lam: sol[3]}) 

    PctStat = FilteredPctStat
    print("Puncte Stationare:", end=" ")
    pprint(PctStat)

    L_xx = diff(L_x, x)
    L_yy = diff(L_y, y)
    L_zz = diff(L_z, z)
    L_xy = diff(L_x, y)
    L_xz = diff(L_x, z)
    L_yz = diff(L_y, z)

    d2L = sympify(L_xx * dx**2 + L_yy * dy**2 + L_zz * dz**2 + 2 * L_xy * dx*dy + 2 * L_yz * dy*dz + 2 * L_xz * dx*dz)
    print("Diferentiala de ord 2:", end=" ")
    print(d2L)

    Hessiana = Matrix([[L_xx, L_xy, L_xz], [L_xy, L_yy, L_yz], [L_xz, L_yz, L_zz]]) if 'z' in str(L) else Matrix([[L_xx, L_xy], [L_xy, L_yy]])
    for i, SetPctStat in enumerate(PctStat):
        print(i, SetPctStat)

        #Rez = d2L.subs({x: SetPctStat[0], y: SetPctStat[1], z: SetPctStat[2]}) if 'z' in str(L) else d2L.subs({x: SetPctStat[0], y: SetPctStat[1]})
        Rez = d2L.subs(SetPctStat)
        print(Rez)

        H_at_sol = Hessiana.subs(SetPctStat)
        #print("Hessiana la punctul critic:")
        #pprint(H_at_sol)

        eigenvalues = H_at_sol.eigenvals()
        eigen_signs = [val.is_positive for val in eigenvalues]

        # Clasificarea punctului
        if all(eigen_signs):  # Toate valorile proprii pozitive
            print("Punct de Minim:", SetPctStat)
            print("fmin =", end=" ")
            print(Functia.subs(SetPctStat))
        elif all(not sign for sign in eigen_signs):  # Toate valorile proprii negative
            print("Punct de Maxim:", SetPctStat)
            print("fmax =", end=" ")
            print(Functia.subs(SetPctStat))
        else:  # Valorile proprii mixte
            pprint("NU PUTEM DETERMINA")
            g_x = diff(Legatura, x)
            g_y = diff(Legatura, y)
            g_z = diff(Legatura, z)
            d1g = sympify(g_x * dx + g_y * dy + g_z * dz)
            print("Diferentiala de ord 1 pt Legatura:", end=" ")
            print(d1g)
            Rez = d1g.subs(SetPctStat)
            DxScrisCaDy = solve(Rez, dx)[0]
            print("Dx scris ca si dy:", DxScrisCaDy)



input()
