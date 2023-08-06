
import sys
sys.path.append('/home/oth/anaconda3/lib/python3.8/site-packages')
sys.path.append('/Users/Maria/Desktop/Uni/sbi/SBI-Project/SBI_PYT/PPI_main') # Path to I_O_args script
#sys.path.append('/home/oth/BHS/PYT/1.project/dash_test.py')
import os, numpy, scipy
import parser as args
from Bio.PDB import *
from Bio.Seq import Seq
from Bio.PDB.PDBIO import PDBIO, Select
from Bio import pairwise2 as pw2
import inputfunctions, chainfunctions, modelfunctions
import time


sys.stderr.write("ARGPARSE OPTIONS:\n")
# Argument parsing functions

options = args.output_argparser() # Object that contains all argument parsing functions


############################################# INPUT PDBs

pdblist = args.check_infile_names(options.infile) # Checking correct file-naming

if options.verbose:
    print("Reading PDBs\n")


#for pdbfile in os.listdir(options.infile):
#    pdblist.append(str(options.infile+pdbfile)) # List of PDBs with their path


# Dictionary with files and their PDB models

i = 0
dictmodels = {}
for pairs in pdblist:
    dictmodels[pairs] = []
    parser = PDBParser(PERMISSIVE=True, QUIET=True)
    structure = parser.get_structure(f"Structure_{i}", pairs)
    model = structure[0]
    dictmodels[pairs] = model # Path+file as KEY, model object as VALUE
if options.verbose:
    print("FILE-MODEL dictionary successfully created.")



##### DNA, PROTEIN CHAINS CHECK
dna_chain_count = 0
prot_chain_count = 0
dnachainlist = []
for model in dictmodels.values():
    for chain in model:
        if inputfunctions.check_type(chain) == "Protein":
            prot_chain_count += 1
        elif inputfunctions.check_type(chain) == "DNA":
            dna_chain_count += 1
            dnachainlist.append(chain)

if options.verbose:
    print(f"There are {dna_chain_count} DNA chains and {prot_chain_count} protein chains")


### CHECKING FOR HETEROATOMS
hetatm_count = 0
for model in dictmodels.values():
    for chain in model:
        for res in chain:
            if res.id[0] != " ":
                hetatm_count += 1

if options.verbose:
    print(f"Number of heteroatoms: {hetatm_count}")




##### INPUT STECHIOMETRY FILE
if options.verbose:
    print(f"Reading stechiometry...")

stechio_dict = {}
stech = options.stechiometry
total_subunits = 0
i=0
for line in open(stech):
    letter = line.split(":")[0].rstrip()
    num = int(line.split(":")[1].rstrip())
    stechio_dict[i] = num
    i+=1
    total_subunits = sum(stechio_dict.values())

if options.verbose:
    print(f"The provided stechiometry is:")
    for id, count in stechio_dict.items():
        print(f"{id}\t{count}")
    print("\n")




#### CHANGING CHAIN IDs
total_models={}
i=0
j=0
for file, model in dictmodels.items():
    total_models[file] = inputfunctions.change_chain_id(model, i, j)
    i+=2
    j+=1

if options.verbose:
    print("Chain IDs have been converted from letters to numbers.\n")


    ##### TOTAL MODELS
    print(f"THESE ARE THE TOTAL MODELS WE HAVE:")
    for file, model in total_models.items():
        print(f"{file}\t{model}")
    print("\n")

    print(f"Within each model, we have the following chains:")
    for model in total_models.values():
        print(model, "-", [ch for ch in model.get_chains()])
    print("\n")



############################################# CHAIN PROCESSING
##### SIMILAR CHAINS

# Protein
similar_chains_prot = chainfunctions.similar_chains(total_models, "Protein")
# ACNUC
similar_chains_dna = chainfunctions.similar_chains(total_models, "DNA")

if options.verbose:
    print("Obtaining the SIMILAR CHAINS...")
    print(f"Similar PROTEIN chains: ")
    for x, y in similar_chains_prot.items():
        print(f"{x}\t{y}")
    print("\n")

    # ACNUC
    if dna_chain_count != 0:
        print(f"Similar ACNUC chains:")
        for x, y in similar_chains_dna.items():
            print(f"{x}\t{y}")
        print("\n")
    else:
        print("This structure does not have ACNUC chains.\n")


##### COMMON-UNIQUE CHAINS
# Proteins
stoich_set_prot = set(list(similar_chains_prot.values()))
newdict_prot = {}

for x in stoich_set_prot:
    newdict_prot[x.id] = []
    for keys, val in similar_chains_prot.items():
        if val.id == x.id and (keys.id != val.id):
            newdict_prot[x.id].append(keys.id)

if options.verbose:
    print("PROTEIN common-unique chains")
    for x, y in newdict_prot.items():
        print(f"UNIQUE CHAIN: {x}\tSIMILAR CHAINS: {y}")
    print("\n")


# DNA
if dna_chain_count != 0:
    stoich_set_dna = set(list(similar_chains_dna.values()))
    newdict_dna = {}

    for x in stoich_set_dna:
        newdict_dna[x] = []
        for keys, val in similar_chains_dna.items():
            if val.id == x.id and (keys.id != val.id):
                newdict_dna[x].append(keys)

    if options.verbose:
        print("DNA common-unique chains")
        for x, y in newdict_dna.items():
            print(f"UNIQUE CHAIN: {x}\tSIMILAR CHAINS: {y}")
        print("\n")



############################################# MODEL CONSTRUCTION

if options.verbose:
    print(f"\n############### MODEL CONSTRUCTION ############# \n")

