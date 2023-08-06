### (V)oice (O)nset (T)ime
This package was made to easily compute voice onset time without any specialty equipment. All that's needed is a computer and a microphone!


### Getting Started
`pip install pyaudio`  --->  **Required**

`pip install votpy`

    import votpy
    # Create Detector variable
    det = Detector()
    # Make sure microphone is picking up a viable signal
    det.test_mic()
    # Record a single voice onset; print to csv
    det.record_vol(timout = 5)
    det.to_csv("file.csv")

### Inspired by [sebastiaan](https://forum.cogsci.nl/index.php?p=/discussion/1772/) and [Primusa](https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound)


### On Windows and can't install pyaudio? Try the below code:


- `pip install pipwin`
- `pipwin install pyaudio`