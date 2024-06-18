import sys
sys.path.append('/users/invites/foldes/Documents/dynamique_CG/simulation/simulation_modules/')

### Paths

_path_home = "/home2/invites/foldes/dynamique_CG/"

_path_data = _path_home + "data_processed/"

_path_trajectoires = _path_home + "trajectoires/"

### Names

def _name_directory(N, epsilon, gamma):
    return f"N{N}_eps{epsilon}_gamma{gamma}/"

def _name_gsd(N, epsilon, gamma, period):
    return f"N{N}_eps{epsilon}_period{period}_gamma{gamma}"

def _name_observable(N, epsilon, gamma, period, observable):
    return _name_gsd(N, epsilon, gamma, period) + '_' + observable + '.npy'

###paths to state point directory

def path_trajectory_directory(N, epsilon, gamma, method):
    return _path_trajectoires + method + '/' + f'N{N}' + '/' + _name_directory(N, epsilon, gamma)

def path_observable_directory(N, epsilon, gamma, method, observable):
    return _path_data + method + '/' + observable +'/' + f'N{N}' + '/' + _name_directory(N, epsilon, gamma)

### paths to files

def path_gsd(N, epsilon, gamma, period, method):
    return path_trajectory_directory(N, epsilon, gamma, method) + _name_gsd(N, epsilon, gamma, period)

def path_observable(N, epsilon, gamma, period, method, observable):
    return path_observable_directory(N, epsilon, gamma, method, observable) + _name_observable(N, epsilon, gamma, period, observable)