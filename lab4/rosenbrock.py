import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

def func(x):
    return x[0]**3 + x[1]**3 - 3 * x[0] * x[1]

def method_rosenbrock_step(func=func, 
                           learning_rate=0.1*np.ones(2), 
                           max_iter=10000, 
                           x0=np.array([8, 9]),
                           alpha=3,
                           beta=-0.5,
                           e0=np.eye(2),
                           dim=2):
    
    xi = [x0]
    yi = [func(x0)]
    si = [dim * [False]]
    step_info = []
    
    for i in range(max_iter):
        
        s_curr = dim * [False]
        
        for inx in range(dim):
            
            xnew = xi[-1] + learning_rate[inx] * e0[inx]
            ynew = func(xnew)
            if ynew < yi[-1]:
                xi.append(xnew)
                yi.append(ynew)
                s_curr[inx] = True
                
            step_info.append({
                'x': xnew,
                'y': ynew,
                's': s_curr[inx],
                'l': learning_rate[inx]
            })
        for inx in range(dim):
            if s_curr[inx]:
                learning_rate[inx] *= alpha
            else:
                learning_rate[inx] *= beta 
        if sum(si[-1])==2 and sum(s_curr)==0:
            break
        else:
            si.append(s_curr)
    step_info_sort = sorted(step_info, key=lambda x: x['y'])
    return step_info_sort[0]['x'], learning_rate

def method_rosenbrock(func=func, 
                      x0=np.array([8, 9]),
                      learning_rate=100*np.ones(2), 
                      max_iter=2000,
                      e0=np.eye(2), 
                      eps=10**-6):
    xi = [x0]
    yi = [func(xi[-1])]
    ei = [e0]
    learning_rate = learning_rate.copy()
    for i in range(max_iter):
        xnew, learning_rate = method_rosenbrock_step(func=func, 
                                                     x0=xi[-1], 
                                                     learning_rate=learning_rate, 
                                                     e0=ei[-1], 
                                                     max_iter=10**3)
        xi.append(xnew)
        yi.append(func(xi[-1]))
        
        e = np.zeros_like(ei[-1])
        if np.array_equal(xi[-1], xi[-2]):
            break
        A1 = xi[-1] - xi[-2]
#         print(A1)
        e[0] = A1 / np.linalg.norm(A1)
        bx = 1
        by = - (e[0][0] * bx) / e[0][1]
        e[1] = [bx, by]
        e[1] /= np.linalg.norm(e[1])
        ei.append(e)
        if np.abs(yi[-1] - yi[-2]) < eps:
            break
    return xi, yi, ei
