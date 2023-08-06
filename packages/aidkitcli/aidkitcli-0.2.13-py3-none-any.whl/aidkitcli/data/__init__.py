"""You can either upload a data set to aidkit or list the names of all the
uploaded data sets.

To upload a data set, it has to be compressed as a zip file. The zip file must
contain a folder with the future name of the data set and two subfolders
("INPUT" and "OUTPUT") with the corresponding csv files inside.

Once the data is structured adequately, run the following command to upload
the zip file:
``python -m aidkitcli.data --file <path_to_zip_file>``

To list all the uploaded data sets run the following command:
``python -m aidkitcli.data``
"""
