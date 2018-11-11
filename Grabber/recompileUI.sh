#!/bin/bash
cd qtDesigner_files/

pyuic5 availablePDs.ui -o ../availablePDs_ui.py
pyuic5 availableROIs.ui -o ../availableROIs_ui.py
pyuic5 dataGrabber.ui -o ../dataGrabber_ui.py

cd ..
