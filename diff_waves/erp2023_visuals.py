import os
import mne
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import namedtuple


def parse_bdf(bdf_txt):
    f1 = open(bdf_txt, encoding='utf-8')
    f2 = f1.read().split()
    f1.close()
    bin_labels = [f2[2+4*i] for i in range(int((len(f2))/4))]
    
    bins = {}
    for i,x in enumerate(bin_labels):
        bins[x] = i
    return bins
    

def align_bindata_files(bins, prefix, path, end=-5, end_except=-4):
    start, end, end_except = len(prefix), -len(' .txt'), -len('.txt')
    files_orig = [[f for f in fs if f.startswith(prefix)] for root, dirs, fs in os.walk(path, topdown=True)][0]
    files = [None]*len(bins)
    for f in files_orig:
        try:
            files[bins[f[start:end]]] = f  # 10 and -5 depend on the file names
        except KeyError:
            files[bins[f[start:end_except]]] = f  # 10 and -4 depend on the file names
    return files
    

Evoked_Wrapper = namedtuple('Evoked_Wrapper',
                            ['evokeds','info','data','bins','ch_names','tmin','tmax'])


def evoked_wrapper_from_data(bins, path, files, tmin, info, col_to_drop=['time','Unnamed: 35'], sep='	', resample=False,
                             disp=None):
    
    print(f'Dropping columns {col_to_drop}\n')
    evokeds, data = [None]*len(files), np.empty((len(files)), dtype=np.ndarray)
    os.chdir(path)
    dfs = []
    for i, f in enumerate(files):
        try:
            df = pd.read_csv(f, sep=sep).drop(columns=col_to_drop)
            eeglab_data = df.to_numpy().transpose()
            if resample == True: eeglab_data = mne.filter.resample(eeglab_data, up=1000/info['sfreq'])
            data[i] = eeglab_data
            dfs.append(df)
        except ValueError:
            try:
                eeglab_data = np.empty(eeglab_data.shape)
                data[i] = eeglab_data
                dfs.append(pd.DataFrame(data=None, index=None, columns=df.columns))
            except UnboundLocalError:
                dfs.append(None)
        try:
            evokeds[i] = mne.EvokedArray(data=eeglab_data, info=info, tmin=tmin)
        except UnboundLocalError:
            pass

    if evokeds[0] == None:
        i = 0
        shape = (0,0)
        while 1:
            if evokeds[i] != None:
                shape = data[i].shape
                break
            i += 1

        eeglab_data = np.empty(shape)
        null_df = pd.DataFrame(data=None, index=None, columns=info.ch_names)
        null_EvokedArray = mne.EvokedArray(data=eeglab_data, info=info, tmin=tmin)
        evokeds = [j if j != None else null_EvokedArray for j in evokeds]
        data = np.array([j if type(j) != type(None) else eeglab_data for j in data])
        dfs = [j if type(j) != type(None) else null_df for j in dfs]
              
    os.chdir('..')
    print(f'''Your bin data text files give {data[0].shape[0]} channels x {data[0].shape[1]} time points.
              (Note that the time points are the resampled time points if resampling is applied.)
              Please check if the dimension is correct...\n''')
    
    if disp != None:
        for i in disp:
            if str(i)[-1] == '1': num = str(i) + 'st'
            elif str(i)[-1] == '2': num = str(i) + 'nd'
            elif str(i)[-1] == '3': num = str(i) + 'rd'
            else: num = str(i) + 'th'
            print(f'Displaying the data file of your {num} bin in pandas.DataFrame format:\n')
            display(dfs[i-1]) if not dfs[i-1].empty else print("Ooops! You've got an empty DataFrame!\n\n")

    evoked_wrapper = Evoked_Wrapper(evokeds, info, data, bins,
                                    evokeds[0].ch_names,
                                    int(tmin*1000),int(data[0].shape[1]*1000/info['sfreq'])+int(tmin*1000))
    return evoked_wrapper


