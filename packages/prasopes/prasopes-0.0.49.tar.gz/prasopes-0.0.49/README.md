Prasopes
========

Prasopes is a free and open source Thermo/Finnigan .RAW spectra viewer. It is an implementation example of the rawFin library. Its limitation in means of the supported format scope is defined by the current developemnt state of the rawFin library.

## Installation

Install using the command bellow. Remove --user from command if You want to
install the application into system directory.

Linux:

```
python3 setup.py install --user
```

Windows:
Install python 3.x AS ADMINISTRATOR (!!), for simplicity I prefer to "install for all user" and check the checkbox to add python to PATH. Then run CMD (command prompt) AS ADMINISTATOR (!!) and type there:
```
pip install prasopes
pip install rawautoparams
```

you can then run Prasopes by typing <i>prasopes</i> to cmdline.

For Git version - download this git repository and:
```
pip install PyQt5
pip install PyQt5-sip
python3 setup.py install --user
```
PyQt5 and PyQt5-sip .egg packages are broken, if you will initiate installation by python3 setup.py the whole process will fail (at least true at 2018-09-16). If you install them by pip install valid .whl packages are downloaded instead and everything works as it should. If you accidentaly installed abovementioned .egg packages please remove them and proceed as stated above.


Mac:
Not tested yet, please report.

## Usage

Execute as: `prasopes [<SPECTRUM_FILE_PATH>]`

The `SPECTRUM_FILE_PATH` argument is optional, it is path to file with spectrum.
Use File -> Open or Ctrl+O to open a spectrum from GUI.

For exporting a spectrum use File -> Export or Ctrl+E.

 **experimental** monitoring of the spectrum during acqusition (Need File -> Settings temp setted-up properly)

### GUI control

  * **Doubleclick** resets active graph
  * **right button selection** selects timelapse in chromatogram and zoom the selection in mass spectrum
  * **left button** pan on x-axis
  * **scrolling** zoom on x-axis
  * **shift + scrolling** zoom on y-axis
  * **arrows** move selection in chromatogram left/right (need a right button selection existing first)

## Special tools

  * **experimental** TSQ zce: ZCE calculator for the Finnigan TSQ 7000, for details see help in the TSQ zce window.
  * **experimental** DRL: data extractor for the relative ion intensities in course of time. Now in testing state.

## Supported format
  * .raw (based on rawprasslib => limited machine scope)
  * in future: .mzml (will be next), .CDF
