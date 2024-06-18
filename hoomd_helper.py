import sys
sys.path.append('./modules/')
import hoomd
import gsd.hoomd
import paths_analysis as path_home
from variables import *
from constants import *
import datetime
import os

def get_initial_positions(N, epsilon, ring):
    def path_init_pos(N,epsilon):
        return f'./init_pos/init_pos_N{N}_eps0{int(epsilon*100)}.npy'
    if ring==False:
        print(epsilon)
        path_init_pos_therm = f'./init_pos/'+ method+ '_' + bond + f'/init_pos_N{N}_eps{epsilon}.npy'
        if os.path.exists(path_init_pos_therm): #if 50k period sim exists, get init pos from last frame
            init_pos = np.load(path_init_pos_therm)
        
        elif epsilon == 3:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(0.27*100)}.npy')[0,:,:]
        elif epsilon >= 1:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0100.npy')[0,:,:]
        elif epsilon>0.5 and N==12000:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(0.5*100)}.npy')[0,:,:]
        elif epsilon in [0.28]:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(0.27*100)}.npy')[0,:,:]
        elif epsilon in [0.29]:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(0.3*100)}.npy')[0,:,:]
        elif epsilon in [0.31,0.32]:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(0.3*100)}.npy')[0,:,:]
        elif epsilon in [0.33,0.34]:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(0.35*100)}.npy')[0,:,:]
        elif N==24000:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(0.35*100)}.npy')[0,:,:]

        else:
            init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(epsilon*100)}.npy')[0,:,:]




    if ring == True:
        init_pos = np.load(f'./init_pos/init_pos_ring_N{N}_eps0{int(epsilon*100)}.npy')
    return init_pos

def make_initial_snapshot(N, epsilon, ring, Lx, Ly, Lz):
    snapshot = gsd.hoomd.Snapshot()
    snapshot.particles.N = N
    # init_pos=np.load(f'./init_pos/init_pos_N{N}_eps0{int(50)}.npy')[0,:,:]
    # snapshot.particles.position = init_pos
    snapshot.particles.position = get_initial_positions(N, epsilon, ring)
    # init_pos=[[0,0,k] for k in range(N)]

    snapshot.particles.types = ['monomere']
    snapshot.particles.typeid = [0] * N
    snapshot.configuration.box = [Lx, Ly, Lz, 0, 0, 0]
    snapshot.bonds.N = N-1 if ring==False else N
    snapshot.bonds.types = ['polymer']
    if ring == False:
        bond_list = [[i,i+1] for i in range(N-1)]
    if ring == True:
        bond_list = [[i,(i+1)%N] for i in range(N)]
    snapshot.bonds.group = bond_list
    print(f'creating initial snapshot with the following properties : Lx, Ly, Lz = {Lx, Ly, Lz}')
    print(f'N = {N}')
    return snapshot

def set_harmonic(k, r0):
    harmonic = hoomd.md.bond.Harmonic()
    harmonic.params['polymer'] = dict(k = k, r0 = r0)
    return harmonic

def set_fene(k_fene, r0_fene, sigma_fene, epsilon_fene):
    fene = hoomd.md.bond.FENEWCA()
    fene.params['polymer'] = dict(k=k_fene, r0=r0_fene, sigma=sigma_fene, epsilon=epsilon_fene, delta = 0)
    return fene

def set_bond_force(bond):
    if bond == 'fene':
        print(f'initializing FENE bonds K={k_fene}, r0={r0_fene} \n')
        bond_force = set_fene(k_fene, r0_fene, sigma_fene, epsilon_fene)
        print(f'k_fene = {k_fene}, r0_fene = {r0_fene}')

    if bond == 'harmonic':
        print(f'initializing HARMONIC bonds \n')
        bond_force = set_harmonic(k = k_harmonic, r0 = r0_harmonic)
        print(f'k_harmonic = {k_harmonic}, r0 = {r0_harmonic}')
    return bond_force

