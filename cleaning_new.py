import pandas as pd
import re
from fastai import *
from fastai.text import *

def clean(file,bank):
    if bank == 'danskebank':
        # read the large csv file with specified chunksize 
        df_chunk = pd.read_csv(file,delimiter=";", encoding='cp1252', chunksize=200)
        # append each chunk df here 
        chunk_list = []

        # Each chunk is in df format
        for chunk in df_chunk:  
            # append the chunk to list
            chunk_list.append(chunk)
        
        # concat the list into dataframe 
        df= pd.concat(chunk_list)
        # Filter out unimportant columns
        df = df[['Dato','Beløb','Tekst']]
        df.rename(columns={'Dato':'Date','Beløb':'Amount','Tekst':'Text'}, inplace=True)
        df['Amount'] = df['Amount'].replace({'\.':''}, regex = True)
        df['Amount'] = df['Amount'].replace({'\,':'.'}, regex = True)
                    
    elif bank == 'sydbank':  
        df_chunk = pd.read_csv(file,delimiter=";", encoding='cp1252', chunksize=200)
        chunk_list = []
        for chunk in df_chunk:  
            chunk_list.append(chunk)
        df= pd.concat(chunk_list)
        df = df[['Dato','Beløb','Tekst']]
        df.rename(columns={'Dato':'Date','Beløb':'Amount','Tekst':'Text'}, inplace=True)
        #Change german format to english one
        df['Amount'] = df['Amount'].replace({'\.':''}, regex = True)
        df['Amount'] = df['Amount'].replace({'\,':'.'}, regex = True)
        # Replace MCD and the numbers
        df['Text'] = df['Text'].replace({'^MCD':''}, regex = True)
        df['Text'] = df['Text'].replace({'\d*$':''}, regex = True)
        
    elif bank == 'n26':  
        df_chunk = pd.read_csv(file, chunksize=200)
        chunk_list = []
        for chunk in df_chunk:  
            chunk_list.append(chunk)
        df= pd.concat(chunk_list)
        df = df[['Datum','Verwendungszweck','Betrag (EUR)','Empfänger']]
        
        #merge empfänger and Verwendungszweck to 'Text'
        df['Verwendungszweck'].fillna(' ', inplace = True)
        df['Text'] = df['Empfänger'] +' '+ df['Verwendungszweck']
        
        df.rename(columns={'Datum':'Date','Betrag (EUR)':'Amount'}, inplace=True)
        df = df[['Text', 'Date', 'Amount']]               
        
        #Change Amount from Euro to DKK 
        df['Amount'] = df['Amount'].astype('float64', copy=False)
        df['Amount'] = df.Amount*7.5


    elif bank =='dkb':
        df_chunk = pd.read_csv(file,delimiter=";", encoding='cp1252', chunksize=200)
        chunk_list = []
        for chunk in df_chunk:  
            chunk_list.append(chunk)
        df= pd.concat(chunk_list)
        df = df[['Buchungstag','Betrag_EUR','Verwendungszweck']]
        df.rename(columns={'Buchungstag':'Date','Betrag_EUR':'Amount','Verwendungszweck':'Text'}, inplace=True)
        
        #replace kommas w/ dots -2.108,00
        df['Amount'] = df['Amount'].replace({'\.':''}, regex = True)
        df['Amount'] = df['Amount'].replace({'\,':'.'}, regex = True)
        
        #Replace AWV-MELDEPFLICHT BEACHTEN  HOTLINE BUNDESBANK: and (0800) 1234-111
        df['Text'] = df['Text'].replace({'(0800) 1234-111$':''}, regex = True)
        df['Text'] = df['Text'].replace({'AWV-MELDEPFLICHT BEACHTEN  HOTLINE BUNDESBANK:*':''}, regex = True) 
        
        #Change Amount from Euro to DKK 
        df['Amount'] = df['Amount'].astype('float64', copy=False)
        df['Amount'] = df.Amount*7.5

        #Delete dates in data
        for i in range(df.shape[0]):
            content=df['Text'][i]
            df['Text'][i]= re.sub('\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s(.*)', '',content)
            df['Text'][i]= re.sub('\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.\s(.*)', '',content)
            df['Text'][i]= re.sub('\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.\d{2}\s(.*)', '',content)

    else:
        print('unknown Bank')

        
    #Change Datatype of amount to float
    df['Amount'] = df['Amount'].astype('float64', copy=False)
    #Delete all positive transfers
    df=df[df.Amount <0.0]
                        
    #Delete weird brackets (((
    df['Text'] = df['Text'].replace({'\)\)\)\)':''}, regex = True)
    df['Text'] = df['Text'].replace({'\)\)\)':''}, regex = True)


    #START THE PREDICTION

    learn = load_learner('model')
    result = learn.predict('lidl med some text')

    return(result)

"""
    return (result)

    #Append column
    df['Prediction'] = df.apply(lambda _: '', axis=1)

    for i in range(df.shape[0]):
        df['Prediction'][i] = learn.predict(df['Text'][i])

    df['Prediction'] = df['Prediction'].astype(str)

    def clean_predictions(programme): 
        # Search for comma in the name followed by any characters repeated any number of times 
        if re.search('\,.*', programme): 
    
            # Extract the position of beginning of pattern 
            pos = re.search('\,.*', programme).start() 
            pos1 = (programme).find(' ')
    
            # return the cleaned name 
            return programme[pos1+1:pos] 
    
        else: 
            #if none of those patterns found, return the original name
            return programme 
            
    # Updated the study programme columns 
    df['Prediction'] = df['Prediction'].apply(clean_predictions)
        return(df.to_string(max_rows=10))
        print(df.head())
                                            
                        
    #Export the cleaned data
    df.to_csv('Data_Cleaned.csv', index =False)
    """