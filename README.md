# Final Project Gevorderd Programmeren - dubieus.rar
Group name: dubieus.rar

In this GitHub repository you can find the Python script needed to align movie script and subtitles.

## Program Information
#### For each subtitle, the program adds:
* The character name 
* The matching line of the script.

#### For each line of the script, the program adds:
* The M for Metadata
* S for Scene boundary
* N for Scene description
* C for Character name
* D for dialogue

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
   python3 fp.py SCRIPT SUBTITLES
   ```
   Here you need to change `SCRIPT` into the .txt file with the movie script and `SUBTITLES` into the    .srt file with the movie subtitles
2. With the Mission Impossible files, you would run the program as follows:
   ```ruby
   python3 fp.py mi.txt mi.srt
   ```

## Division of labor
The division of labor for our Final Project is as follows:

* Robin Elting: Tagging movie scripts (this includes the functions tagger() and dic_tagger())
* Mark Bellman: Preprocessing of text, extracting timestamps and subtitles, aligning subtitles.
* Eva Dyadko: Creation of unit tests
* Pieter Jansma: Aligning subtitles
