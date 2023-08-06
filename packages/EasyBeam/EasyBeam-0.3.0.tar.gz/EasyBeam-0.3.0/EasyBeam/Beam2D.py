import numpy as np

def ShapeMat(self, ξ, ell):
    return(np.array([[1-ξ,               0,              0, ξ,            0,              0],
                     [  0, 1-3*ξ**2+2*ξ**3, ξ*ell*(1-ξ)**2, 0, ξ**2*(3-2*ξ), ξ**2*ell*(ξ-1)]]))

def StrainDispMat(self, ξ, ell, zU, zL):
    BL = np.array([[-1/ell,                  0,               0, 1/ell,                   0,               0],
                   [     0, zL*(6-12*ξ)/ell**2,  zL*(4-6*ξ)/ell,     0, zL*(-6+12*ξ)/ell**2, zL*(-6*ξ+2)/ell]])
    BU = np.array([[-1/ell,                  0,               0, 1/ell,                   0,               0],
                   [     0, zU*(6-12*ξ)/ell**2,  zU*(4-6*ξ)/ell,     0, zU*(-6+12*ξ)/ell**2, zU*(-6*ξ+2)/ell]])
    return(BL, BU)

def StrainDispNablah(self, ξ, ell):
    BLNablah = np.array([[0,                0,            0, 0,                 0,             0],
                         [0, -1/2*(6-12*ξ)/ell**2, -1/2*(4-6*ξ)/ell, 0, -1/2*(-6+12*ξ)/ell**2, -1/2*(-6*ξ+2)/ell]])
    BUNablah = np.array([[0,               0,           0, 0,                0,            0],
                         [0, 1/2*(6-12*ξ)/ell**2, 1/2*(4-6*ξ)/ell, 0, 1/2*(-6+12*ξ)/ell**2, 1/2*(-6*ξ+2)/ell]])
    return(BLNablah, BUNablah)

def StiffMatElem(self, i):
    A = self.A[i]
    E = self.E[i]
    ell = self.ell[i]
    I = self.I[i]
    nu = self.nu[i]
    ϰ = self.ϰ[i]
    # bar (column) terms of stiffness matrix
    k = E*A/ell*np.array([[ 1, 0, 0, -1, 0, 0],
                          [ 0, 0, 0,  0, 0, 0],
                          [ 0, 0, 0,  0, 0, 0],
                          [-1, 0, 0,  1, 0, 0],
                          [ 0, 0, 0,  0, 0, 0],
                          [ 0, 0, 0,  0, 0, 0]], dtype=float)

    # Bending terms after Euler-Bernoulli
    if self.stiffMatType[0].lower() in ["e", "b"]:
        phi = 0
    # Bending terms after Timoshenko-Ehrenfest
    elif self.stiffMatType[0].lower() == "t":
        G = E/(2*(1+nu))
        AS = A * ϰ
        phi = 12*E*I/(ϰ*A*G*l**2)
    c = E*I/(ell**3*(1+phi))
    k += c*np.array([[0,     0,              0, 0,      0,                0],
                     [0,    12,          6*ell, 0,    -12,            6*ell],
                     [0, 6*ell, ell**2*(4+phi), 0, -6*ell,   ell**2*(2-phi)],
                     [0,     0,              0, 0,      0,                0],
                     [0,   -12,         -6*ell, 0,     12,           -6*ell],
                     [0, 6*ell, ell**2*(2-phi), 0, -6*ell,   ell**2*(4+phi)]],
                    dtype=float)
    return k

def MatMat(self, i):
    return(np.array([[self.E[i]*self.A[i],                   0],
                     [                  0, self.E[i]*self.I[i]]]))