def my_plots(evoked_wrapper, layout=None, pos_dict=None, xlabel_pos=None, ylabel_pos=None,
             ch_to_plot=[], bins_to_plot=[], linestyles=[], colors=[],
             nrows=0, ncols=0, figsize=(0,0), xlim=(0,0), ylim=(0,0), xticks=[], yticks=[],
             loc='', borderpad=None, bbox_to_anchor=[],
             pad=1.08, save=False, fname=None):
    
    evokeds, info, data, bins, ch_names, tmin, tmax = evoked_wrapper
    N = data[0].shape[1]
    
    ch_dict = {}
    for i, x in enumerate(ch_names):
        ch_dict[x] = i

    t = [i for i in range(1, N+1)]
    actual_xticks = [(i-tmin)*N/(tmax-tmin) for i in xticks]

    if layout == 'Classic ERP':
        figure, axes = plt.subplots(nrows,ncols, figsize=figsize, sharey=True)
        for ax in axes.copy().flatten()[len(ch_to_plot):]:
            ax.remove()
        
        for ax, ch in zip(axes.copy().flatten()[0:len(ch_to_plot)], ch_to_plot):
            for i, x in enumerate(bins_to_plot):
                ax.plot(t, data[bins[x]][ch_dict[ch]],
                        linestyle=linestyles[i], color=colors[i], label=x)
            ax.axvline(x=abs(tmin)/(tmax-tmin)*N, color='black', linewidth=0.5)
            ax.axhline(y=0, color='black', linewidth=0.5)
            ax.set_title(ch)
            ax.set_xlabel('Time (ms)') # xlabel fontsize and labelpad not customized yet
            ax.set_xlim((xlim[0]-tmin)*N/(tmax-tmin), (xlim[1]-tmin)*N/(tmax-tmin)) 
            ax.set_xticks(actual_xticks, labels=xticks)
            ax.set_ylabel('µV') # ylabel fontsize and labelpad not customized yet
            ax.set_ylim(ylim[0], ylim[1])
            ax.set_yticks(yticks)
            ax.invert_yaxis()
            ax.yaxis.set_tick_params(labelbottom=True) # yticks label fontsize not customized yet
            hdl, lbl = ax.get_legend_handles_labels()
        figure.legend(hdl, lbl, loc=loc, borderpad=borderpad, bbox_to_anchor=bbox_to_anchor)
        figure.tight_layout(pad=pad)

    elif layout == 'Topo':
        keys, vals = list(pos_dict.keys()), list(pos_dict.values())

        figure, axes = plt.subplots(nrows, ncols, figsize=figsize, sharey=True)
        if xlabel_pos == None: xlabel_pos = (ncols-1)*nrows + int(ncols/2)
        if ylabel_pos == None: ylabel_pos = ncols*int(nrows/2)
        for (m,n), ax in np.ndenumerate(axes):
            if m*ncols+n == xlabel_pos: ax.set_xlabel('Time (ms)', fontsize=30, labelpad=35.0) # xlabel fontsize and labelpad not customized yet
            if m*ncols+n == ylabel_pos: ax.set_ylabel('µV', fontsize=30, labelpad=35.0) # ylabel fontsize and labelpad not customized yet
            try:
                if keys[vals.index(m*ncols+n)] not in ch_to_plot: ax.remove()
            except ValueError:
                ax.remove()
        
        for ch in ch_to_plot:
            ax = plt.subplot(nrows, ncols, pos_dict[ch]+1)
            for i, x in enumerate(bins_to_plot):
                ax.plot(t, data[bins[x]][ch_dict[ch]], linestyle=linestyles[i], color=colors[i], label=x)
            ax.axvline(x=abs(tmin)/(tmax-tmin)*N, color='black', linewidth=0.5)
            ax.axhline(y=0, color='black', linewidth=0.5)
            ax.set_title(ch, fontsize=40) # title fontsize not customized yet
            ax.set_xlim((xlim[0]-tmin)*N/(tmax-tmin), (xlim[1]-tmin)*N/(tmax-tmin))  
            ax.set_xticks(actual_xticks, labels=xticks)
            ax.set_ylim(ylim[0], ylim[1])
            ax.set_yticks(yticks)
            ax.invert_yaxis()  # negative up
            ax.yaxis.set_tick_params(labelbottom=True, labelsize=20)  # xticks label fontsize not customized yet
            ax.xaxis.set_tick_params(labelbottom=True, labelsize=20)  # yticks label fontsize not customized yet
            hdl, lbl = ax.get_legend_handles_labels()
        figure.legend(hdl, lbl, loc=loc, bbox_to_anchor=bbox_to_anchor, fontsize=45, borderpad=borderpad)
        figure.tight_layout(pad=pad)

    else:
        print("layout must be either 'Classic ERP' or 'Topo'!")
    
    if save == True:
        try: figure.savefig(fname)
        except AttributeError: print('Plot not saved... Please provide a valid file name to save the plot!')
        except UnboundLocalError: pass
        
    plt.show() 


