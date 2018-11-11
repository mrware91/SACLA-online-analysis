#!/bin/bash
cd qtDesigner/

pyuic5 availableDetectors.ui -o ../availableDetectors_ui.py
pyuic5 roi_set.ui -o ../roi_set_ui.py
pyuic5 roiSetter.ui -o ../roiSetter_ui.py

cd ..
