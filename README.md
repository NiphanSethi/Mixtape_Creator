# Mixtape Creator

## Project Overview

The application downloads a list of songs from YouTube to a new directory on your local machine. The list of songs must be stored in a text file, where each line in the file indicates the artist and the song name. This is passed as an input argument, along with the name of a new directory (the mixtape title) and its path. The application outputs this new directory containing the list of songs as mp3 files. Songs that failed to download are written to a separate text file entitled “Unsuccessful_Downloads.txt” in the directory itself. A GUI has been created to make these steps intuitive for users.

<em>Application built using Python 3.8</em>

## Table of Contents

1. [Python Libraries and Packages Required](#python-libraries-and-packages-required)
2. [Formatting the List of Songs](#formatting-the-list-of-songs)

## Python Libraries and Packages Required

* tkinter 
* Pillow
* urllib
* pytube
* moviepy

## Formatting the List of Songs

Each line of the file containing the list of songs must be in the format “artist_name : song_name”. The following image shows an example of a valid list of songs:



