def tau(gamma): # Gives mode p's time constant (small p/N approx)
    return gamma / ((3.14**2)*3)
# def Nsteps(period):
#     return (5*10**4)*period
def Nsteps(period):
    return (5*10**4)*period
# Langevin
kt = 1

#LJ
sigma_lj = 1/1.122
EXCLUDE_NN = True #exclude NN pairs from interaction pair list (if True, NO LJ between NN)
LJ = True #add LJ interactions between monomer pairs


#FENE:
sigma_fene = 1/1.122
epsilon_fene = 1
k_fene = 30
r0_fene = 1.5*sigma_fene
#np.sqrt(3*kt/k)/1.122

#HARMONIC
k_harmonic = 3
r0_harmonic = 0


### Simulation constants
# gamma = 0.5

# Box size
Lx, Ly, Lz = 10000, 10000, 10000

##LJ

r_cut = sigma_lj*2.5
check_period = 1
r_buff = 1.2

# Simulation steps
Nthermalize = 100_000_000
dt = 0.01