def set_LJ(epsilon):
    if epsilon == 0:
        print(f'setting LJ potential with epsilon = {epsilon}\n')
        new_eps = 0.1
        print(f'setting a TREE nl list with r_buff={r_buff}')
        nl = hoomd.md.nlist.Tree(buffer = r_buff, rebuild_check_delay=check_period, check_dist=True)

        if EXCLUDE_NN==False:
            print('LJ IS computed between bonded particles \n')
            nl.exclusions = []
        else:
            print('LJ IS NOT computed between bonded particles \n')
        lj = hoomd.md.pair.LJ(nlist = nl, default_r_cut=2.5*sigma_lj, default_r_on=0, mode = 'none')
        lj.params[('monomere', 'monomere')] = dict(sigma = sigma_lj, epsilon = new_eps)
        lj.r_cut[('monomere', 'monomere')] = r_cut

    else:
        print(f'setting LJ potential with epsilon = {epsilon}\n')
        print(f'setting a TREE nl list with r_buff={r_buff}')
        nl = hoomd.md.nlist.Tree(buffer = r_buff, rebuild_check_delay=check_period, check_dist=True)

        if EXCLUDE_NN==False:
            print('LJ IS computed between bonded particles \n')
            nl.exclusions = []
        else:
            print('LJ IS NOT computed between bonded particles \n')
        lj = hoomd.md.pair.LJ(nlist = nl, default_r_cut=2.5*sigma_lj, default_r_on=0, mode = 'none')
        lj.params[('monomere', 'monomere')] = dict(sigma = sigma_lj, epsilon = epsilon)
        lj.r_cut[('monomere', 'monomere')] = r_cut

    return lj, nl

def configure_integration_method(method, gamma, dt, forces):

    all = hoomd.filter.All()
    if method == 'brownian':
        int_method = hoomd.md.methods.Brownian(all, kT=kt)

    if method == 'langevin':
        int_method = hoomd.md.methods.Langevin(all, kT=kt)

    int_method.gamma.default = gamma

    print(f'integrating with method = {method}')
    print(f'dt = {dt}')
    print(f'gamma = {gamma}')


    integrator = hoomd.md.Integrator(dt = dt, methods=[int_method], forces=forces)
    return integrator

def stdout_table(sim, lj, bond_force):
    class Status():

        def __init__(self, sim):
            self.sim = sim

        @property
        def seconds_remaining(self):
            try:
                return round((self.sim.final_timestep - self.sim.timestep) / self.sim.tps)
            except ZeroDivisionError:
                return 0

        @property
        def etr(self):
            return str(datetime.timedelta(seconds=self.seconds_remaining))

    thermodynamic_properties = hoomd.md.compute.ThermodynamicQuantities(filter=hoomd.filter.All())
    sim.operations.computes.append(thermodynamic_properties)
    logger = hoomd.logging.Logger(categories=['scalar', 'string'])
    status = Status(sim)
    logger[('Status', 'etr')] = (status, 'etr', 'string')
    logger.add(sim, quantities=['timestep', 'tps'])
    logger.add(bond_force, quantities = ['energy'])
    if LJ:
        logger.add(lj, quantities=['energy'])
    logger.add(thermodynamic_properties, ['potential_energy'])
    table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=10000), logger=logger)
    return table


def tune_rbuff(sim, nl, steps, buffer_min, buffer_max, Nbins, set_r_buff, set_check_period):
    r_buffs = np.round(np.linspace(buffer_min, buffer_max, Nbins), 3)
    TPSs = []
    shortest_rebuilds = []
    print(f'Staring tune of buffer size for the neighboring \n')
    print(f'r-buff in {r_buffs} \n')

    for r_buff in r_buffs:
        print(f'buffer size = {r_buff} \n')
        nl.buffer = r_buff
        print(f'starting run for {steps} steps \n')
        sim.run(steps)
        print(f'for buffer size = {r_buff}, TPS = {sim.tps} \n, shortest rebuild = {nl.shortest_rebuild} \n')
        TPSs.append(sim.tps)
        shortest_rebuilds.append(nl.shortest_rebuild)

    best_r_buff = r_buffs[TPSs.index(max(TPSs))]
    best_shortest_rebuild = shortest_rebuilds [TPSs.index(max(TPSs))]
    print(f'The best buffer size is: {best_r_buff} with a TPS of {max(TPSs)} and shortest rebuild = {best_shortest_rebuild} \n')
    if set_r_buff == True:
        print(f'setting buffer size to {best_r_buff} \n')
        nl.buffer = best_r_buff
    if set_check_period:
        print(f'setting rebuuld check delay to {best_shortest_rebuild - 2} \n')
        nl.rebuild_check_delay = best_shortest_rebuild - 2
    return best_r_buff, best_shortest_rebuild

