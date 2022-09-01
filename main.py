# * This is the main script, it coordinates the other scripts.

import mangadex_api as manga
import dbcon as db
import logger
import os
import time
import sys
import pandas as pd
log=logger.log()
#make a function that gets the start and endtime of the program
def get_start_time():
    #get the start time of the program
    start_time=time.time()
    return start_time


log.info_main("Starting program")
log.info_main("Checking if Program can be run")
def can_run():
    # * Check if program can be run
    # check if csv is present
    # check if database is present
    #check if series_id_name.csv is present
    files=False
    Database=False
    if os.path.exists('series_id.csv'):
        log.info_main("series_id.csv found")
        files=True
    else:
        log.critical_main("series_id.csv not found")
    db_reachable=db.check_db() 
    if db_reachable is not None:
        log.info_main("Database is reachable")
        Database=True
    else:
        log.critical_main("Database is not reachable")
    if files and Database is True:
        log.info_main("Program can be run")
        print("Program can be run")
    else:
        log.fatal_main("Program can not be run")
        print("Program can not be run, check log")
        sys.exit()
def main():

    # Main function
    # Check if program can be run
    start=get_start_time()
    can_run()
    # Check if database is reachable
    db_reachable=db.check_db()
    if db_reachable is not None:
        log.info_main("Database is reachable")
        # Read series_id_name.csv
        series_id_name=pd.read_csv('series_id.csv')
        # Loop through series_id_name
        for index,row in series_id_name.iterrows():
            print(f'index: {index}')
            # Get series_id and series_name
            series_id=row['series_id']
            series_name=row['series_name']
            # Get series_metadata from mangadex_api
            series_metadata=manga.get_metadata(series_name)
            summary=series_metadata['summary'][0]
            genres=series_metadata['genres']
            tags=series_metadata['tags']
            ageRating=series_metadata['ageRating'][0]
            status=series_metadata['status'][0]
            data={'series_id':series_id,'series_name':series_name,'summary':summary,'genres':genres,'tags':tags,'ageRating':ageRating,'status':status}
            print(f'finished: {series_id,series_name}')
            db.write_db(data)

            time.sleep(1)
            # # Get summary from series_metadata
            # summary=series_metadata['data']['attributes']['description']['en']
            # # Get genres from series_metadata
            # genres=series_metadata['data']['attributes']['publicationDemographic']
            # # Get tags from series_metadata
            # tags=series_metadata['data']['attributes']['tags']
            # # Write summary to database
            # db.write_db_summary(series_id,summary)
            # # Write genres to database
            # db.write_db_genres(series_id,genres)
            # # Write tags to database
            # db.write_db_tags(series_id,tags)
            # # Sleep for 1 second
            # time.sleep(1)
    else:
        log.error_main("Database is not reachable")
        print("Database is not reachable")
        sys.exit()
    end=time.time()
    log.info_main(f"Program took {end-start} seconds to run")
    print(f"Program took {end-start} seconds to run")
if __name__=="__main__":
    main()