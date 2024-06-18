import os
import numpy as np
import gsd.hoomd
import multiprocessing as mp
import freud

def name_directory(N, epsilon, gamma):
    return f"N{N}_eps{epsilon}_gamma{gamma}/"

def name_gsd(N, epsilon, period, gamma):
    return f"N{N}_eps{epsilon}_period{period}_gamma{gamma}"

def path_to_simulation_state(prefix, N, epsilon, period, gamma):
    return '/home/invites/foldes/dynamique_CG/trajectoires/' + prefix + f'/N{N}/' + name_directory(N, epsilon, gamma) + name_gsd(N, epsilon, period, gamma)

def get_position(args):
    data, frame = args
    return data[frame].particles.position[:]
trajectoires = []

def msd_par(state):
    state.load_msd()
    return None

class state:

    def __init__(self, N, epsilon, period, gamma=5., prefix = 'langevin_fene'):
        self.N = N
        self.epsilon = epsilon
        self.period = period
        self.gamma = gamma
        self.prefix = prefix
        self.name = name_gsd(self.N, self.epsilon, self.period, self.gamma)
        self.name_directory = name_directory(self.N, self.epsilon, self.gamma)
        self.path_gsd = '/home/invites/foldes/dynamique_CG/trajectoires/' + self.prefix + f'/N{self.N}/' + self.name_directory + self.name
        self.path_directory_msd = f'/home/invites/foldes/dynamique_CG/data_processed/msd/N{self.N}/{self.name_directory}'
        self.path_msd = self.path_directory_msd + f'/{self.name}_msd.npy'
        self.gsd_file = gsd.hoomd.open(self.path_gsd,'rb')
        pass

    def __str__(self) -> str:
        return f'{self.prefix}, N={self.N}, epsilon = {self.epsilon}, period = {self.period}'

    def load_conformations(self):
        with self.gsd_file as data:
            print('#data =', len(data))
            print(f'epsilon = {self.epsilon}, N = {self.N}, period = {self.period}')

            with mp.Pool(processes=mp.cpu_count()) as pool:
                conf = pool.map(
                    get_position,
                    [(data, frame) for frame in range(len(data))]
                    )
        self.conf = conf
        return conf

    def load_msd(self):
        if os.path.exists(self.path_msd):
            self.MSD = np.load(self.path_msd)
        else:
            self.MSD = self._compute_msd()
            os.makedirs(self.path_directory_msd, exist_ok=True)
            np.save(self.path_msd, self.MSD)
        pass
    def _compute_msd(self):
        hoomd_box = self.gsd_file[0].configuration.box
        box = freud.box.Box(Lx=hoomd_box[0], Ly=hoomd_box[1], Lz=hoomd_box[2])
        msd = freud.msd.MSD(box=box, mode='window')
        print('computing MSD for', self.__str__())
        if hasattr(self, 'conf'):
            msd.compute(self.conf)
        else:
            msd.compute(self.load_conformations())
        return msd.msd

class exp:
    def __init__(self, N, epsilons, periods, gamma = 5., prefix = 'langevin_fene') -> None:
        self.N = N
        self.epsilons = epsilons
        self.periods = periods
        self.gamma = gamma
        self.prefix = prefix
        states = [[[] for e in range(len(epsilons))] for ts in range(len(periods))]
        for ts, period in enumerate(periods):
            for e, eps in enumerate(epsilons):
                states[ts][e] = state(self.N, eps, period, gamma = gamma, prefix = prefix)
        self.states = states
        pass

    def load_frames(self):
        for ts, period in enumerate(self.periods):
            for e, eps in enumerate(self.epsilons):
                self.states[ts][e].load_conformations()


    def load_msds(self):
        missing_msds = []
        for ts, period in enumerate(self.periods):
            for e, eps in enumerate(self.epsilons):
                if os.path.exists(self.states[ts][e].path_msd):
                    self.states[ts][e].load_msd()
                else :
                    missing_msds.append((ts, e))
        for ts,e in missing_msds:
            self.states[ts][e].load_conformations()
        # with mp.Pool(processes=mp.cpu_count()) as pool:
        #         result = pool.map(
        #             self.msd_par,
        #             missing_msds
        #         )
        with mp.Pool(processes=mp.cpu_count()) as pool:
                result = pool.map(
                    msd_par,
                    [self.states[ts][e] for ts,e in missing_msds]
                )