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
import chainfunctions, modelfunctions
#import dash_test



####### CHECK FOR DNA AND PROTEIN CHAINS

def check_type(input_chain):
    """
    Given a chain, it checks if it pertains to a DNA or protein structure.
    :param input_pdb_file:
    :return: structure object
    """

    atoms = set(Selection.unfold_entities(input_chain, "A"))
    for at in atoms:
        if at.id == "CA":
            return "Protein"
        elif at.id == "P":
            return "DNA"


################################
#    ACNUC CHAIN PROCESSING    #
################################

######### CHANGE C1 TO CA IN DNA CHAINS

def mutate_dna_chain(input_chain):
    """
    Given an input DNA chain, its C1' is transformed into a CA in order
    to make it a suitable input for the Superimposer and clashes functions.
    :param input_chain:
    :return:
    """

    if check_type(input_chain) == "Protein":
        pass
        return input_chain
    elif check_type(input_chain) == "DNA":
        print("Transforming DNA chains.....")
        new_chain = Chain.Chain(input_chain.id)
        for res in input_chain: # Should add copy of chain??? I don't really see why
            new_chain.add(res.copy()) # Shallow copy to actually copy the object attributes

        for res in new_chain:
            for atom in res:
                if atom.id == "C1'":
                    atom.id = "CA"

        return new_chain
    else:
        print("The chain introduce was not PROT nor ACNUC.")



############ GET ACNUC SEQUENCE FROM DNA CHAINS

def acnucseq_from_pdb(input_chain):
    acnucseq = ""
    for res in input_chain:
        if len(res.get_resname()) > 1:
            acnucseq += str(res.get_resname().rstrip()[2:])
        else:
            acnucseq += str(res.get_resname()).rstrip()

    return acnucseq


#___________________________________________________________________________________

### CHANGE CHAIN IDs

def change_chain_id(file, i, j):
    """
    Given a PDB MODEL object, the Chain IDs are converted from a letter format to a numeric format.
    It also checks for heteroatoms, and detaches them from the file. ¿Pero esto no funciona?
    :param:
    :return:
    """
    #struct_list = []
    #structure = PDBParser(PERMISSIVE=True, QUIET=True).get_structure(f"{j}", file)
    #chains = structure[0].get_chains()

    current_model = file
    current_model.id = j
    j += 1
    for chain in current_model:
        heteroatoms = list(filter(lambda x: x.id[0] != " ", chain.get_residues()))
        for heteroatom in heteroatoms:
            chain.detach_child(heteroatom.id)
        chain.id = i # replace chain ID with number
        i += 1 # i will keep increasing depending on the number of models
    return current_model


### STECHIOMETRY CHECK

"""
for key in newdict_prot.keys():
    current_chains = value_list[i]

    for chain in current_chains:
        print(chain)
        rmsd = functions.Superimpose_modified(key, chain)
        clash = functions.clashes(key, chain)
        if rmsd < 0.001 and clash == True:
            newdict_prot[key].remove(chain)
            print("CCH", current_chains)
    print(f"RESULTING CHAINS {current_chains}\n")


    for index, ch in enumerate(current_chains):
        for ch2 in current_chains:
            if ch.id != ch2.id:
                rmsd = functions.Superimpose_modified(ch, ch2)
                clash = functions.clashes(ch, ch2)
                print(f"Between {ch} and {ch2} the RMSD is {rmsd} and the CLASH status is {clash}")
                if rmsd < 0.001 and clash == True:
                    newdict_prot[key].remove(ch2)

    i+=1
for x, y in newdict_prot.items():
   print(x,y, len(newdict_prot.items()))
"""




########################## OTHER FUNCTIONS ###################################

class SelectNonHet(Select):
    """
    Select sub-class that saves a pdb file without heteroatoms.
    Not used for now.
    """
    def accepted_residues(self, residue):
        return 1 if residue.id[0] != " " else 0