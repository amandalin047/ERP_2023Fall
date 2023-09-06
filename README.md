## macOS
### Pre-installed Python
Since most macOS computers come with Python pre-installed (please do not modify your mac's pre-installed Python as it would mess with your system), it's always a good practice to check which Python version you have on your device. Go to your terminal and type `python --version` which probably isn't 3.11.5. The steps below will install the latest Python release and a virtual environment for better package version/dependency management.

### Install Xcode Command Line Tools
Check if they're installed:
```
xcode-select --version
```
If they are, you'll get the corresponding version in your terminal output; if not, run
```
xcode-select --install
```
which will pop out a window asking you to install them. Click Install, and wait. You will then see a message display
> The software was installed.

Click Done, and type 
```
xcode-select -p
```
in the terminal, which should output
> /Library/Developer/CommandLineTools

### Install Homebrew
In the terminal, type
```
brew help
```
to see if Homebrew is installed on your mac. If an error occurs, it is not installed. Type the following command to install Homebrew:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
After installation, type
```
brew doctor
```
to check that everything's okay.

### Install `pyenv` via Homebrew 

After Homebrew has been installed, run the following lines **one line at a time** in the terminal to install Python 3.11.5 and the packages we'll be using in class, along with several others I find useful for data analysis:
```
brew update && brew upgrade
brew install pyenv
```

After installation, run
```
pyenv init
```
<img src="https://github.com/NTU-BLPLab/ERP_2023Fall/blob/installation/screenshots/screenshot1.png" alt="pyenv init" width=400>

and look at the terminal output carefully; follow the instruction there, i.e.,  copy and paste the listed lines to your corresponding files, which in my case are `~/.bashrc` and `~/.profile` as I'm running Ubuntu in Windows Subsystem for Linux. Remember to save, then _source_ the files or _close and restart_ your terminal for the changes to take effect. 
- 💡 If you've never modified such files and are lost at this step, feel free to screenshot what `pyenv init` outputs and [email me](https://docs.google.com/document/d/1JBO6eFAZ6MM8P9p1YiCILFfPHe5p0GV_/edit?usp=sharing&ouid=103533581234587701878&rtpof=true&sd=true) the picture.

## Python via `pyenv`
Now install Python 3.11.5 using pyenv (this may take a while):
```
pyenv install 3.11.5
```

Set Python to the newly installed version:
```
pyenv global 3.11.5
```

Type
```
which python
```
which should output something like 
> blahblahblah/.pyenv/shims/python

And typing
```
python --version
```
should get you the desired 3.11.5

### Python packages via PIP
Now type
```
pip3 list
```
to see the packages installed by pip, which in this case are probably just `pip` itself and `setuptools`. We want to install a package called `virtualenv` to create a virtual environment as mentioned in the beginning, so run
```
pip3 install virtualenv
```

After installation, create a new folder called `erpclass`, go to that folder, and create a virtual environment named `venv`. Execute the commands below one line at a time:
```
mkdir erpclass; cd erpclass
virtualenv venv
source venv/bin/activate
pip3 install jupyterlab mne pandas pingouin openpyxl flake8
```
- **[MNE](https://mne.tools/stable/index.html) is the Python package for reading, processing, analyzing, and plotting EEG/MEG data.**
- [Pandas](https://pandas.pydata.org/docs/) is a powerful library for data analysis amd manipulations in the form of `pandas.DataFrame`
- [Pingouin](https://pingouin-stats.org/build/html/index.html) is for for statistical analyses in Python (I find it more convenient tyan Statsmodels, which comes installed as a dependency with MNE.
- [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) is needed in order for Python to read from and qrite to Excel files.
    + Side note: Excel now accepts (or is about to accept) Python syntax and functions 😍
- [Flak8](https://flake8.pycqa.org/en/latest/) is basically Grammerly for Python.

After it's done, type `pip3 list` again. You should now see a long list of packages installed.

## Opening Jupyter Lab
No we're ready to open your Jupyter Lab! Type
```
jupyter lab
```
which will automatically open a browser tab (if it doesn't, copy and paste any one of the URLs, e.g., `http:/localhost:blahblahblah` into your browser search bar), and voila! There's your Jupyter Lab! Note also that you do not need the internet to run Jupyter; localhost refers to your device. 

Last step, open a Jupyter notebook and paste the following lines into the first cell, then hit Run:
```
import mne
import numpy as np
from platform import python_version
python_version()
```

### Deactivating virtual environments
To deactivate a virtual environment, simply type
```
deactivate
```
in the terminal. In addition, if you now type
```
pip3 list
```
after `venv` has been deactivated, you won't see any of the packages we just installed.
