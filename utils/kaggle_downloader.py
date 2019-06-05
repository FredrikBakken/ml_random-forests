''' Kaggle Downloader
The Kaggle Downloader is a tiny script for downloading and extracting
dataset files for Kaggle competitions. It is designed to be as universal
as possible, to work for "all" use cases.

@author Fredrik Bakken <Fredrik.Bakken@gmail.com>

How to execute the script:
python kaggle_downloader.py -c <defined-competition> -a <kaggle-api-download> -e <extract-all>

-c | Pre-defined competitions includes: 'bulldozers' and 'titanic'
-a | Use the Kaggle API, e.g. 'kaggle competitions download -c <dataset-name>'
-e | Extract all zipped files? Must be integer: 0 = yes, 1 = no (default = 0 = yes)
'''

# TODO:
# - Check if competition files have been downloaded already
# - Extract competition files (.zip) and move the zipped files to "source_files" directory

# Library imports
from os import mkdir, chdir
from sys import exit
from zipfile import ZipFile
from os.path import exists
from argparse import ArgumentParser
from subprocess import Popen, PIPE, STDOUT


# Pre-defined Kaggle competitions
competitions = {
    'bulldozers':   'kaggle competitions download -c bluebook-for-bulldozers',
    'titanic':      'kaggle competitions download -c titanic',
}


# Initialize global variables
data_dir = '../data/'
kaggle_api_cmd = 'kaggle competitions download -c'


# Check if input arguments are valid
def inputValidator(competition=None, api=None, extract=0):
    if ((competition != None) and (api != None)):
        return False
    elif ((extract == 0 or extract == 1) and (api == None) and (competition in competitions.keys())):
        return True
    elif ((extract == 0 or extract == 1) and (api != None) and (kaggle_api_cmd in api) and (competition == None)):
        return True

    return False


# Initialize the set up of project directories
def setUpDirectories(competition=None, api=None):
    # Root directory for holding all resource files
    if (exists(data_dir) == False):
        mkdir(data_dir)
    
    # Initialize the root directory
    root_dir = ''
    
    # Create current competition directory and set new root
    if ((competition != None) and (competition in competitions.keys())):
        root_dir = data_dir + competition + '/'
    elif (api != None):
        api_dir = api.replace(kaggle_api_cmd, '').replace(' ', '')
        root_dir = data_dir + api_dir + '/'
    
    # Competition directory for holding specified compeition files
    if (exists(root_dir) == False):
        mkdir(root_dir)
    
    # Set the root directory for current execution
    chdir(root_dir)
    
    # Executed without errors
    return True


# Download the Kaggle competition files
def downloadKaggleFiles(competition=None, api=None):
    # Initialize download command
    download_cmd = ''

    # Specify the download command
    if (competition != None):
        download_cmd = competitions[competition]
    elif (api != None):
        download_cmd = api
    
    # Download Kaggle compeition files
    proc = Popen(download_cmd, stdin = PIPE, stdout = PIPE)
    stdout, stderr = proc.communicate(bytes(download_cmd, 'utf-8'))

    # Check if user has joined the Kaggle competition
    if ('403 - Forbidden' in str(stdout)):
        exit("Before you can download the competition files from Kaggle, you need to 'Join Competition'.")

    # Print download output
    print(stdout)

    # Executed without errors
    return True


# Extract all the downloaded competition files
def extractFiles(competition=None, api=None):
    print('TODO')


# Main application functionalities
def main(competition=None, api=None, extract=0):
    # Setup necessary directories
    dir_success = setUpDirectories(competition, api)

    # If directory set up was successful
    if (dir_success):
        # Download Kaggle competition files
        download_success = downloadKaggleFiles(competition, api)

        # If successful download of competition files
        if (download_success and extract == 0):
            extractFiles(competition, api)


if __name__ == '__main__':
    # Initialize the input ArgumentParser
    parser = ArgumentParser(
        description='Parameters for specifying which Kaggle competition to download and extract.')
    
    # Add arguments to ArgumentParser
    parser.add_argument(
        '-competition', metavar='-c', type=str,
        help='Download pre-defined competition.'
    )
    parser.add_argument('-api', metavar='-a', type=str,
        help='Download competition files that has not been pre-defined.'
    )
    parser.add_argument(
        '-extract', metavar='-e', type=int,
        help='Do you want to extract all the downloaded competition files? (0 = yes, 1 = no)'
    )
    
    # Parse the input arguments
    args = parser.parse_args()

    # Set extract to default values (0 = yes)
    if (args.extract == None):
        args.extract = 0

    # Validate user inputs
    valid = inputValidator(competition=args.competition, api=args.api, extract=args.extract)

    # Only continue execution if input is valid
    if (valid):
        main(competition=args.competition, api=args.api, extract=args.extract)
    else:
        exit('Your input arguments are invalid, please check your execution arguments.')
