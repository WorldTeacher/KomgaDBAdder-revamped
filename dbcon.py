import sqlite3
import pandas as pd
import time
import logger
import json
log=logger.log()

def connect():
    with open('settings.json') as f:
        config=json.load(f)
    global db_path
    db_path=config['Database-Path']
    
    conn=sqlite3.connect(db_path)
    c=conn.cursor()
    return c,conn

def make_csv():
    c,conn=connect()
    #get the series_id and series_name from the SERIES table if the ageRating in the SERIES_METADATA table is null
    query="SELECT ID,NAME FROM SERIES WHERE ID IN (SELECT SERIES_ID FROM SERIES_METADATA WHERE AGE_RATING IS NULL)"
    series_id={'series_id':[],'series_name':[]}
    c.execute(query)
    for row in c:
        series_id['series_id'].append(row[0])
        series_id['series_name'].append(row[1])
        #series_add.append(series_id)
        #print(series_id)
    conn.close()
    df=pd.DataFrame(series_id)
    df.to_csv('series_id-newer.csv',index=False,header=True)

def check_db():
    #see if database is reachable
    try:
        c,conn=connect()
        query="SELECT Sqlite_version()"
        c.execute(query)
        result=c.fetchone()
        conn.close()
        log.info_api(f"Database {db_path} is reachable")
    except sqlite3.OperationalError:
        log.fatal_db(f"Database not reachable, is this the correct path? {db_path}")
    return result

def write_db_summary(series_id,summary):
    log.info_db("Writing summary to database")
    #write series_id and series_name to database
    c,conn=connect()
    #insert values from data into database at table series_metadata
    query="UPDATE SERIES_METADATA SET SUMMARY=? WHERE SERIES_ID=?"
    c.execute(query,(summary,series_id))
    conn.commit()
    conn.close()
    log.info_db("Finished writing summary to database")

def write_db_genres(series_id,genres):
    log.info_db("Writing genres to database")
    c,conn=connect()
    for genre in genres:
        genre=genre.lower()
        #insert values from data into database at table series_metadata_genre if they don't already exist
        query="INSERT INTO SERIES_METADATA_GENRE (SERIES_ID,GENRE) SELECT ?,? WHERE NOT EXISTS (SELECT 1 FROM SERIES_METADATA_GENRE WHERE SERIES_ID=? AND GENRE=?) "
        c.execute(query,(series_id,genre,series_id,genre))
    conn.commit()
    conn.close()
    log.info_db(f"Finished writing genres {genres} to database")

def write_db_tags(series_id,tags): 
    log.info_db("Writing tags to database")
    #write series_id and series_name to database
    c,conn=connect()
    #insert values from data into database at table series_metadata
    for tag in tags:
        #check if tag is NoneType
        if tag is None:
            continue
        tag=tag.lower()
        query="INSERT INTO SERIES_METADATA_TAGS (SERIES_ID,TAG) SELECT ?,? WHERE NOT EXISTS (SELECT 1 FROM SERIES_METADATA_TAGS WHERE SERIES_ID=? AND TAG=?) "
        c.execute(query,(series_id,tag,series_id,tag))
    conn.commit()
    conn.close()
    log.info_db(f"Finished writing tags {tags} to database")

def write_db_ageRating(series_id,ageRating):
    log.info_db("Writing ageRating to database")
    #write series_id and series_name to database
    c,conn=connect()
    #insert values from data into database at table series_metadata
    query="UPDATE SERIES_METADATA SET AGE_RATING=? WHERE SERIES_ID=?"
    c.execute(query,(ageRating,series_id))
    conn.commit()
    conn.close()
    log.info_db(f"Finished writing ageRating {ageRating}  to database")

def write_db_status(series_id,status):
    log.info_db("Writing status to database")
    #write series_id and series_name to database
    c,conn=connect()
    if status=='completed':
        status='ENDED'
    status=status.upper()

    #insert values from data into database at table series_metadata
    query="UPDATE SERIES_METADATA SET STATUS=? WHERE SERIES_ID=?"
    c.execute(query,(status,series_id))
    conn.commit()
    conn.close()
    log.info_db(f"Finished writing status {status} to database")

def remove_text_in_parentheses_from_db():
    c,conn=connect()
    replacement=['(1)','(2)','(3)','(4)','(5)','(6)','(7)','(8)','(9)','(10)','(11)','(12)','(13)','(14)','(15)','(16)','(17)','(18)','(19)','(20)','(21)','(22)','(23)','(24)','(25)','(26)','(27)','(28)','(29)','(34)','(1990)','(1991)','(1992)','(1993)','(1994)','(1995)','(1996)','(1997)','(1998)','(1999)','(2000)','(2001)','(2002)','(2003)','(2004)','(2005)','(2006)','(2007)','(2008)','(2009)','(2010)','(2011)','(2012)','(2013)','(2014)','(2015)','(2016)','(2017)','(2018)','(2019)','(2020)','(2021)','(2022)','(2023)','(2024)','(2025)','(2026)','(2027)','(2028)','(2029)','(2030)','(2031)','(2032)','(2033)','(2034)','(2035)','(2036)','(2037)','(2038)','(2039)','(2040)','(2041)','(2042)','(2043)','(2044)','(2045)','(2046)','(2047)','(2048)','(2049)','(2050)','(2051)','(2052)','(2053)','(2054)','(2055)','(2056)','(2057)','(2058)','(2059)','(2060)','(2061)','(2062)','(2063)','(2064)','(2065)','(2066)','(2067)','(2068)','(2069)','(2070)','(2071)','(2072)','(2073)','(2074)','(2075)','(2076)','(2077)','(2078)','(2079)','(2080)','(2081)','(2082)','(2083)','(2084)','(2085)','(2086)','(2087)','(2088)','(2089)','(2090)','(2091)','(2092)','(2093)','(2094)','(2095)','(2096)','(2097)']
    #for repl in replacements, remove the parentheses from the title
    for repl in replacement:
        print(repl)
        c.execute("UPDATE SERIES_METADATA SET TITLE=REPLACE(TITLE,?,?)", (repl,''))
        c.execute("UPDATE SERIES_METADATA SET TITLE_SORT=REPLACE(TITLE_SORT,?,?)", (repl,''))

        conn.commit()
        time.sleep(1)

def write_db(data):
    log.info_db("Writing to database")
    series_id=data['series_id']
    summary=data['summary'] #-> summary (string)
    genres=data['genres']   #-> genres (list)
    tags=data['tags']    #-> tags (list)
    ageRating=data['ageRating'] #-> ageRating (int)
    status=data['status'] #-> status (string)
    write_db_summary(series_id,summary)
    write_db_genres(series_id,genres)
    write_db_tags(series_id,tags)
    write_db_ageRating(series_id,ageRating)
    write_db_status(series_id,status)

    log.info_db(f'Finished writing {series_id} to database')

def test():
    c,conn=connect()
    c.execute("SELECT * FROM SERIES_METADATA")
    print(c.fetchall())
    conn.close()
if __name__=="__main__":
    make_csv()