def create_bin_op_evoked_wrapper(evoked_wrapper, bin_op_weights={}, new_binlabels=[]): # bin_op_weights is a dictionary
    evokeds, info, data, bins, ch_names, tmin, tmax = evoked_wrapper
    
    bin_op = [mne.combine_evoked([evokeds[bins[k.split(';')[i]]] for i in range(len(k.split(';')))], weights=v)
              for k,v in bin_op_weights.items()]
    
    data = np.empty(len(bin_op), dtype=object)
    for i,x in enumerate(bin_op):
        data[i] = x.get_data()

    new_bins = {}
    for i,x in enumerate(new_binlabels):
        new_bins[x] = i

    bin_op_evoked_wrapper = Evoked_Wrapper(bin_op, info, data, new_bins, evoked_wrapper.ch_names,
                                           evoked_wrapper.tmin, evoked_wrapper.tmax)
    return bin_op_evoked_wrapper


def create_contra_ipsi_evoked_wrapper(evoked_wrapper, bins_to_compare=[], groups={}):
    evokeds, info, data, bins, ch_names, tmin, tmax = evoked_wrapper

    contra_ipsi_evokeds = [mne.channels.combine_channels(evokeds[bins[bins_to_compare[i]]], 
                                                     groups=groups,
                                           method=lambda data: data[0]-data[1]) for i in range(len(bins_to_compare))]
    data = np.empty(len(contra_ipsi_evokeds), dtype=object)
    for i,x in enumerate(contra_ipsi_evokeds):
        data[i] = x.get_data()

    new_bins = {}
    for i,x in enumerate(bins_to_compare):
        new_bins[x] = i

    contra_ipsi_evoked_wrapper = Evoked_Wrapper(contra_ipsi_evokeds, info, data, new_bins, 
                                               list(groups.keys()), tmin, tmax)
    return contra_ipsi_evoked_wrapper


def plot_nice_topo(evoked_wrapper, drop_eog=True, bin_to_plot=None, times=[], nrows=None, ncols=None,
                   figsize=(0,0), time_fontsize=10, cbar_fontsize=7.5, vlim=(-10,10),
                   cbar_xstart=1, cbar_width=0.01, cbar_ystart=0.475, cbar_height=0.1,
                   title='Name Me... Please ><', title_x=0.5, title_y=0.675, title_fontsize=20, pad=1.08):
    # times is a list of tuples
    evokeds, info, data, bins, ch_names, tmin, tmax = evoked_wrapper
    if drop_eog == True:
        new_evokeds = [i.pick('eeg') for i in evokeds]
        new_data = np.empty(len(bins), dtype=object)
        for i in range(len(bins)):
            new_data[i] = evokeds[i].get_data()
        new_evoked_wrapper = Evoked_Wrapper(new_evokeds, new_evokeds[0].info, new_data, bins,
                                            new_evokeds[0].ch_names, tmin, tmax)
        evokeds, info, data, bins, ch_names, tmin, tmax = new_evoked_wrapper
          
    s = info['sfreq']/1000
    means = [np.mean(data[bins[bin_to_plot]][:,round((i[0]-tmin)*s):round((i[1]-tmin)*s)], axis=1) for i in times]
    if nrows == ncols == None:
        print(f'Number of rows and columns not set... Defaulting to 1 row, {len(times)} column(s)\n\n')
        nrows, ncols = 1, len(times)
    figure, axes = plt.subplots(nrows,ncols, figsize=figsize)
    for ax, (i,m) in zip(axes.copy().flatten(), enumerate(means)):
        ax.set_title(str(times[i][0])+'ms - '+str(times[i][1])+'ms', fontsize=time_fontsize)
        if not all(np.isnan(m)):
            im,cm = mne.viz.plot_topomap(m, pos=info, axes=ax, cmap='RdBu_r', vlim=vlim, show=False)
        else:
            ax.remove()
            print(f'Not enough sampling points to distinguish between {times[i][0]}ms and {times[i][1]}ms!\n\n')
    cbar_ax = figure.add_axes([cbar_xstart, cbar_ystart, cbar_width, cbar_height])
    clb = figure.colorbar(im, cax=cbar_ax)
    clb.ax.set_title('μV',fontsize=cbar_fontsize)
    figure.suptitle(title, x=title_x, y=title_y, fontsize=title_fontsize)
    figure.tight_layout(pad=pad)