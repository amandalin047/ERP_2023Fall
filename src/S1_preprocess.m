function processing1 = S1_preprocess(subj_name,folder_path)

data_name = [subj_name '.set'];
data_path = [folder_path '/'];
 
% naming 
name1 = [subj_name '_reref.set'];
name2 = [subj_name '_reref_be.set'];
name3 = [subj_name '_reref_be_filt.set'];
name4 = [subj_name '_reref_be_filt_auto.set'];
    
% load set file
EEG = pop_loadset('filename',data_name,'filepath',data_path);
EEG = eeg_checkset( EEG );
    
% rereference 
EEG = pop_eegchanoperator( EEG, [folder_path '/' 'S1_chrereference.txt']);
EEG = eeg_checkset( EEG );
EEG = pop_saveset( EEG, 'filename',name1,'filepath',data_path);
    
% create eventlist
EEG  = pop_creabasiceventlist( EEG , 'AlphanumericCleaning', 'on', 'Eventlist', [data_path subj_name '_elist.txt'], 'Newboundary', { -99 }, 'Stringboundary', { 'boundary' }, 'Warning', 'on' );

% assign bins 
EEG = pop_binlister( EEG , 'BDF', [folder_path '/' 'BDF.txt'], 'ExportEL', [data_path subj_name '_elist.txt'], 'ImportEL', 'no', 'Saveas', 'on', 'SendEL2', 'EEG&Text', 'UpdateEEG', 'on', 'Warning', 'on' );
EEG = eeg_checkset( EEG );
    
% epoch 
EEG = pop_epochbin( EEG , [-100.0  1000.0],  'pre');
EEG = eeg_checkset( EEG );
EEG = pop_saveset( EEG, 'filename',name2,'filepath',data_path);
   
% low-pass filter
EEG  = pop_basicfilter( EEG,  1:34 , 'Boundary', 'boundary', 'Cutoff',  30, 'Design', 'butter', 'Filter', 'lowpass', 'Order',...
  2 );
EEG = eeg_checkset( EEG );
EEG = pop_saveset( EEG, 'filename',name3,'filepath',data_path);
    
% auto artifact detection_VEOG 
EEG  = pop_artmwppth( EEG , 'Channel',  34, 'Flag', [ 1 2], 'Review', 'off', 'Threshold',  80, 'Twindow', [ -100 999], 'Windowsize',  200, 'Windowstep',  100 );
EEG = eeg_checkset( EEG );
    
% auto artifact detection_HEOG 
EEG = pop_artstep( EEG , 'Channel',  33, 'Flag', [ 1 3], 'Review', 'off', 'Threshold',  80, 'Twindow', [ -100 999], 'Windowsize',  100, 'Windowstep', 50  );
EEG = eeg_checkset( EEG );
    
% auto artifact detection_all channels 
EEG = pop_artextval( EEG , 'Channel',  1:34, 'Flag', [ 1 4], 'Review', 'off', 'Threshold', [ -100 100], 'Twindow', [ -100 999] );
EEG = eeg_checkset( EEG );
   
% import channel location file 
EEG = pop_chanedit(EEG, 'lookup','C:\Users\amand\Downloads\eeglab_current\eeglab2022.1\plugins\dipfit\standard_BESA\standard-10-5-cap385.elp');
EEG = eeg_checkset( EEG );
    
% save set file after artifact detection
EEG = pop_saveset( EEG, 'filename',name4,'filepath',data_path);
EEG = eeg_checkset( EEG );