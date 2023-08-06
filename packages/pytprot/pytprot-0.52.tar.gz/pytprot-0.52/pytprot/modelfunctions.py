# Adding module location to sys.path
import sys
sys.path.append('/home/oth/anaconda3/lib/python3.8/site-packages')
sys.path.append('/Users/Maria/Desktop/Uni/sbi/SBI-Project/SBI_PYT/PPI_main') # Path to I_O_args script
sys.path.append('/home/oth/BHS/PYT/1.project/SBI_PYT/PPI_main') # Path to I_O_args script
sys.path.append('/home/oth/BHS/PYT/1.project/dash_test.py')
import os, numpy, scipy
import argparse as args
from Bio.PDB import *
from Bio.Seq import Seq
from Bio.PDB.PDBIO import PDBIO, Select
from Bio import pairwise2 as pw2
import inputfunctions, chainfunctions
#import dash_test




################################
#      MODEL BUILDING          #
################################



###### COMMON ATOMS BETWEEN TWO CHAINS (TO SUPERIMPOSE THEM)
###### A LO MEJOR VALE LA PENA INCLUIR get_atoms_list en common_chain_res

def get_atoms_list(chain):
    """Creates a list of the atoms only taking CA or P for protein and nucleic acids, respectively.
    This list of atoms will be lately used in the superimposition process."""
    type_chain = check_type(chain)
    if type_chain == "Protein":
        atom_id = "CA"
    elif type_chain == "DNA":
        atom_id = "P"
    atoms = chain.get_atoms()
    atoms_list = []
    for atom in atoms:
        if atom.id == atom_id:
            atoms_list.append(atom)
    return atoms_list


def common_chain_res(model1, model2):
    """
    Given a pair of chains, obtains the common residues and their respective CA atoms.
    Returns a tuple with two lists: The first one contains the list of atoms corresponding
    to the first chain. The second list contains the list of atoms of the second chain.
    :param chain1:
    :param chain2:
    :return:
    """
    print("Getting the common chains...")
    #res1 = [res for res in chain1 if res["CA"] or res["P"]
    #res2 = [res for res in chain2 if res["CA"] pr res["P"]]

    res1 = []
    res2 = []

    for res in model1:
        for atom in res:
            for a in atom:
                if a.id == "CA":
                    res1.append(atom)

    for res in model2:
        for atom in res:
            for a in atom:
                if a.id == "CA":
                    res2.append(atom)

    common_res1 = [res1 for res1, res2 in zip(res1, res2) if res1.get_resname() == res2.get_resname()]
    common_res2 = [res2 for res1, res2 in zip(res1, res2) if res1.get_resname() == res2.get_resname()]

    #chain1_atoms_list = [res["CA"] for res in common_res1]
    #chain2_atoms_list = [res["CA"] for res in common_res2]

    chain1_atoms_list = []
    chain2_atoms_list = []

    for res in common_res1:
        for atom in res:
            if atom.id == "CA":
                chain1_atoms_list.append(atom)

    for res in common_res2:
        for atom in res:
            if atom.id == "CA":
                chain2_atoms_list.append(atom)

    common_atoms = (chain1_atoms_list, chain2_atoms_list)

    return common_atoms


# ---------------------------------------------------------------------------------------
############ SUPERIMPOSING THE STRUCTURES


def Superimpose_pair(pair1, pair2, i):
    """
    Given a pair of chains, these are superimposed. The first input is the
    fixed chain, and the second one the moving chain. The rotran matrix is computed, applied to the
    second chain, and then the RMSD is computed.
    :param :
    :return: RMSD score between structures
    """

    print("Superimposing the structures...")

    equal_chains_moved=[]
    # Set fixed, moving models
    fixed_chain = pair1[0]
    moving_chain = pair2[i]
    pair_fixed_chain = pair1[1]
    pair_moving_chain = pair2[abs(i-1)]

    # Create the LIST OF ATOMS to be aligned
    fixed_atoms = get_atoms_list(fixed_chain)
    moving_atoms = get_atoms_list(moving_chain)

    # When superimposing chains are not equally sized
    if len(fixed_atoms) != len(moving_atoms):
        common_atoms = common_chain_res(fixed_chain, moving_chain)

        imposer = Superimposer()
        imposer.set_atoms(common_atoms[0], common_atoms[1])
        imposer.apply(pair_moving_chain.get_atoms())
        print(imposer.rms)

    # If they are the same size
    else:
        imposer = Superimposer()
        imposer.set_atoms(fixed_atoms, moving_atoms)
        imposer.apply(pair_moving_chain.get_atoms())
        return(imposer.rms, pair_moving_chain, pair_fixed_chain)


