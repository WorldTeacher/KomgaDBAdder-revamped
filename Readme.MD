# Welcome to the documentation of the KomgaDBAdder-revamped

This documentation describes the metadata injection process, and how to use it. The process is divided in two steps:

   1. Going though the database and creating a csv file with the title and the Series_ID
   2. Grabbing the metadata using the MangaDex API and writing it to the database

## Setup

1. Clone the repository using `git clone, or simply download the zip file and unzip it.
2. Add your database path to the settings.json file. (While you are there, you might want to change the age ratings, depending on your opinion)
3. Shutdown the Komga Server and make a backup of the database. (nothing should go wrong, but you should be careful)
4. Run the following command:

    ```
    python setup.py 
    ``` 
This will create the csv file that will be used later on.

5. Run the following command:

    ```
    python main.py
    ```
This will start the metadata-grabbing and write the metadata to the database.

## What will be written to the database
These are the fields that will be written to the database:

- Summary
- age rating, based on the available age ratings in the settings.json file
- Genres
- Tags
- Language, currently hardcoded to English, as I only have English titles in my database
- Status

Additional fields, like Writers, Inkers and Pencillers could be added in the future, if needed.


## What's this about the title_rename.csv file?

As I tested the functionality, I found that the titles from the database are not always the same as the titles from the website. This can eiter be because the Foldername is not the same as the title, or because MangaDex has a different naming scheme.

I have hardcoded a conversion from "&" to "and", as MangaDex mostly uses "and" instead of "&" in the titles.
(This is not a perfect solution, but it works for me, and I don't have a better idea at the moment)
If need be, you can add more entries to the title_rename.csv file, following the format:
    
    ```
    "old_title", "new_title"
    ```


## My workflow for best tagging

Have the digital version of the Manga/Comic
As I use Komga only for Manga, I will only describe how I am tagging my Manga.

1. Rename the Manga to the following format:
    ```
    <title> <Vvolume> <#Volume>.cbz
    ```
    Example:
    ```
    Naruto V001 #001 
    ```
This allows [comictagger](https://github.com/comictagger/comictagger) to correctly identify and auto tag the Manga. The Volume now has the metadata based on the data from [ComicVine](https://comicvine.gamespot.com/)
2. Import the Manga into Komga, either by directly copying the file into the specified folder, or by using the built-in import feature.

## Important notes

Currently the metadata for all entries in the database will be written the first time you run the script. 
If you want to add Series to the metadata grabbing process, you will have to remove the ageRating field in the WebUI, as I have written the [make_csv()](https://github.com/WorldTeacher/KomgaDBAdder-revamped/blob/main/dbcon.py#L19) function to only grab Series that do not have an ageRating.
