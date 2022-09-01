#this is a script to test the functions in the file
#the api being called is from mangadex.com
#the api is called with the query parameter



import requests
import json
import os
import time
from googlesearch import search
from googleapi import google
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import logger
import sqlite3

log=logger.log()
#get all folders in the mangafolder
class Komga:
    def __init__(self):
        self.change_title=input('Do you want to change the title? (y/n): ')
        self.api_param=self.additional_data()#'' #setting for the api to get additional data
        #self.additional_data() #query to define additional data
        #print(self.api_param)


    def get_series(self):
        with open('settings.json') as json_file:
            data=json.load(json_file)
            database=data['Database-Path']
        print(database)
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("SELECT name FROM series")
        seriesnames=c.fetchall()
        #remove '(' and ')' and ' from the series names
        for i in range(len(seriesnames)):
            seriesnames[i]=seriesnames[i][0].replace('(','').replace(')','').replace('\'','')
        #print(seriesnames)
        return seriesnames
            
    def get_folders():#*!Deprecated!*#
        try:
            with open('settings.json') as json_file:
                data=json.load(json_file)
            mangafolder=data['Manga_Folder']['Path']
        except Exception as e:
            log.error_api('Error getting folders: '+str(e))
            return
        folders = os.listdir(mangafolder)
        log.info_webrequest('Getting folders from: '+mangafolder)
        log.info_webrequest('Found '+str(len(folders))+' folders')

        return folders

    #function for getting the manga id
    def get_manga_id(self): #*!Deprecated!*#

        log.info_webrequest('Getting manga id')
        folders=Komga.get_folders()
        #print(folders)
        series_name_id={'id':[],'name':[]}
        for folder in folders:
            #do a google search for the folder name
            #get the first result
            #get the manga id from the result
            query=folder
            url_base= query + ' mangadex.org'
            log.info_webrequest('Searching for '+query+' on mangadex.org')
            for url in search(url_base, tld='com', num=1, stop=1, pause=2):
                
                if 'mangadex.org/title' in url:
                    log.info_webrequest('Found '+url)
                    array=url.split('/')
                    manga_id=array[4] #for the api call
                    series_name_id['id'].append(manga_id)
                    series_name_id['name'].append(folder)
                print(url)
                time.sleep(5)
        '''
        folders=self.get_folders()
         def get_folders(self):
            folders = os.listdir(self.mangafolder)
            log.info_webrequest('Getting folders from: '+self.mangafolder)
            log.info_webrequest('Found '+str(len(folders))+' folders')
            return folders
            
        for folder in folders:
            #folder=folder.replace(" ","%20")
            print(folder)
            #query is a google search for the manga title and mangadex.com
            lookup= folder + ' ' + '"mangadex"'
            #using the googlesearch module to get the url
            results = search(lookup,num_results=10) #search for the query, and return the first 10 results
            time.sleep(2)
            #print(url)
            #from results get the url
            for result in results:
                if 'mangadex' in result:
                    url=result
                    print(url)
                    #get the manga id from the url
                    manga_id=url.split('/')[-1]
                    print(manga_id)
                    #return the manga id
                    return manga_id
                    
                else:
                    continue
            print(results)
            
            time.sleep(1)'''
    #create a checker that checks if the user wants genres,tags
    #if true, add request part to the api call
    def additional_data(self):
        y_count=0
        log.info_api('Checking if the user wants additional data')
        '''genre=input('Do you want to get genres? (y/n): ')
        if genre=='y':
            y_count+=1
        tags=input('Do you want to get tags? (y/n): ')
        if tags=='y':
            y_count+=1
        '''
        artist=input('Do you want to get artists? (y/n): ')
        if artist=='y':
            y_count+=1
            log.info_api("Added Artist to API Query")
        else: log.info_api("Artist was not added to API Query")
            
        author=input('Do you want to get authors? (y/n): ')
        if author=='y':
            y_count+=1
            log.info_api("Added Author to API Query")
        else: log.info_api("Author was not added to API Query")
        print(y_count)
        
        api_param='?'
        
        if artist=='y':
            if y_count>1:
                api_param=api_param+'includes[]=artist&'
                y_count-=1
            else:
                api_param=api_param+'includes[]=artist'
        if author=='y':
            if y_count>1:
                api_param=api_param+'includes[]=author&'
            else:
                api_param=api_param+'includes[]=author'
        
        #print(api_param)
        #print(y_count)
   
        self.api_param=api_param

    def API_CALL_get(self):
        #query is the manga id
        for series in self.get_series():
            query=series
            #add all the exceptions to the api call
           
            url='https://api.mangadex.org/manga?title='+query+ '&order[relevance]=desc'# +'&includes[]=genres'
            log.info_api(f'Calling API with url: {url}')
            try:
                data= requests.get(url)
                log.debug_api('API call returned: '+str(data.status_code))
                if data.status_code==200:
                    log.info_api('API call successful')
                    datafield=json.loads(data.text)
                mangadata={'title':[],'summary':[],'language':[],'genres':[],'tags':[],'status':[],'ageRating':[],'publisher':[]}
                metadata=datafield['data'][0]['attributes']
            except Exception as e:
                log.error_api('Error getting data: '+str(e))
                continue
            for attr in metadata:
                #needed: description, language,status, genres, tags
                if self.change_title=='y': #* might be changed to altTitle, to get english title
                    if attr == 'title':
                        title_data = metadata[attr]['en']
                    try:
                        if attr =='altTitles':
                            len_alttitles = len(metadata[attr])
                            for i in range(len_alttitles):
                                if 'en' in metadata[attr][i]:
                                    alttitle_data = metadata[attr][i]['en']
                                    break
                            if title_data == alttitle_data:
                                log.info_api('Title is the same as altTitle')
                                mangadata['title'].append(title_data)
                            else:
                                log.info_api('Title is different from altTitle')
                                mangadata['title'].append(alttitle_data)
                    except:
                        log.info_api('No altTitles')
                        mangadata['title'].append(title_data)
                    
                if attr=='description':
                    log.info_api('Found description')
                    description=str(metadata[attr]['en'])
                    #remove \n from the description
                    description=description.replace('\n','')
                    description=description.replace('    ',' ')
                    #replace everything after ----
                    description=description.split('---')[0]
                    mangadata['summary'].append(description)
                    mangadata['language'].append('en')
                if attr=="status":
                    log.info_api('Found status')
                    mangadata['status'].append(metadata[attr])
                if attr=='tags':
                    log.info_api('Found tags and genres')
                    taglen=len(metadata['tags'])
                    for i in range(taglen):
                        #print(data['data']['attributes']['tags'][i])
                        if 'genre' in metadata['tags'][i]['attributes']['group']:
                            mangadata['genres'].append(metadata['tags'][i]['attributes']['name']['en'])
                        if 'theme' in metadata['tags'][i]['attributes']['group']:
                            mangadata['tags'].append(metadata['tags'][i]['attributes']['name']['en'])
                if attr=='publicationDemographic':
                    mangadata['tags'].append(metadata[attr])
                if attr=='contentRating':
                    log.info_api('Found age rating')
                    if metadata[attr]=='safe':
                        age=0
                    elif metadata[attr]=='suggestive':
                        age=16
                    elif metadata[attr]=='erotica':
                        age=18
                    log.info_api('Age rating is '+str(age))
                    mangadata['ageRating'].append(age)
                    mangadata['tags'].append(metadata[attr])
                if attr=='links':
                    log.info_api('Found publisher')
                    #print(metadata[attr])
                    #in metadata['links'] check if engtl is there
                    #if yes, get the publisher
                    #if no, get the first one
                    try:
                        if 'engtl' in metadata[attr]:
                            publisher=metadata[attr]['engtl']
                            publisher=publisher.split('/')
                            publisher=publisher[2]
                            publisher=publisher.split('.')
                            publisher=publisher[1]
                            mangadata['publisher'].append(publisher)
                        else:
                            publisher='unknown'
                            mangadata['publisher'].append(publisher)
                    except:
                        publisher='unknown'
                        mangadata['publisher'].append(publisher)
            print('######')
            print(mangadata)
            print('######')
    



    
    def get_manga_info(self):
        log.info_api('Getting manga info from API call')
        #import json file
        # with open('sth.json') as json_file:
        #     data=json.load(json_file)
        data=self.API_CALL_get()
        metadata=data['data']['attributes']
        mangadata={'title':[],'summary':[],'language':[],'genres':[],'tags':[],'status':[],'ageRating':[],'publisher':[]}
        
        for attr in metadata:
            
            #print(attr)
            #needed: description, language,status, genres, tags
            if self.change_title=='y': #* might be changed to altTitle, to get english title
                if attr == 'title':
                    title_data = metadata[attr]['en']
                try:
                    if attr =='altTitles':
                        len_alttitles = len(metadata[attr])
                        for i in range(len_alttitles):
                            if 'en' in metadata[attr][i]:
                                alttitle_data = metadata[attr][i]['en']
                                break
                        if title_data == alttitle_data:
                            log.info_api('Title is the same as altTitle')
                            mangadata['title'].append(title_data)
                        else:
                            log.info_api('Title is different from altTitle')
                            mangadata['title'].append(alttitle_data)
                except:
                    log.info_api('No altTitles')
                    mangadata['title'].append(title_data)
                
            if attr=='description':
                log.info_api('Found description')
                description=str(metadata[attr]['en'])
                #remove \n from the description
                description=description.replace('\n','')
                description=description.replace('    ',' ')
                #replace everything after ----
                description=description.split('----')[0]
                mangadata['summary'].append(description)
                mangadata['language'].append('en')
            if attr=="status":
                log.info_api('Found status')
                mangadata['status'].append(metadata[attr])
            if attr=='tags':
                log.info_api('Found tags and genres')
                taglen=len(metadata['tags'])
                for i in range(taglen):
                    #print(data['data']['attributes']['tags'][i])
                    if 'genre' in metadata['tags'][i]['attributes']['group']:
                        mangadata['genres'].append(metadata['tags'][i]['attributes']['name']['en'])
                    if 'theme' in metadata['tags'][i]['attributes']['group']:
                        mangadata['tags'].append(metadata['tags'][i]['attributes']['name']['en'])
            if attr=='publicationDemographic':
                mangadata['tags'].append(metadata[attr])
            if attr=='contentRating':
                log.info_api('Found age rating')
                if metadata[attr]=='safe':
                    age=0
                elif metadata[attr]=='suggestive':
                    age=16
                elif metadata[attr]=='erotica':
                    age=18
                log.info_api('Age rating is '+str(age))
                mangadata['ageRating'].append(age)
                mangadata['tags'].append(metadata[attr])
            if attr=='links':
                log.info_api('Found publisher')
                if 'engttl' in metadata['links']:
                    if "j-novel" in metadata['links']['engttl']:
                        publisher="J-Novel"
                    mangadata['publisher'].append(publisher)
                else:
                    publisher="none"
                    mangadata['publisher'].append(publisher)
              
           
               
        print(mangadata)
                # mangadata['ageRating'].append(metadata[attr])
        time.sleep(0.5)

            
    

    def main(self):
        self.get_manga_id()

if __name__=="__main__":
    #API_CALL_get("425f2ccf-581f-42cf-aed3-c3312fcde926")
    #get_manga_info()
    # get_manga_id()
    g=Komga()
    g.API_CALL_get()
   # g.get_manga_info()
    #g.get_series()