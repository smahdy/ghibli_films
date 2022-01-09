from ghibli_films import ghibli_films
import requests 
import pandas as pd
import numpy as np
import json


def get_film(title):
    
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
        return ghibli['output'][row]
        
        assert 'title'!=title, "This film is unavailable."
        
        

def test_get_film():
    actual=get_film('Princess Mononoke')
    expected="Princess Mononoke, directed by Hayao Miyazaki and produced by Toshio Suzuki, was released in 1997 with a run time of 134 minutes. The original title in Japanese, もののけ姫, is pronounced Mononoke hime."
    assert actual==expected  
                    
test_get_film()
                    


def get_rating(title):
   
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
    return ghibli['RT'][row]
    
    assert 'title'!=title, "Rating for this film is unavailable."
                    
def test_get_rating():
    actual=get_rating('Princess Mononoke')
    expected="According to Rotten Tomatoes, Princess Mononoke earned a score of 92 designating it Fresh!"
    assert actual==expected  
                    
test_get_rating()
                    
def get_summary(title):
    
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
    return ghibli['summary'][row]
    
    assert 'title'!=title, "Summary for this film is unavailable."
                    
def test_get_summary():
    actual=get_summary('Princess Mononoke')
    expected="Summary of Princess Mononoke: Ashitaka, a prince of the disappearing Ainu tribe, is cursed by a demonized boar god and must journey to the west to find a cure. Along the way, he encounters San, a young human woman fighting to protect the forest, and Lady Eboshi, who is trying to destroy it. Ashitaka must find a way to bring balance to this conflict."
    assert actual==expected  
                    
test_get_summary()