# FOR THE SUPERIMPOSE: If we're mutating the DNA chains, we don't really need to
# separate them, right?

def Superimpose(model1, model2, apply=False):
    """
    Given a pair of models, these are superimposed. The first input is the
    fixed chain, and the second one the moving chain. The rotran matrix is computed, applied to the
    second chain, and then the RMSD is computed.
    :param :
    :return: RMSD score between structures
    """

    print("Superimposing the structures...")

    # Set fixed, moving models
    fixed_model = model1
    moving_model = model2

    # Create the LIST OF ATOMS to be aligned
    fixed_atoms = []
    moving_atoms = []

    for fixed_chain in fixed_model:
        for res in fixed_chain:
            for atom in res:
                if atom.id == "CA":
                    fixed_atoms.append(atom)

    for moving_chain in moving_model:
        for res in moving_chain:
            for atom in res:
                if atom.id == "CA":
                    moving_atoms.append(atom)

        #fixed_atoms = [res["CA"] or res["P"] for res in chain1 if res.id[0] == " "]
        #moving_atoms = [res["CA"] or res["P"] for res in chain2 if res.id[0] == " "]

        # fixed_atoms = [res["CA"] or res["P"] for res in chain1 if res.id[0] == " "]
        # moving_atoms = [res["CA"] or res["P"] for res in chain2 if res.id[0] == " "]

    # When superimposing chains are not equally sized
    if len(fixed_atoms) != len(moving_atoms):
        common_atoms = common_chain_res(fixed_model, moving_model)
        imposer = Superimposer()
        imposer.set_atoms(common_atoms[0], common_atoms[1])
        if apply == True:
            imposer.apply(moving_model.get_atoms())
        return(imposer.rms)

    # If they are the same size
    else:
        imposer = Superimposer()
        imposer.set_atoms(fixed_atoms, moving_atoms)
        if apply == True:
            imposer.apply(moving_model.get_atoms())
        return(imposer.rms)



def clashes(model1, model2, type, dist=1.9):
    """
    Computes the steric clashes between two chains.
    Change the clash distance cutoff?
    :param chain1:
    :param chain2:
    :return:
    """

    print("Obtaining the clashes....")

    if type == "atom":
        atoms1 = [atom for atom in model1.get_atoms()]
        atoms2 = [atom for atom in model2.get_atoms()]

        neighborsearch = NeighborSearch(atoms2)

        neighbors = set()

        for atom in atoms1:
            center = atom.get_coord()
            neighbs = neighborsearch.search(center, dist, level='C')
            for x in neighbs:
                if x != chain1:
                    neighbors.add(x)

        if len(neighbors) != 0:
            return True
        else:
            return False

    if type == "residue": # Looking at the clashes between two chains
        chain1 = [atom for atom in model1.get_atoms()]
        chain2 = [atom for atom in model2.get_atoms()]

        neighborsearch = NeighborSearch(chain2) # Is it relevant which one we choose?

        neighbors = set()

        for atom in chain1:
            center = atom.get_coord()
            neighbs = neighborsearch.search(center, 8, level='R')
            #print(neighbs)
            for x in neighbs:
                if x != chain1:
                    neighbors.add(x)

        if len(neighbors) != 0:
            return True
        else:
            return False


## AN ALTERNATIVE TO LOOKING FOR CLASHES: COMPUTING THE DISTANCE

def get_dist(list1, list2):
    """Given two lists of atom coordinates, it calculates the distance."""
    import math
    distance_result = (list1[0] - list2[0]) ** 2 + (list1[1] - list2[1]) ** 2 + (list1[2] - list2[2]) ** 2
    return math.sqrt(abs(distance_result))

def get_distance(chain1, chain2):
    distances=[]
    chain1_atoms=chain1.get_atoms()
    atoms1=list()
    for atom in chain1_atoms:
        if atom.id == "CA":
            atoms1.append(atom)
    chain2_atoms=chain2.get_atoms()
    atoms2=list()
    for atom in chain2_atoms:
        if atom.id == "CA":
            atoms2.append(atom)

    for combination in itertools.product(atoms1, atoms2):
        coords1=combination[0].get_coord()
        coords2=combination[1].get_coord()
        dist=get_dist(list(coords1.tolist()), list(coords2.tolist()))
        distances.append(dist)

     #print(distances)
    num_min = 0
    if len(distances) != 0:
        dist_arr = numpy.array(distances)
        for dist in dist_arr:
            if dist < 8:
                num_min += 1
        return num_min