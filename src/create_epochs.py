import mne
import numpy as np
import copy

def parse_bdf(BDF_txt):
    '''Do not include spaces in the bin names, e.g., LVF Grammatical Correct, for it will cause parsing errors - am working on it.
       The bins in BDF must be mutually exclusive.
    '''
    f1 = open(BDF_txt)
    f2 = f1.read().split()
    f1.close()
    bin_labels = [f2[2+4*i] for i in range(int((len(f2))/4))]
    
    bins = {}
    for i,x in enumerate(bin_labels):
        bins[str(i+1)] = x      
    return bins


def parse_elist(elist_txt):
    f1 = open(elist_txt)
    f2 = f1.readlines()
    f1.close

    row = 0
    while 1:
        if f2[row][0] == '1': break
        row += 1
    
    lines = [i.split() for i in f2[row:]]
    return lines


def epoching(eeglab_raw, eeglab_epochs, BDF_txt, elist_txt):
    bins, lines = parse_bdf(BDF_txt), parse_elist(elist_txt)

    annot = eeglab_raw.annotations
    items = {}
    for j, key in enumerate(annot[0].keys()):
        items[key] = []
    for i in range(len(annot)):
        for j, key in enumerate(annot[i].keys()):
            items[key].append(annot[i][key])
        
    items['description'] = [bins[lines[i][11][0]] if lines[i][11][0]!=']' and int(lines[i][8])==0 else x for i,x in enumerate(items['description'])]

    new_annot = mne.Annotations(np.array(items['onset'], dtype=object),
                            np.array(items['duration'], dtype=object),
                            np.array(items['description'], dtype=object), orig_time=None, ch_names=None)
    raw = eeglab_raw.copy().set_annotations(new_annot)

    events, event_id = mne.events_from_annotations(raw)
    
    old_event_id = copy.deepcopy(event_id)
    event_id = {}
    for v in bins.values():
        event_id[v] = old_event_id[v]

    events = np.array([i for i in events if i[2] in [old_event_id[v] for v in bins.values()]])
    
    # Question: How does MNE know tmax, i.e., epoch end time? (Hint: Numpy.ndarray.shape)
    epochs = mne.EpochsArray(data=eeglab_epochs.get_data(), info=eeglab_epochs.info, events=events, tmin=-0.1, event_id=event_id)
    return epochs
