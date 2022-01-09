import pytest
import requests 
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

def get_film(title):
    '''Returns information on Studio Ghibli films in sentence format.
   
    Parameters
    ----------
    title: title of a film. (str)
    
    Returns 
    -------
    Returns information on a given film, including the director, producer, release year, run time, and film's pronunciation in Japanese. (str)
    
    Example
    --------
    >>> get_film(title='Princess Mononoke')
    >>>Princess Mononoke, directed by Hayao Miyazaki and produced by Toshio Suzuki, was release in 1997 with a run time of 134 minutes. The original title in Japanese, もののけ姫, is pronounced Mononoke hime.
    '''
    
    try:
        r_films=requests.get("https://ghibliapi.herokuapp.com/films")
        r_films.raise_for_status()
        
    except HTTPError as http_err:
        print(f'HTTP Error Occured: {http_err}')
    except Exception as err:
        print(f'Other Error Occured: {err}')
            
    else:
        ghibli=pd.DataFrame.from_dict(pd.json_normalize(r_films.json()), orient='columns')
        ghibli.loc[:,'output']=ghibli.apply(lambda x:f'{x["title"]}, directed by {x["director"]} and produced by {x["producer"]}, was released in {x["release_date"]} with a run time of {x["running_time"]} minutes. The original title in Japanese, {x["original_title"]}, is pronounced {x["original_title_romanised"]}.', axis=1)
        row=ghibli[ghibli['title']==title].index.item()
        print(ghibli['output'][row])
        
        assert 'title'!=title, "This film is unavailable."
        
        
        
def get_rating(title):
    '''Returns the rating of Studio Ghibli film in sentence format.
   
    Parameters
    ----------
    title: title of a film. (str)
    
    Returns 
    -------
    Returns the Rotten Tomatoes score for a given film. (str)
    
    Example
    --------
    >>>get_rating(title='Princess Mononoke')
    >>>According to Rotten Tomatoes, Princess Mononoke earned a score of 92 designating it Fresh! 
    '''
    try:
        r_films=requests.get("https://ghibliapi.herokuapp.com/films")
        r_films.raise_for_status()
        
    except HTTPError as http_err:
        print(f'HTTP Error Occured: {http_err}')
    except Exception as err:
        print(f'Other Error Occured: {err}')
    
    def rating(r):
        if r >=60:
            return 'Fresh!'
        else:
            return 'Rotten!'
    
    ghibli=pd.DataFrame.from_dict(pd.json_normalize(r_films.json()), orient='columns')
    ghibli['score']=ghibli['rt_score'].astype(int)
    ghibli['rtscore']=ghibli['score'].apply(rating)
    ghibli.loc[:,'RT']=ghibli.apply(lambda y:f'According to Rotten Tomatoes, {y["title"]} earned a score of {y["score"]} designating it {y["rtscore"]}', axis=1)
    row=ghibli[ghibli['title']==title].index.item()
    print(ghibli['RT'][row])
    
    assert 'title'!=title, "Rating for this film is unavailable."
    
    

def get_summary(title):
    '''Returns a summary of a Studio Ghibli films in sentence format.
   
    Parameters
    ----------
    title: title of a film. (str)
    
    Returns 
    -------
    Returns a summary of a given film. (str)
    
    Example
    --------
    >>> get_film(title='Princess Mononoke')
    >>>Princess Mononoke, directed by Hayao Miyazaki and produced by Toshio Suzuki, was release in 1997 with a run time of 134 minutes. The original title in Japanese, もののけ姫, is pronounced Mononoke hime.
    '''
    try:
        r_films=requests.get("https://ghibliapi.herokuapp.com/films")
        r_films.raise_for_status()
        
    except HTTPError as http_err:
        print(f'HTTP Error Occured: {http_err}')
    except Exception as err:
        print(f'Other Error Occured: {err}')
    
    
    ghibli=pd.DataFrame.from_dict(pd.json_normalize(r_films.json()), orient='columns')
    ghibli.loc[:,'summary']=ghibli.apply(lambda z:f'Summary of {z["title"]}: {z["description"]}', axis=1)
    row=ghibli[ghibli['title']==title].index.item()
    print(ghibli['summary'][row])
    
    assert 'title'!=title, "Summary for this film is unavailable."