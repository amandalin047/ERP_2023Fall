import mne
import numpy as np
# Matplotlib not used in this script (yet). Imported it because I wanted to wrap the plotting code into one single function in this script
import matplotlib.pyplot as plt
from copy import deepcopy
from re import findall

def parse_bdf(BDF_txt):
    '''Bin sizes should be in descending order: if Bin j ⊂ Bin i, then j > i (this is due to how an EventList is parsed in my algorithm).
    
       This epoching algorithm in Python only works when all the bins are either mutually exclusive or completely inclusive, i.e., 
       Let A, B be any two bins (A ≠ B), then their relationship must be one of the three:
           A ⊂ B
           B ⊂ A
           A ∩ B = ø

       If there are two non mutually exclusive bins where their intersection is non-empty, the algorithm will fail because in this case,
       it's impossible to correctly capture all the bins in one single mne.Epochs object; multiple instances of mne.Epochs would be needed as MNE only supports
       hierarchical bin structures. This MNE constraint probably has to do with Python dictionaries where one key can only be mapped to one value'''
    f1 = open(BDF_txt, encoding='utf-8')
    f2 = f1.read().split()
    f1.close()
    bin_labels = [f2[2+4*i] for i in range(int((len(f2))/4))]
    
    bins = {}
    for i,x in enumerate(bin_labels):
        bins[str(i+1)] = x      
    return bins


def parse_elist(elist_txt):
    f1 = open(elist_txt, encoding='utf-8')
    f2 = f1.readlines()
    f1.close

    row = 0
    while 1:
        if f2[row][0] == '1': break
        row += 1
    
    lines = [i.split() for i in f2[row:]]
    return lines


def epoching(eeglab_raw, eeglab_epochs, BDF_txt, elist_txt, tmin):
    bins, lines = parse_bdf(BDF_txt), parse_elist(elist_txt)

    annot = eeglab_raw.annotations
    items = {}
    for j, key in enumerate(annot[0].keys()):
        items[key] = []
    for i in range(len(annot)):
        for j, key in enumerate(annot[i].keys()):
            items[key].append(annot[i][key])
        
    items['description'] = [bins[findall(r'\d+', lines[i][-1])[0]] if lines[i][-1][0]!=']' and int(lines[i][8])==0 else x for i,x in enumerate(items['description'])]

    new_annot = mne.Annotations(np.array(items['onset'], dtype=object),
                            np.array(items['duration'], dtype=object),
                            np.array(items['description'], dtype=object), orig_time=None, ch_names=None)
    raw = deepcopy(eeglab_raw).set_annotations(new_annot)

    events, event_id = mne.events_from_annotations(raw)
    
    old_event_id = deepcopy(event_id)
    event_id = {}
    for v in bins.values():
        try:
            event_id[v] = old_event_id[v]
        except KeyError:
            pass
        
    events = np.array([i for i in events if i[2] in [old_event_id[v] for v in event_id.keys()]])
    
    # Question: How does MNE know tmax, i.e., epoch end time? (Hint: Numpy.ndarray.shape)
    epochs = mne.EpochsArray(data=eeglab_epochs.get_data(), info=eeglab_epochs.info, events=events, tmin=tmin, event_id=event_id)
    return epochs

