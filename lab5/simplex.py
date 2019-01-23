import numpy as np


class Simplex:
    def __init__(self, c, A, b):
        """
        Parameters
        ----------
        c : Коефіцієнти при цільовій функції
        A : Матриця коефіцієнтів
        b : Вільні члени
        
        Minimize f = c[i] * x[i]
        A[j, i] * x[i] <= b[j]
        """
        
        self.c = -c
        self.A = A
        self.b = b
        self.f = 0
        self.base_col = np.arange(len(c))
        self.base_row = np.arange(len(c), len(c) + len(b))
        
    def solve(self):
        if np.all(self.b >= 0):
            if np.all(self.c <= 0):
                return 'Відповідь'
            else:
                self.general_col = self.c.argmax()
                bi_plus = np.where(self.b >= 0)[0]
                ai_plus = np.where(self.A[:,self.general_col] > 0)[0]
                plus = np.intersect1d(ai_plus, bi_plus)
                if not plus.size:
                    return 'Необмежений мінімум'
                self.general_row = plus[(self.b[plus] / self.A[plus, self.general_col]).argmin()]
                self.general_element = self.A[self.general_row, self.general_col]
        else:
            self.general_row = self.b.argmin()
            ai_minus = np.where(self.A[self.general_row] < 0)[0]
            if not ai_minus.size:
                return 'Відсуття допустима область'
            self.general_col = ai_minus[(self.b[self.general_row] / self.A[self.general_row, ai_minus]).argmin()]
            self.general_element = self.A[self.general_row, self.general_col]
        
        self.Afull = np.block([
            [self.b[:,np.newaxis], self.A],
            [self.f, self.c]
        ])
        self.recalculation()
        self.change_base()

    def recalculation(self):
        new_general_row =  self.Afull[self.general_row, :] / self.general_element
        new_general_col =  - self.Afull[:, self.general_col+1] / self.general_element
        new_general_element = 1 / self.general_element
        
        self.Afull[self.general_row, self.general_col+1] = new_general_element

        Aplus = new_general_col[:,np.newaxis] @ self.Afull[self.general_row][:, np.newaxis].T
        self.Afull = self.Afull + Aplus
        
        self.Afull[self.general_row] = new_general_row
        self.Afull[:, self.general_col+1] = new_general_col
        self.Afull[self.general_row, self.general_col+1] = new_general_element
        
        self.c = self.Afull[-1, 1:]
        self.A = self.Afull[:-1, 1:]
        self.b = self.Afull[:-1,0]
        self.f = self.Afull[-1, 0]
    
    def change_base(self):
        self.base_col[self.general_col], self.base_row[self.general_row] = (
            self.base_row[self.general_row], 
            self.base_col[self.general_col]
        )
        
    def fit(self, max_iter=100):
        for i in range(max_iter):
            res = self.solve()
            if res is not None:
                if res == 'Відповідь':
                    res_list = list(zip(self.base_row, self.b)) + list(zip(self.base_col, len(self.base_col) * [0]))
                    self.res = np.array(sorted(res_list, key=lambda x: x[0]))[:len(self.c), 1]
                    res_text = ['x{}={}\n'.format(inx, val) for inx, val in enumerate(self.res)]
                    res_text.append('Значення функції: {}'.format(self.f))
                    return ''.join(res_text)
                return res
        return 'Занадто мало ітерацій'