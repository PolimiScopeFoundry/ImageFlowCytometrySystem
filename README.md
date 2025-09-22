# ImageFlowCytometrySystem
ScopeFoundry compatible code for acquisition and realtime object detection and saving for imaging flow cytometry.

Detected regions of interest are saved into a h5 file, each roi into a different dataset, in order to make easy data loading with Fiji/ImageJ H5 file reader.


Current version is implemented using IDS cameras. Please clone PolimiScopeFoundry.IDS_ScopeFoundy into a sibling directory, in order to run this code.