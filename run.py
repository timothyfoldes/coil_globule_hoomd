import sys
sys.path.append('./modules/')
sys.path.remove('/users/invites/foldes/.local/lib/python3.8/site-packages')
sys.path.insert(0,"/users/lptl/viot/HOOMD3.8/local/lib64/python3.10/site-packages/")
import hoomd
import gsd.hoomd
import paths
from constants import *
import hoomd_helper
import os
import numpy as np
import paths_analysis as path_home
def run_simu(epsilon, N, ring, bond, method, gamma, Nsteps, period, path_home_gsd, dt, seed, therm, tune):


    sim = hoomd.Simulation(device=hoomd.device.GPU(), seed=seed)
    snapshot = hoomd_helper.make_initial_snapshot(N, epsilon, ring, Lx, Ly, Lz)
    sim.create_state_from_snapshot(snapshot)

    ###Forces

    ## Bound forces

    bond_force = hoomd_helper.set_bond_force(bond=bond)

        ## Pair forces
    if LJ:
        print(epsilon)
        lj, nl = hoomd_helper.set_LJ(epsilon)
        forces = [bond_force, lj]
    else:
        forces = [bond_force]
        lj = 'None'

    ### Integration Algorithm

    sim.operations.integrator = hoomd_helper.configure_integration_method(method=method, gamma=gamma, dt=dt, forces=forces)

    ### Stdout logs (ETR, simulation step, bond energy, LJ energy, total potential energy)

    table = hoomd_helper.stdout_table(sim, lj, bond_force)
    sim.operations.writers.append(table)

    ### Simulation

    ### Thermalization
    # path_init_pos_therm = f'./init_pos/langevin_fene/init_pos_N{N}_eps{epsilon}.npy'
    if therm:# and not os.path.exists(path_init_pos_therm):
        # print('fene')
        # for k_fen, r0_fen, eps_fene, sig_fene in zip( np.linspace(1,k_fene,50), np.linspace(0,r0_fene,50), np.linspace(0,epsilon_fene,50), np.linspace(0,sigma_fene,50)):
        #     print('fene_bond')
        #     lj.params[('monomere', 'monomere')] = dict(sigma = 0, epsilon = 0)
        #     bond_force.params['polymer'] = dict(k=k_fen, r0=r0_fen, sigma=sig_fene, epsilon=eps_fene, delta = 0)
        #     print(f'sig_fene = {round(sig_fene, 3)},  r0_fene = {round(r0_fen, 3)}, k_fene = {round(k_fen, 3)}, eps_fene = {round(eps_fene,3)}')
        #     sim.run(10_000)
        # sim.run(100_000)
        # print('LJ')
        # for sig_lj,eps in zip(np.linspace(0.01,sigma_lj,10), np.linspace(0,epsilon,10)):
        #     lj.params[('monomere', 'monomere')] = dict(sigma = sig_lj, epsilon = epsilon)
        #     print(f'sigma_lj = {round(sig_lj, 3)}, eps_fene = {round(eps, 3)}')
        #     sim.run((1/sig_lj)*5000)
        # print(f'Starting thermaliation for {Nthermalize} steps')
        print(f"thermalizing for {Nthermalize} steps")
        sim.run(Nthermalize)
    # else :
    #     print(f"thermalizing for {1_000_000} steps, just for good measure")
    #     sim.run(1_000_000)

    ### Benchmark
    if tune and LJ:
        hoomd_helper.tune_rbuff(sim, nl, steps = 200_000, buffer_min=0.5, buffer_max=1.5, Nbins=10, set_r_buff=True, set_check_period=False)

    ### Run
    os.makedirs(paths.path_home_directory(N, epsilon, gamma), exist_ok=True)

    gsd_writer = hoomd.write.GSD(filename=path_home_gsd, trigger=hoomd.trigger.Periodic(period), mode='ab')
    sim.operations.writers.append(gsd_writer)

    print(f'Running simulation for {Nsteps} steps recording conformation every {period} step --> {int(Nsteps/period)} frames per GSD file  \n')
    sim.run(Nsteps)
    print(f'Simulation complete \n')