new_model = Model.Model('X')
i = 0
new_model_stech = {}
keys_list = list(newdict_prot.keys())
value_list = list(newdict_prot.values())
listmodels = list(total_models.values())

# Iterating over the models

for idx, model in enumerate(listmodels):
    ch1 = [ch for ch in listmodels[0].get_chains() if ch not in [ch for ch in new_model.get_chains()]]
    for chain in ch1:
        if ch1[0] in keys_list or ch1[1] in keys_list: # Only introduce the ones that contain unique chains first
            new_model.add(chain)
            print(f"{chain} has been added to the model")
    print("Chain 1", ch1)
    for model2 in listmodels[idx+1:]:
        ch2 = [ch for ch in model2.get_chains()] # List of chains of the model that is going to be incorporated
        print("Chain 2", ch2)
        #print(newdict_prot[ch1[0].id])

        # Looking for the common chain, if there is any
        print("Looking for the common chains...")
        try:
            if ch2[0].id in newdict_prot[ch1[0].id] or ch2[1].id in newdict_prot[ch1[0].id]:
                common_chain1 = ch2[0]
                common_chain2 = ch1[0]
                print(common_chain1, common_chain2)
                rmsd = modelfunctions.Superimpose(model, model2, apply=True)
                clash = modelfunctions.clashes(model, model2, type="residue")
                # print(f"Between {key} and {chain} the RMSD is {rmsd} and the CLASH status is {clash}")
                print(rmsd, clash)
                if rmsd > 5:
                    try:
                        for chain in model2:
                            new_model.add(chain)
                        new_model_stech[key] += 1
                        print(f"###### This {chain} has been ADDED")
                    except:
                        pass
        except:
            pass






"""
# Then use the unique-common dict to build the model
for key in newdict_prot.keys():
    #print(f"\nFor unique chain {key}")
    try:
        new_model.add(key)
    except:
        pass
    new_model_stech[key] = 1
    current_chains = value_list[i]
    j = 0
    for chain in current_chains:
        key = functions.mutate_dna_chain(key)
        chain = functions.mutate_dna_chain(chain)
        rmsd = functions.Superimpose(key, chain)
        clash = functions.clashes(key, chain)
        #print(f"Between {key} and {chain} the RMSD is {rmsd} and the CLASH status is {clash}")
        if rmsd > 0.001 and clash == False:
            if chain.id not in [ch.id for ch in new_model.get_chains()]:
                try:
                    new_model.add(chain)
                    new_model_stech[key] += 1
                    print(f"###### This {chain} has been ADDED")
                except:
                    pass

    for index, ch in enumerate(current_chains):
        for ch2 in current_chains[index+1:]:
            rmsd = functions.Superimpose(ch, ch2)
            clash = functions.clashes(ch, ch2)
            #print(f"Between {ch} and {ch2} the RMSD is {rmsd} and the CLASH status is {clash}")
            if rmsd > 0.001 and clash == False:
                if ch.id not in [ch.id for ch in new_model.get_chains()]: # We don't need this?
                    try: # Added the try-except block again because it wasn't working with the last model
                        new_model.add(ch)
                        new_model_stech[key] += 1
                        print(f"###### This {ch} has been ADDED")
                    except:
                        pass

    i += 1
"""


# MODEL STECHIOMETRY
if options.verbose:
    print(f"\nNEW MODEL STECHIOMETRY:")
    for id, count in new_model_stech.items():
        print(f"{id.id}\t{count}")


new_model_chains = [ch for ch in new_model.get_chains()]

if options.verbose:
    print(f"NEW MODEL WITH:\n{len(new_model_chains)} CHAINS\nWHICH ARE: {new_model_chains}")


#### SAVING THE STRUCTURE
parser=PDBParser()
#model_structure=parser.get_structure(final_chains)
io = PDBIO()
io.set_structure(new_model)
model_name = (str(pdblist[0]).split("/")[-1]).split("_")[0]
# timestamp
model_out_path = options.outdir
t = time.localtime()
timestamp = time.strftime('%d%m%Y_%H:%M', t)

# Saving the structure
if len(new_model_chains) != 0:
    io.save(f"{model_out_path}/{model_name}_complex_{len(new_model_chains)}_chains_{timestamp}.pdb")

    if options.verbose:
        print(f"\nSaving the structure...\n")


chains = list(listmodels[0].get_chains())
chains2 = list(listmodels[1].get_chains())

print(chains, chains2)

clash_01 = modelfunctions.clashes(chains[0], chains2[1], type="residue")
print(clash_01)




# etc

#### DIFFERENT CHAINS
# Chains that are NOT present in similar chains
# These can NOT be superimposed. I don't see how could we include them
"""
if options.verbose:
    print(f"Looking for the different chains")

different_chains = []
for model in total_models.values():
    for chain in model:
        if chain not in similar_chains_prot.values() and chain not in similar_chains_prot.keys():
            different_chains.append(chain)

if options.verbose:
    print("These are the DIFFERENT CHAINS:")
    print(different_chains, "\n")

"""

"""

# First add the different chains
for chain in different_chains:
    new_model.add(chain) # No clash check??
    
    
unique_keys=set()
for index, key1 in enumerate(keys_list):
    for key2 in keys_list[index+1:]:
        clash = functions.clashes(key1, key2)
        if clash == False:
            unique_keys.add(key1)
print(unique_keys)

unique_dict={}
for key in unique_keys:
    unique_dict[key]=newdict_prot[key]
print(unique_dict.items())

value_list_prot = list(unique_dict.values())
"""