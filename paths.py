import sys
sys.path.append('/users/invites/foldes/Documents/dynamique_CG/simulation/modules/')
import variables
def name_directory(N, epsilon, gamma):
    return f"N{N}_eps{epsilon}_gamma{gamma}/"

def name_gsd(period, N, epsilon, gamma):
    return f"N{N}_eps{epsilon}_period{period}_gamma{gamma}"

 #paths to state point directory

def path_home_directory(N, epsilon, gamma):
    return path_home + name_directory(N, epsilon, gamma)

def path_users_directory(N, epsilon, gamma):
    return path_users + name_directory(N, epsilon, gamma)

 # paths to gsd files

def path_home_gsd(period, N, epsilon, gamma):
    return path_home_directory(N, epsilon, gamma) + name_gsd(period, N, epsilon, gamma)

def path_users_gsd(period, N, epsilon, gamma):
    return path_users_directory(N, epsilon, gamma) + name_gsd(period, N, epsilon, gamma)


### Paths

path_home = "/home/invites/foldes/"

if variables.ring == False:
    path_users = f"/users/invites/foldes/Documents/dynamique_CG/simulation/trajectoires/{variables.method}_{variables.bond}/"
if variables.ring == True:
    path_users = f"/users/invites/foldes/Documents/dynamique_CG/simulation/trajectoires/{variables.method}_{variables.bond}_ring/"
