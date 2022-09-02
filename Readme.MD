#Welcome to the documentation of the KomgaDBAdder-revamped

This documentation describes the metadata injection process, and how to use it. The process is divided in two steps:

   1. Going though the database and creating a csv file with the title and the Series_ID
   2. Grabbing the metadata using the MangaDex API and writing it to the database

## Setup:

1. Clone the repository using `git clone, or simply download the zip file and unzip it.
2. Add your database path to the settings.json file. (While you are there, you might want to change the age ratings, depending on your opinion)
3. Shutdown the Komga Server and make a backup of the database. (nothing should go wrong, but you should be careful)
4. Run the following command:

```pyhton
python setup.py 
```
This will create the csv file that will be used later on.
5. Run the following command:

```pyhton
python main.py
```
This will start the metadata-grabbing and write the metadata to the database.

## What will be written to the database:
These are the fields that will be written to the database:
- Summary
- age rating, based on the available age ratings in the settings.json file
- Genres
- Tags
- Language, currently hardcoded to English, as I only have English titles in my database
- Status

## What's this about the title_rename.csv file?

As I tested the functionality, I found that the titles from the database are not always the same as the titles from the website. This can eiter be because the Foldername is not the same as the title, or because MangaDex has a different naming scheme.

I have hardcoded a conversion from "&" to "and", as MangaDex mostly uses "and" instead of "&" in the titles.
(This is not a perfect solution, but it works for me, and I don't have a better idea at the moment)
If need be, you can add more entries to the title_rename.csv file, following the format:
    
    ```
    "old_title", "new_title"
    ```