def MassMatElem(self, i):
    ell = self.ell[i]
    rho = self.rho[i]
    A = self.A[i]
    if self.stiffMatType[0].lower() in ["e", "b"]:
        if self.massMatType[0].lower() == "c":
            c = A*rho*ell/420
            m = c*np.array([[140,       0,         0,  70,       0,         0],
                            [  0,     156,    22*ell,   0,      54,   -13*ell],
                            [  0,  22*ell,  4*ell**2,   0,  13*ell, -3*ell**2],
                            [ 70,       0,         0, 140,       0,         0],
                            [  0,      54,    13*ell,   0,     156,   -22*ell],
                            [  0, -13*ell, -3*ell**2,   0, -22*ell,  4*ell**2]],
                           dtype=float)
        elif self.massMatType[0].lower() == "l":
            alpha = 0
            c = A*rho*ell/2
            m = c*np.array([[ 1, 0,              0, 1, 0,                0],
                            [ 0, 1,              0, 0, 0,                0],
                            [ 0, 0, 2*alpha*ell**2, 0, 0,                0],
                            [ 1, 0,              0, 1, 0,                0],
                            [ 0, 0,              0, 0, 1,                0],
                            [ 0, 0,              0, 0, 0, 2*alpha*ell**2.]],
                           dtype=float)
    elif self.stiffMatType[0].lower() == "t":
        IR = self.I[i]
        nu = 0.3
        G = self.E[i]/(2*(1+nu))
        AS = A * ϰ
        phi = 12*self.E[i]*self.I[i]/(ϰ*A*G*ell**2)
        m = A*rho*ell/420*np.array([[140, 0, 0,  70, 0, 0],
                                    [  0, 0, 0,   0, 0, 0],
                                    [  0, 0, 0,   0, 0, 0],
                                    [ 70, 0, 0, 140, 0, 0],
                                    [  0, 0, 0,   0, 0, 0],
                                    [  0, 0, 0,   0, 0, 0]], dtype=float)
        # tranlational inertia
        cT = A*rho*ell/(1+phi)**2
        m += cT*np.array([[0,                                   0,                                     0, 0,                                   0,                                     0],
                          [0,           13/35+7/10*phi+1/3*phi**2,   (11/210+11/120*phi+1/24*phi**2)*ell, 0,            9/70+3/10*phi+1/6*phi**2,    -(13/420+3/40*phi+1/24*phi**2)*ell],
                          [0, (11/210+11/120*phi+1/24*phi**2)*ell,  (1/105+1/60*phi+1/120*phi**2)*ell**2, 0,   (13/420+3/40*phi+1/24*phi**2)*ell, -(1/140+1/60*phi+1/120*phi**2)*ell**2],
                          [0,                                   0,                                     0, 0,                                   0,                                     0],
                          [0,            9/70+3/10*phi+1/6*phi**2,     (13/420+3/40*phi+1/24*phi**2)*ell, 0,           13/35+7/10*phi+1/3*phi**2,   (11/210+11/120*phi+1/24*phi**2)*ell],
                          [0,  -(13/420+3/40*phi+1/24*phi**2)*ell, -(1/140+1/60*phi+1/120*phi**2)*ell**2, 0, (11/210+11/120*phi+1/24*phi**2)*ell,  (1/105+1/60*phi+1/120*phi**2)*ell**2]],
                         dtype=float)
        # rotary inertia
        cR = rho*IR/(ell*(1+phi)**2)
        m += cR*np.array([[0,                  0,                                0, 0,                   0,                                0],
                          [0,                6/5,               (1/10-1/2*phi)*ell, 0,                -6/5,               (1/10-1/2*phi)*ell],
                          [0, (1/10-1/2*phi)*ell, (2/15+1/6*phi+1/3*phi**2)*ell**2, 0, (-1/10+1/2*phi)*ell, (1/30+1/6*phi-1/6*phi**2)*ell**2],
                          [0,                  0,                                0, 0,                   0,                                0],
                          [0,               -6/5,              (-1/10+1/2*phi)*ell, 0,                 6/5,              (-1/10+1/2*phi)*ell],
                          [0, (1/10-1/2*phi)*ell, (1/30+1/6*phi-1/6*phi**2)*ell**2, 0, (-1/10+1/2*phi)*ell, (2/15+1/6*phi+1/3*phi**2)*ell**2]],
                         dtype=float)
    return m
