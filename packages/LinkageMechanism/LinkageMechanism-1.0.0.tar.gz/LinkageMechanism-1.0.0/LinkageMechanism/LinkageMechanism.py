#!/usr/bin/env python
# coding: utf-8

from sympy import *
init_printing(use_latex='mathjax')

a,b,c,d,e,f,g,h,x,y,x,z,u,w,k,t = symbols('a b c d e f g h x y x z u w k .')
α,β,γ,δ,θ,φ = symbols('alpha beta gamma delta theta varphi')
θ1,θ2,θ3 = symbols('theta_1 theta_2 theta_3')
x1,x2,y1,y2,z1,z2 = symbols('x_1 x_2 y_1 y_2 z_1 z_2')

def MecSolve_OneDOF(Cg,Eq):      # Cg,Eq Coords generalizados e Eq Restrição
    Eq = Matrix(Eq)
    Cs = [ i for i in Cg[1:] ]   # Lista com as coords secundárias
    J = Eq.jacobian(Cs)          # Jacobiano do sistema
    F = Eq.jacobian([Cg[0]])     # Obtenção da matriz F
    K = simplify(-(J**-1)*F)     # Obtenção da matriz K
    Ks = Matrix([ k**i for i in Cg[1:] ])
    L = simplify( K.jacobian([Cg[0]]) + K.jacobian(Cs)*Ks )
    return(F, J, K, L)

def MecSolve_MultDOF(Cg,Eq):    # Cg,Vg Coords e Veloc Generalizadas
    f = len(Cg)-len(Eq)
    Eq = Matrix(Eq)
    J = Eq.jacobian(Cg[f:])     # Jacobiano do sistema
    F = Eq.jacobian([Cg[:f]])   # Obtenção da matriz F
    K = simplify(-(J**-1)*F)    # Obtenção da matriz K

    L = Matrix([])
    Tg = [ i**t for i in Cg ]
    for i in range(f):          # Obtenção da matriz L
        Lprov = K.col(i).jacobian(Cg[:f])*Matrix(Tg[:f]) + K.col(i).jacobian(Cg[f:])*Matrix(Tg[f:])
        L = L.row_join(Lprov)
    return(F, J, K, L)