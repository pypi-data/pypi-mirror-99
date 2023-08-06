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
import inputfunctions, modelfunctions

#import dash_test


#### PAIRWISE ALIGNMENT BETWEEN TWO CHAINS

def chain_align(chain1, chain2):
    """Pairwise alignment between two chains.
    NOT USED FOR NOW.
    """
    ppb = PPBuilder()
    for pp in ppb.build_peptides(chain1):
        seq1 = pp.get_sequence()
        print(f"From {chain1} we get {seq1}")
    for pp in ppb.build_peptides(chain2):
        seq2 = pp.get_sequence()
        print(f"From {chain2} we get {seq2}")
    alignments = pw2.align.globalxx(seq1, seq2, score_only=True) # Only scores to save time
    min_length = max(len(seq1), len(seq2)) # Why min and not max?
    identity_perc = round(alignments / min_length, 2)
    print(f"Between {chain1} and {chain2} there is a {identity_perc}% of identity")
    if identity_perc > 0.95: # Should be modificable
        return chain1, chain2

################################
#      CHAIN PROCESSING        #
################################


def protein_interactions(dictmodels):
    """Gets all possible interactions given a list of pdb files. It computes the distance between chains and pairs the interacting
    ones. In order to interct they need to fullfill the following condition: at least 8 residues are found at a distanc of less than ess than 8A"""
    set_models = set()
    main_dict=dict()

    for model in dictmodels.values():
        for chain in model:
            set_models.add(chain)

    for ind, chain1 in enumerate(list(set_models)):
        main_dict[chain1]={}
        for chain2 in list(set_models)[ind+1:]:
            if chain1.get_id() != chain2.get_id():
                if chain2 not in main_dict:
                    main_dict[chain1][chain2]=get_distance(chain1, chain2)
    #print(main_dict)

    inter_list = []
    for k1,v1 in main_dict.items():
        for k2,v2 in v1.items():
            if v2 >= 8:
                if [k1, k2] not in inter_list:
                    inter_list.append([k1, k2])
    return(inter_list)

def redundant_pairs(interacting_pairs):
    redundant_pairs=[]
    print("BEFORE", interacting_pairs)
    for index, pair1 in enumerate(interacting_pairs):
        for pair2 in interacting_pairs[index+1:]:
            i=0
            for chain in pair2:
                id_perc=chain_align(pair1[0], chain)
                if id_perc > 0.95:
                    print("Superimposing")
                    rmsd, pair_moving_chain, pair_fixed_chain=Superimpose_pairs(pair1, pair2, i)

                    clash=clashes(pair_moving_chain, pair_fixed_chain)
                    #print(clash)
                    if rmsd < 0.0001 and clash == True:
                        interacting_pairs.remove(pair2)
                i+=1
    return(interacting_pairs)


###### GET CHAINS SIMILAR IN SEQUENCE

def similar_chains(input_model_dict, type):
    """
    Given an dictionary of PDB files as Keys, and their Structure objects as values, this function
    makes pairwise alignments between the chains, keeping only those with a 95% or higher
    similarity.
    """
    print("Looking for similar chains...")
    similar_chains = {}
    ppb = PPBuilder()
    model_list = list(input_model_dict.values())
    seq1 = ""
    seq2 = ""
    for index, model in enumerate(model_list):
        for chain1 in model:
            if inputfunctions.check_type(chain1) == type:
                #print(chain1, type)
                for model2 in model_list[index+1:]:
                    for chain2 in model2:
                        if inputfunctions.check_type(chain2) == type:
                            #print(chain2)

                            if type == "DNA":
                                seq1 = acnucseq_from_pdb(chain1)
                                seq2 = acnucseq_from_pdb(chain2)
                                alignments = pw2.align.globalxx(seq1, seq2, score_only=True)
                                min_length = max(len(seq1), len(seq2))
                                identity_perc = round(alignments / min_length, 2)
                                #print(identity_perc)
                                if identity_perc > 0.95:
                                    similar_chains.setdefault(chain2, chain1)


                            elif type == "Protein":
                                for pp1 in ppb.build_peptides(chain1):
                                    seq1 = pp1.get_sequence()
                                for pp2 in ppb.build_peptides(chain2):
                                    seq2 = pp2.get_sequence()
                                alignments = pw2.align.globalxx(seq1, seq2, score_only=True)
                                min_length = max(len(seq1), len(seq2))
                                identity_perc = round(alignments / min_length, 2)
                                #print(identity_perc)
                                if identity_perc > 0.95:
                                    similar_chains.setdefault(chain2, chain1)
    return similar_chains