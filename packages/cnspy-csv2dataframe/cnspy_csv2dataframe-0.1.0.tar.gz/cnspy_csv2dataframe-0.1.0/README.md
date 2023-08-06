# cnspy_csv2dataframe


The class [CSV2DataFrame](CSV2DataFrame.py) is intended to load [CSV-files](https://en.wikipedia.org/wiki/Comma-separated_values) into a `pandas.DataFrame`. The CSV files need to match known formats (defined by their header in the first line) according to those defined in the package [spatial_csv_formats]().
  
In case no format is specified, it tries to match the first line of the CSV-File with known headers from [spatial_csv_formats]() and loads the data in that format. 

There a some specialization of  [CSV2DataFrame](CSV2DataFrame.py) that support different operations on the data:
* [PoseCovCSV2DataFrame](PoseCovCSV2DataFrame.py)
* [PoseWithCov2DataFrame](PoseWithCov2DataFrame.py)
* [TimestampCSV2DataFrame](TimestampCSV2DataFrame.py)
* [TUMCSV2DataFrame](TUMCSV2DataFrame.py)

## Installation

Install the current code base from GitHub and pip install a link to that cloned copy
```
git clone https://gitlab.aau.at/aau-cns/py3_pkgs/csv2dataframe.git
cd csv2dataframe
pip install -e .
```

## Dependencies

* [numpy]()
* [pandas]()
* [cnspy_spatial_csv_formats](https://gitlab.aau.at/aau-cns/py3_pkgs/cnspy_spatial_csv_formats)
* [cnspy_numpy_utils](https://gitlab.aau.at/aau-cns/py3_pkgs/cnspy_numpy_utils)


## License


Software License Agreement (GNU GPLv3  License), refer to the LICENSE file.

*Sharing is caring!* - [Roland Jung](https://github.com/jungr-ait)
