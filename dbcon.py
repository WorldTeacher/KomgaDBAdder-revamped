import sqlite3
import pandas as pd
import time
import logger
log=logger.log()
def connect():
    conn=sqlite3.connect('database.sqlite')
    c=conn.cursor()
    return c,conn

def make_csv():
    c,conn=connect()
    query="SELECT id,name FROM series"
    series_id={'series_id':[],'series_name':[]}
    c.execute(query)
    for row in c:
        series_id['series_id'].append(row[0])
        series_id['series_name'].append(row[1])
        #series_add.append(series_id)
        #print(series_id)
    conn.close()
    df=pd.DataFrame(series_id)
    df.to_csv('series_id.csv',index=False,header=True)

def check_db():
    #see if database is reachable
    c,conn=connect()
    query="SELECT Sqlite_version()"
    c.execute(query)
    result=c.fetchone()
    conn.close()
    return result

def write_db_summary(series_id,summary):
    log.info_api("Writing summary to database")
    #write series_id and series_name to database
    c,conn=connect()
    #insert values from data into database at table series_metadata
    query="UPDATE SERIES_METADATA SET SUMMARY=? WHERE SERIES_ID=?"
    c.execute(query,(summary,series_id))
    conn.commit()
    conn.close()
    log.info_api("Finished writing summary to database")

def write_db_genres(series_id,genres):
    log.info_api("Writing genres to database")
    #write series_id and series_name to database
    c,conn=connect()
    #insert values from data into database at table series_metadata
    for genre in genres:
        genre=genre.lower()
        query="INSERT INTO SERIES_METADATA_GENRE (SERIES_ID,GENRE) VALUES (?,?)"
        c.execute(query,(series_id,genre))
    conn.commit()
    conn.close()
    log.info_api(f"Finished writing genres {genres} to database")

def write_db_tags(series_id,tags):
    log.info_api("Writing tags to database")
    log.debug_api(f"Tags: {tags}")
    #write series_id and series_name to database
    c,conn=connect()
    #insert values from data into database at table series_metadata
    for tag in tags:
        #check if tag is NoneType
        if tag is None:
            continue
        tag=tag.lower()
        query="INSERT INTO SERIES_METADATA_TAG (SERIES_ID,TAG) VALUES (?,?)"
        c.execute(query,(series_id,tag))
    conn.commit()
    conn.close()
    log.info_api(f"Finished writing tags {tags} to database")

def write_db_ageRating(series_id,ageRating):
    log.info_api("Writing ageRating to database")
    #write series_id and series_name to database
    c,conn=connect()
    #insert values from data into database at table series_metadata
    query="UPDATE SERIES_METADATA SET AGE_RATING=? WHERE SERIES_ID=?"
    c.execute(query,(ageRating,series_id))
    conn.commit()
    conn.close()
    log.info_api(f"Finished writing ageRating {ageRating}  to database")

def write_db_status(series_id,status):
    log.info_api("Writing status to database")
    #write series_id and series_name to database
    c,conn=connect()
    #insert values from data into database at table series_metadata
    query="UPDATE SERIES_METADATA SET STATUS=? WHERE SERIES_ID=?"
    c.execute(query,(status,series_id))
    conn.commit()
    conn.close()
    log.info_api(f"Finished writing status {status} to database")

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
    log.info_api("Writing to database")
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
    log.info_api(f'Finished writing {series_id} to database')
def test(data):
    summary=data['summary'] #-> summary (string)
    genres=data['genres']   #-> genres (list)
    tags=data['tags']    #-> tags (list)
    ageRating=data['ageRating'] #-> ageRating (int)
    status=data['status'] #-> status (string)
    for tag in tags:
        print(tag)
        print(tag.lower())
if __name__=="__main__":
    data={'id':["095S75W3H260P"],'summary':[],'genres':[],'tags':['Romance', "Girls' Love"],'status':'ongoing', 'ageRating':[0]}
    #print(type(data['id'][0]),type(data['summary'][0]),type(data['genres']),type(data['tags']),type(data['ageRating']))
    #write_db(data)
    test(data)
    