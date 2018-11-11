# Online analysis suite for SACLA
Written by Matthew Ware (mrware@stanford.edu), Jordan O'Neal, Kathryn Ledbetter, and Takahiro Sato

This code is provided free of use. The only restriction is that its use must be acknowledged in any resulting publications and presentations.

## Operation
1. Access xu-bl3-anapc01 from the opcon computers via 
```shell
ssh -Y mrware@xu-bl3-anapc01
PW: c7PKCRW3
```
2. Run the Viewer gui. Located in /home/mrware/ANAPC/online/Viewer. Run 
```shell
python roiSetter_main.py
```
The viewer defines the ROIs. You must first define them here before they can be access by the data grabber.
3. Run the data Grabber gui. Located in /home/mrware/ANAPC/online/Grabber. Run
```shell
python dataGrabber_main.py
```
Add your desired detectors and ROIs then hit run.
4. Run the Plotter gui. Located in /home/mrware/ANAPC/online/Plotter/Code. Run
```shell
python plotter.py
```
It will automatically populate with the online variables you definied in the Grabber gui. You may combine these to your hearts content using the variable definitions (many variables may be combined in X and Y), the ON filter definition (must evaluate to Trues or Falses), the OFF filter definition (must evaluate to Trues or Falses). The ONs and OFFs may be substracted by clicking the toggle.

Enjoy.


## Summary of current features
* Acquires live data from user specified point detectors and regions-of-interest (ROIs) from large detectors, see dataSaverLoader/Database::dataSaver(...), into pickled pandas DataFrames at /dataSaverLoader/smallData
* Quickly loads the smallData pickles from (1) a specified run, (2) a specified range of events, or (3) live data stream using the N most recent events, see dataSaverLoader/Database::loadData(...)
* Quickly plots the data in a GUI using user specified input, see Plotter/Code/plotter.py
* Saves the plotted data and current GUI settings into Plotter/Code/Logs

## Planned features
* GUI for controlling the data acquisition, detector specification, and regions of interest
* roiGrabber library
* GUI for live viewing of MPCCD and defining ROIs
* dataScanner library for setting programmatic scans
* GUI for controlling dataScanner library
* Jupyter on opcon

## Installation of online analysis features
SACLA uses Python3.5 for its online data access libraries, dbpy and olpy. These are only available on the anapc clusters which may be ssh'd into from the opcon computers outside the hutches.
For compatibility, we muse then install Anaconda3 Version 4.2.0 on the anapc clusters. To do this,
1. Download the Anaconda3 V 4.2.0 installation for linux to your personal computer
2. File transfer the installation file (Anaconda3-4.2.0-Linux-x86_64.sh) to the hpc cluster (xhpcfep.hpc.spring8.or.jp). To do this, you must VPN into SACLA's network.
3. From the anapc node for your beamline (eg. xu-bl3-anapc01), grab the file from the hpc cluster using `scp username@xhpcfep.hpc.spring8.or.jp:/directory_to/Anaconda3-4.2.0-Linux-x86_64.sh .`
4. On the anapc terminal, run 
```shell
chmod x Anaconda3-4.2.0-Linux-x86_64.sh
./Anaconda3-4.2.0-Linux-x86_64.sh
```
5. Similarly copy this folder to the anapc cluster
## Installation of programmatic scan features
SACLA uses Python3.5 for its experimental control library, ecpy. This library is only available at the opcon clusters outside the hutches or in the ecpy simulation cluster. (Ask a staff scientist to be shown where these clusters are).

To install, simply create a personal directory on the opcon directory and use `scp username@xhpcfep.hpc.spring8.or.jp:/directory_to/these_files .` to copy the data.

## Editing and creating GUIs
Editing must be done directly in python for Plotter. For the other GUIs, their UI may be updated without breaking the codebase (Provided you do not remove any buttons, change their names, etc.). 
To make new or edit GUI windows use Qt Designer in the terminal window with

```shell
designer
```

To compile the ui files into a PyQt5 library, run


```shell
pyuic5 input.ui -o output.py
```

## dataSaverLoader

dataSaverLoader is the backend for the GUI environment. It uses the dbpy and olpy libraries provided on the anapc clusters at SACLA, eg. xu-bl3-anapc01 for beamline 3, to access the point detectors and the large detectors like the MPCCD.

**dataSaverLoader/Database.py:**
* dataSaver( ) is a class that starts a thread which acquires data from specified point detectors and regions of interest on large detectors. To use,
```python
dS = dataSaver( bl=3, refDet='some_det', ngrab=120 )
dS.setPointDetectors(pointDetectors) # format for pointDetectors is in code base
dS.setROIs(rois) # format for pointDetectors is in code base
dS.start() # starts gathering data

dS.request_Stop() # call when you want data acquisition to stop
```
* loadData(), loadRunData(), loadLiveData() will returns a pandas dataframe containing the data gathered by the dataSaver

**dataSaverLoader/saveDataInterface.ipynb:**
Jupyter notebook for defining point detectors and roi's programmatically.
To start a jupyter notebook, run the following in the terminal:
```shell
firefox &
jupyter notebook
```
Then navigate to the above notebook.

**dataSaverLoader/loadDataInterface.ipynb:**
Jupyter notebook for loading and analyzing point detectors and roi's programmatically.
To start a jupyter notebook, run the following in the terminal:
```shell
firefox &
jupyter notebook
```
Then navigate to the above notebook.

**dataSaverLoader/roiGrabber.ipynb:**
Jupyter notebook for loading, viewing, and choosing roi's programmatically.
To start a jupyter notebook, run the following in the terminal:
```shell
firefox &
jupyter notebook
```
Then navigate to the above notebook.

**dataSaverLoader/dummyDatabase.py:**
Defines a dummy version of the LoadData(...) function for debugging analysis programs.

**dataSaverLoader/smallData:**
Contains the generated smallData files from Database.py. These are saved as pickle files (.pkl) for quick access for plotting and analysis. Note that the .pkl files are not compatible with different versions of Python, so they must be opened with Python 3.5 as used at SACLA.

## Plotter

Plotter is a GUI that quickly pulls in data and plots based on user-specified input.  It can update continuously, select on run, or tag range.  It can generate scatter plots or 1/2D histograms, filter, and subtract background.

**plotter.py**
* Starts the GUI.  Runs the main window.  To use,
```python plotter.py
```

**dialog_plot_var.py/dialog_filter.py/dialog_filter_onoff.py**
Controls dialog boxes.

## Grabber

## largeDetectorViewer

## Scanner
