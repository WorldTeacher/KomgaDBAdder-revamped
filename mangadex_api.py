# * This is the script that interacts with the API.
# * It is used to get metadata for a manga.

import requests
import json
import logger
import csv

log=logger.log()
title_replace_list={'title':[],'title_replace':[]}
with open('settings.json') as f:
    settings=json.load(f)
    rating_safe=settings['rating_safe']
    rating_suggestive=settings['rating_suggestive']
    rating_erotica=settings['rating_erotica']
with open('title_rename.csv') as f:
    has_header = csv.Sniffer().has_header(f.read(1024))
    f.seek(0)  # Rewind.
    reader = csv.reader(f)
    if has_header:
        next(reader)
    for row in reader:
        title_replace_list['title'].append(row[0])
        title_replace_list['title_replace'].append(row[1])
def get_metadata(title):
    if title != "skip" :
        url=f'https://api.mangadex.org/manga?title={title}&order[relevance]=desc'
        log.info_api(f'Getting metadata for {title}')
        log.info_api(f'URL: {url}')
        try:
            data=requests.get(url)
            log.debug_api(f'API response: {data.status_code}')
            if data.status_code==200:
                log.info_api("API request successful")
                datafields=json.loads(data.text)
            metadata=datafields['data'][0]['attributes']
            #result=process_metadata(metadata)
            #if status code is >=400, then there is no data, skip 
            if data.status_code>=400:
                log.warning_api(f'No data for {title}')
                metadata=None
        except Exception as e:
            log.error_api(f'Error: {e}')
            metadata=None
        return metadata
    else:
        log.warning_api(f'Skipping Title, as it is in the skip list')
        metadata=None
        return metadata
def process_metadata(metadata):
    mangadata={'summary':[],'language':[],'genres':[],'tags':[],'status':[],'ageRating':[]} #! removed ,'publisher':[], since this is mostly handeled by comictagger
        
    for attr in metadata:
        # if attr=='title': #! temorarily removed title from metadata search, as it is mostly handeled by comictagger and Komga
        #     title_data=metadata[attr]['en']
        #     try:
        #         if attr =='altTitles':
        #             len_alttitles = len(metadata[attr])
        #             for i in range(len_alttitles):
        #                 if 'en' in metadata[attr][i]:
        #                     alttitle_data = metadata[attr][i]['en']
        #                     break
        #             if title_data == alttitle_data:
        #                 log.info_api('Title is the same as altTitle')
        #                 mangadata['title'].append(title_data)
        #             else:
        #                 log.info_api('Title is different from altTitle')
        #                 mangadata['title'].append(alttitle_data)
        #     except:
        #         log.info_api('No altTitles')
        #         mangadata['title'].append(title_data)
            
        if attr=='description':
            #check if description is empty
            if metadata['description']==[] or metadata['description']==None:
                log.info_api('No description')
                mangadata['summary'].append('No description available')
            else:
                description_data=str(metadata[attr]['en'])
                description_data=description_data.replace('\n','')
                description_data=description_data.replace('    ',' ')
                #replace everything after ----
                description_data=description_data.split('---')[0]
                mangadata['summary'].append(description_data)
                mangadata['language'].append('en')
        if attr=='status':
            status_data=metadata[attr]
            mangadata['status'].append(status_data)
        if attr=='contentRating':
            if metadata[attr]=='safe':
                age=rating_safe
            elif metadata[attr]=='suggestive':
                age=rating_suggestive
            elif metadata[attr]=='erotica':
                age=rating_erotica
            mangadata['ageRating'].append(age)
            mangadata['tags'].append(metadata[attr])
        if attr=='tags':
            taglen=len(metadata['tags'])
            for i in range(taglen):
                #print(data['data']['attributes']['tags'][i])
                if 'genre' in metadata['tags'][i]['attributes']['group']:
                    mangadata['genres'].append(metadata['tags'][i]['attributes']['name']['en'])
                if 'theme' in metadata['tags'][i]['attributes']['group']:
                    
                    mangadata['tags'].append(metadata['tags'][i]['attributes']['name']['en'])
        if attr=='publicationDemographic':
            mangadata['tags'].append(metadata[attr])
        # if attr=='links': #! this might be re-added later, depending on how well the  publishers are added using comictagger
        #     if 'engtl' in metadata[attr]:
        #         if 'j-novel' in metadata[attr]['engtl']:
        #             mangadata['publisher'].append('J-Novel')
        #         else: print(metadata[attr]['engtl'])            
    #print(mangadata)
    return mangadata

def api_search(title):
    title=title_replace(title)
    metadata=get_metadata(title)
    if metadata is not None:
        processed_metadata=process_metadata(metadata)
    else:
        processed_metadata=None
    return processed_metadata

def title_replace(title):
    for i in range(len(title_replace_list['title'])):
        if title==title_replace_list['title'][i]:
            title=title_replace_list['title_replace'][i]
    #if title contains & replace with 'and', as the mangadex api does not support &
    if '&' in title:
        title=title.replace('&','and')
    #if title contains Pok??mon, set title to Pok??mon Adventure
    if 'Pok??mon' in title:
        title='Pok??mon Adventure'
    if 'Pok??mon' in title:
        title='Pok??mon Adventure'
    if title=='Good Dog, Cerberus!':
        title='skip'
    return title
if __name__=='__main__':
    pass

