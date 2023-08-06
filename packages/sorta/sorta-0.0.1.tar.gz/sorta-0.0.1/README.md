# sorta
Get rid of clutter in your directories. Sorta organizes your files by moving them to different folders based on their filetype and extensions.

We tend to download files on our PC's very often and usually this tends to pile up and before you know it, your downloads folder turns into a messy room. Or, you might just like to be organized and have a nice looking desktop. Sorta will take care of this for you by moving your notes, documents, music, images and videos into categorized folders.

It then takes this a step further by creating subfolders that stores files with the same extension.

## Installation
```bash
$ pip install sorta
```
<br>

### Usage
**Basic (Organizes your Desktop, Documents and Download directories)**
```bash
$ sorta
```
<br>

**Clean up a single specified directory**
```bash
$ sorta -d
Enter directory:
```
<br>

**Allow sorta to run at intervals (note that in order to run Sorta in the background, you'll have to run a daemon command or your system's equivalent with Sorta along with the specified arguments(see below) as the process). Here is an example of running Sorta indefinitely, allowing it to clean up your directories periodically every 15 minutes.**
```bash
$ sorta -b -i 15
```

<br>
<br>

## Command Line Arguments
```text
usage: sorta [-h] [-b] [-d] [-i INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  -b, --background      Run sorta indefinitely
  -d, --directory       Run sorta on a single directory
  -i INTERVAL, --interval INTERVAL
                        how frequently you want to action to run in minutes
```