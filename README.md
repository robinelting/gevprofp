# Final Project Gevorderd Programmeren - dubieus.rar
Group name: dubieus.rar

In this GitHub repository you can find the Python script needed to align movie script and subtitles. We have tested our Python script on the Mission Impossible files and the files related to the movie 'It'.

## Program Information
This program aligns subtitles and scripts.

#### For each line of the script, the program adds:
* The corresponding tag (either S for scene boundary, M for meta-data, C for character name, N for scene description, and D for dialogue)
* The corresponding subtitle
* The corresponding timestamp to the subtitle

This will result in a CSV file with a table including all script lines and their corresponding tags, subtitles and timestamps.

## Contributors:

* Robin Elting
* Mark Bellman
* Eva Dyadko
* Pieter Jansma

## System requirements
To run this program, a few packages need to be installed:

### NLTK
1. Install NLTK:
   ```ruby
   pip install --user -U nltk
   ```

### PYSRT
1. Install PYSRT
   ```ruby
   sudo pip install pysrt
   ```

## Access files
You can access the files from this repository in two ways; downloading direct from GitHub or cloning the repository.

### Download
You can download the repository as follows:
1. Click the green `Code` button.
2. Select `Download ZIP`

A zip-file with all contents of this repository will be downloaded to your computer.

### Clone repository (Linux)
You can clone the repository as follows:
1. Go to the directory on your computer where you want to clone the repository to.
2. Type git clone and paste the URL of this repository:
   
   ```ruby
   https://github.com/robinelting/gevprofp
   ```
3. Press `Enter` to create your local clone.

## Run script
After you have downloaded the necessary files, you can run the script called `fp.py` as follows:
1. Run the following command
   ```ruby
   python3 finalproject.py SCRIPT SUBTITLES OUTPUTFILE
   ```
   Here you need to change `SCRIPT` into the .txt file with the movie script, `SUBTITLES` into the .srt file with the movie subtitles, and `OUTPUTFILE` into a desired output        .csv file.
2. With the Mission Impossible files, you would run the program as follows:
   ```ruby
   python3 finalproject.py mi.txt mi.srt output.csv
   ```

## Division of labor
In general we all worked together via Google Meet on this project. This means that we worked together on certain aspects of the project and that multiple persons worked on the same aspect of the project. However, the following shows a more specific division of labor for our Final Project:

* Robin Elting: Tagging movie scripts (tagger() function), generating output file, aligning scripts and subtitles (script_aligner() function)
* Mark Bellman: Preprocessing of text (subtitle_preprocessing() function), extracting timestamps and subtitles (subtitle_preprocessing() function), aligning scripts subtitles (script_aligner() function).
* Eva Dyadko: Creation of unit tests, aligning scripts and subtitles (script_aligner() function)
* Pieter Jansma: Aligning scripts and subtitles (script_aligner() function), extracting timestamps and subtitles (subtitle_preprocessing() function)
