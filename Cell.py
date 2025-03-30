import numpy as np

# Cell class to represent a cell in the simulation
class Cell():
    # Initialize the cell with given parameters
    def __init__(self, n, r, s, m): 

        self.n = n
        self.r = r
        self.s = s
        self.m = m

        self.type = 0
        self.cat = [False, False, False]


    def get_content(self):
        return [self.n, self.r, self.s, self.m] 
    
    def get_type(self):
        return self.type

    def __str__(self):
        return f"n: {self.n}, r: {self.r}, s: {self.s}, m: {self.m}, type: {self.type}"
    
    # Update the cell's state based on the given parameters using a Gillespie algorithm
    def update(self, params):

        zeta = params["zeta"]
        n_0 = params["n_0"]
        eps = params["eps"]
        omega = params["omega"]
        phi = params["phi"]
        kQ = params["kQ"]
        kT = params["kT"]

        n, r, m = self.n, self.r, self.m

        Q = r/(n+r+kQ)
        T = n*r/(n+r+kT)

        # Calculate the rates of different events
        rates = np.array([zeta + n_0*m, eps*n + omega*(1-Q)*T, (1-phi)*Q*T, phi*Q*T])
        Lambda = sum(rates)

        dt = -np.log(np.random.uniform(0.0,1.0))/Lambda      # Time step for the next event
        ran = np.random.uniform(0.0,1.0)                     # Random number for event selection

        if ran < rates[0]/Lambda:
            self.n += 1
        elif ran < (rates[0]+rates[1])/Lambda:
            self.n -= 1
            self.r += 1
        elif ran < (rates[0]+rates[1]+rates[2])/Lambda:
            self.n -= 1
            self.s += 1
        else:
            self.n -= 1
            self.m += 1

        return dt

    # Check if the cell can split based on the given parameters
    def split(self, params):
        s0 = params["s0"]
        if self.s >= s0:
            return True
        else:
            return False
    
    # Partition the cell's content into two and return either half
    def partition(self, q):
        ran = np.random.randint(2)
        if ran == 0:
            return np.floor(q/2)
        else:
            return np.ceil(q/2)
    
    # Divide the cell into two new cells and pick one of them randomly (Lineage growth)
    def divide(self):
        n = self.partition(self.n)
        r = self.partition(self.r)
        s = self.partition(self.s)
        m = self.partition(self.m)

        return Cell(n, r, s, m)
    
    # Update the cell's type based on its current state
    def update_type(self):

        cat1, cat2, cat3 = self.cat
        
        if( not cat1 and not cat3 and self.n==0 and self.m==0 ):
            self.type = 1                                             # Type 1: m-Dormant cell (n=0, m=0)
            cat1 = True
        if( not cat2 and not cat3 and self.r==0 ):
            self.type = 2                                             # Type 2: r-Dormant cell (r=0)
            cat2 = True
        if( not cat3 and self.m==0 and self.r==0 ):
            self.type = 3                                             # Type 3: mr-Dormant cell (m=0, r=0)
            cat3 = True

        self.cat = [cat1, cat2, cat3]