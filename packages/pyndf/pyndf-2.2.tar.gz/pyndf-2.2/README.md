# Neurobit Data Format #

pyndf is a python library to read, write and create Neurobit Data Format (NDF) file/stream from raw PSG/ECG/HRV data. NDF is an open standard for communication with the Z3Score and NEO sleep scoring system (https://z3score.com). Instead of using polysomnography data or raw ECG data in European Data Format (EDF, https://en.wikipedia.org/wiki/European_Data_Format), the Z3Score system uses NDF files. NDF files are on an average 18X smaller than corresponding EDF files and can be as much as 100X smaller in some cases. This reduces data overhead significantly. The format does not allow any user identifiable information ensuring anonymity. The code is released under Neurobit EULA a copy of which can be requested from contact@neurobit.io. (c)-2020 Neurobit Technologies Pte Ltd 

### To Push new version to PIP ###
```
python setup.py sdist
twine upload dist/*
```

### To install ###
```console
git clone https://NeurobitTech@bitbucket.org/NeurobitTech/pyndf.git
cd pyndf
python setup.py install 
```
### dependencies ###
numpy, scikit-image, scipy, msgpack, msgpack_numpy, py-ecg-detectors, numba
```console
pip install numpy numba msgpack msgpack_numpy py-ecg-detectors scikit-image scipy 
```

### v2.1.0 ###

* This version adds the pressure channel to the PSG spec
* ECG storage technology has changed, we directly store ECG raw data @ 128Hz
* Previously ECG was compressed using wavelet based compression @ 100Hz
* there is a new key in the spec called revision which is set at 1

### v2.0.0 ###

* This version adds support for Z3Score-HRV API 
* This includes support for ECG, rr or nn interval based sleep staging

### v1.0.0 ###

* This version supports Z3Score API V4 
* This includes, EEG, ECG, EMG, Respiratory Channels and Leg EMG

### Important Functions

```python
    create_ndf_from_psg(data, sampling_rates, compressionbit=True, check_quality = True, age=None, gender=None))
```
  - Returns a NDF binary array from polysomnography data (this array can be saved in a file using save_ndf() or sent to the server)
  - data is a 12 channels cell array of 1Xsamples PSG data 
  - Order of data is: C3, C4, EOG-l, EOG-R, EMG-chin, EMG-left, 
  - EMG-right, ECG, Airflow, Thor, Abdo, SpO2 and Corresponding sampling rates as a numpy array
  - age and gender ('male' or 'female') are optional
  - a new dc-block filter is added now to EEG and ECG channels, other channels are not touched
  - compressionbit: is True (default) if compression is enabled, False otherwise
  - check_quality=True (default) does a quality check (will show warnings if check fails)


```python
    create_ndf_from_ecg(data, sampling_rate, compressionbit=True, age=None, gender=None))
```
  - Returns a NDF binary array from ECG data (this array can be saved in a file or sent to the server)
  - data is vector with raw ECG data 
  - sampling_rate is sampling rate for the ECG data
  - age and gender ('male' or 'female') are optional
  - compressionbit: is True (default) if compression is enabled, False otherwise
  - apply only light pre-processing if any
  - recommended sampling rate 128 Hz or more


```python
    create_ndf_from_rr(rr_loc, sampling_rate, duration=None, compressionbit=True, age=None, gender=None))
```
  - Returns a NDF binary array from rr peak locations (this array can be saved in a file or sent to the server)
  - rr_loc is integer vector with locations of rr peaks in terms of sample number
  - eg. rr = [128, 256, 512] @ sampling rate 128 implies rr-peaks are located at 1, 2 and 4 seconds
  - sampling_rate is sampling rate for the rr peak locations
  - age and gender ('male' or 'female') are optional
  - compressionbit: is True (default) if compression is enabled, False otherwise
  - Function will apply ADARRI to detect spurious r-peaks, Rebergen et al. 2018
  - recommended sampling rate 128 Hz or more
  - duration (in seconds) is optional, if not provided it is inferred from the rr_loc

  ```python
    create_ndf_from_nn(nn_loc, sampling_rate, duration=None, compressionbit=True, age=None, gender=None))
```
  - Returns a NDF binary array from nn peak locations (this array can be saved in a file or sent to the server)
  - function is same as create_ndf_from_rr, but no spurious r-peak detection is carried out.


  ```python 
    header = read_stream_header(stream)
```
 - Reads the header from a pyNDF I/O stream, it rewinds the reader after reading the stream
 - You are responsible for closing the stream

```python 
    save_ndf(file_name, ndf_bytearray)
```
 - save a NDF byte array to a file 


```python 
    header, payload = read_stream(stream, check_quality = True)
```
 - read the header and payload from a NDF I/O stream, it rewinds the reader after reading the stream
 - You are responsible for closing the stream

```python 
    header, payload = read_ndf(ndf_file, check_quality = True)
```
 - read the header and payload from a NDF file

```python 
    header = read_header(ndf_file)
```
 - read the header from a NDF file