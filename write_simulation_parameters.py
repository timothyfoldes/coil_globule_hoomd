from constants import *
import variables

# Writes a txt file including all simulation parameters.

def write(path_users_directory, Nsteps, period, dt, N, epsilon, tune, therm, bond, method, LJ, seed, EXCLUDE_NN, gamma, ring):
    f= open(path_users_directory + f"parameters_Nstep{Nsteps}_period{period}_dt{round(dt,4)}_N{N}_eps{epsilon}.txt","w+")

    f.write("N = {} \n".format(N))
    f.write("epsilon = {} \n".format(epsilon))
    f.write("Lx, Ly, Lz = {}, {}, {} \n".format(Lx, Ly, Lz))
    f.write("Nthermalize = {} \n".format(Nthermalize))
    f.write("period = {} \n".format(period))
    f.write("k_harmonic = {} \n".format(k_harmonic))
    f.write("r0_harmonic = {} \n".format(r0_harmonic))
    f.write("k_fene = {} \n".format(k_fene))
    f.write("r0_fene = {} \n".format(r0_fene))
    f.write("gamma = {} \n".format(gamma))
    f.write("kt = {} \n".format(kt))
    f.write("r_cut = {} \n".format(r_cut))
    f.write("sigma fene = {} \n".format(sigma_fene))
    f.write("sigma lj = {} \n".format(sigma_lj))
    f.write("dt = {} \n".format(dt))
    f.write(f"steps = {Nsteps} \n")
    f.write(f"period = {period} \n")
    f.write(f"tune = {tune} \n")
    f.write(f"therm = {therm} \n")
    f.write(f"bond = {bond} \n")
    f.write(f"method = {method} \n")
    f.write(f"LJ = {LJ} \n")
    f.write(f"seed = {seed} \n")
    f.write(f'EXCLUDE_NN = {EXCLUDE_NN}')
    f.write(f'ring = {ring}')



    f.close()