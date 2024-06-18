import os
from pathlib import Path
import sys
import numpy as np
import json
import subprocess
import shutil
import time

def directory(epsi):
    return f'{epsi:.2f}'.replace('.', '')

def load(epsi, N):
    path = Path(".") / directory(epsi) / '0'
    frames = []
    for dir in os.listdir(path):
        with open(path / dir / f'{N}.txt') as file:
            frames.extend(map(json.loads, file))
            # for line in file:
            #     frames.append(json.loads(line))
    return np.asarray(frames)

# subprocess.run("./isaw-par", f"run \
#     --output conformation \
#     --size {size} \
#     --threads 1 \
#     --thermalize 1024 \
#     --samples 10 \
#     --subsampling 1 \
#     isaw \
#         --epsilon {epsilon}")
def generate_conformation(epsilon, size):
    os.system(f"bash run.sh {epsilon} {size}")

def center_frames(frames):
    #frames = axis 0
    #monomere = axis 1
    #dim = axis 2

    return np.array(frames - np.array(frames[:,:,:]).mean(axis = 1)[:, np.newaxis,:])
    #return np.array(frames - np.array(frames[:,0,:])[:, np.newaxis,:])

def get_conformation(epsilon, size):
    generate_conformation(epsilon, size)
    conformation = center_frames(load(epsilon, size))
    path = Path(".") / directory(epsilon) / f'{size}.txt'
    shutil.rmtree(path, ignore_errors=True)
    shutil.rmtree(Path("./save", ignore_errors=True))
    return conformation
