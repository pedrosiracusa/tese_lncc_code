
# coding: utf-8

# In[3]:

import paths


# In[9]:

import pandas as pd
import pickle


# In[5]:

dsetPath = '/home/pedro/datasets/ub_herbarium/occurrence.txt'
cols=['recordedBy','scientificName','taxonRank','kingdom','phylum','class','order','family','genus','species',
      'countryCode','stateProvince', 'rightsHolder', 'repatriated', 'occurrenceRemarks', 'eventDate']
occs = pd.read_table(dsetPath,usecols=cols,low_memory=False)
occs = occs[occs['recordedBy'].notnull()]
occs = occs[occs['scientificName'].notnull()]
occs = occs[occs['species'].notnull()]


# In[6]:

# Names Atomization
from caryocar.cleaning import NamesAtomizer,namesFromString

names_replaces_file = '/home/pedro/caryocar/caryocar/cleaning/data/ub_collectors_replaces.json'
na = NamesAtomizer(atomizeOp=namesFromString)
na.read_replaces(names_replaces_file)
occs['recordedBy_atomized']=na.atomize(occs['recordedBy'])

# Names Map
from caryocar.cleaning import normalize,read_NamesMap_fromJson
collectors_names = list(set( n for n,st,num in na.getCachedNames()))


nm = read_NamesMap_fromJson('/home/pedro/caryocar/caryocar/cleaning/data/ub_namesmap.json',
                             normalizationFunc=normalize)
nm.addNames(collectors_names)

# Names index
from caryocar.cleaning import getNamesIndexes
ni = getNamesIndexes(occs, 'recordedBy_atomized',namesMap=nm.getMap())


# ### Build SCN

# In[7]:

from caryocar.models import SpeciesCollectorsNetwork

scn = SpeciesCollectorsNetwork(species=occs['species'],collectors=occs['recordedBy_atomized'],namesMap=nm)

cols_to_filter = ['','ignorado','ilegivel','incognito','etal']
scn.remove_nodes_from(cols_to_filter)


# ### Build CWN

# In[8]:

from caryocar.models import CoworkingNetwork

cwn = CoworkingNetwork(cliques=occs['recordedBy_atomized'],namesMap=nm)

cols_to_filter = ['','ignorado','ilegivel','incognito','etal']
cwn.remove_nodes_from(cols_to_filter)


# ---
