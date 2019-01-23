import numpy as np

f = lambda x, u: -(x+u)/x
a = 1.
b = 3.
u0 = 0.5

def method_runge_kutti(a, b, u0, num=1000):
    f = lambda x, u: -(x+u)/x
    xi, h = np.linspace(a, b, num, retstep=True)
    yi = np.array([u0])
    for i in range(num-1):
        k1 = f(xi[i], yi[i])
        k2 = f(xi[i]+h/2, yi[i]+h*k1/2)
        k3 = f(xi[i]+h/2, yi[i]+h*k2/2)
        k4 = f(xi[i]+h, yi[i]+h*k3)
        yi = np.append(yi, yi[i] + h * (k1 + 2*k2 + 2*k3 + k4) / 6)
    return xi, yi

xi, yi = method_runge_kutti(a, b, u0, 30)

from scipy.integrate import odeint

y0 = 1
f = lambda u, x: -(x+u)/x
t = np.linspace(1,3,1000)

y = odeint(f,y0,t)
