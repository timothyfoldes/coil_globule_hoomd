import numpy as np

# epsilons = (np.arange(21)/10)[[7]]
# epsilons = np.array([0.1,0.2,0.25,0.27,0.3,0.35,0.4,0.45,0.5]).astype(float)
# epsilons = np.array([0.1,0.2,0.25,0.27,0.3,0.35,0.4,0.45,0.5]).astype(float)
epsilons = np.array([0.5]).astype(float)


Ns = np.array([24000])
periods = np.array([2000])
gammas = np.array([5.0])
tune = False
therm = True
bond = 'fene' #'harmonic' or 'fene'
method = 'langevin' #'brownian' or 'langevin'
ring = False
node = 'dazzler'

# nodes = ['ember', 'karma', 'magma', 'wilbur']
# nodes = ['cyclope', 'bosons', 'dazzler']
# nodes = ['chamber', 'mimeto', 'lisdal']

# epsilons = [0.,0.1,0.2,0.25,0.27,0.3,0.35,0.4,0.45,0.5,0.7]
# Ns = [200,400,800,1600,3000,6000,12000]