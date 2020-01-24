import pandas as pd
import re

def clean(file,bank):

    if bank == 'danskebank':
        df = pd.read_csv(file, delimiter=";", encoding='cp1252', usecols = ['Dato','Beløb','Tekst'])
        df.rename(columns={'Dato':'Date','Beløb':'Amount','Tekst':'Text'}, inplace=True)
        #replace kommas w/ dots -2.108,00
        df['Amount'] = df['Amount'].replace({'\.':''}, regex = True)
        df['Amount'] = df['Amount'].replace({'\,':'.'}, regex = True)
        
    elif bank == 'Sydbank':  
        df = pd.read_csv(file, delimiter=";", encoding='cp1252', usecols = ['Dato','Beløb','Tekst'])
        df.rename(columns={'Dato':'Date','Beløb':'Amount','Tekst':'Text'}, inplace=True)
        
        #Change german format to english one
        df['Amount'] = df['Amount'].replace({'\.':''}, regex = True)
        df['Amount'] = df['Amount'].replace({'\,':'.'}, regex = True)
        
        # Replace MCD and the numbers
        df['Text'] = df['Text'].replace({'^MCD':''}, regex = True)
        df['Text'] = df['Text'].replace({'\d*$':''}, regex = True)
        
    elif bank == 'N26':  
        df = pd.read_csv(file, usecols = ['Datum','Verwendungszweck','Betrag (EUR)','Empfänger'])
        
        #merge empfänger and Verwendungszweck to 'Text'
        df['Verwendungszweck'].fillna(' ', inplace = True)
        df['Text'] = df['Empfänger'] +' '+ df['Verwendungszweck']
        
        df.rename(columns={'Datum':'Date','Betrag (EUR)':'Amount'}, inplace=True)
        df = df[['Text', 'Date', 'Amount']]               
        
        #Change Amount from Euro to DKK 
        df['Amount'] = df['Amount'].astype('float64', copy=False)
        df['Amount'] = df.Amount*7.5


    elif bank =='DKB':
        df = pd.read_csv(file, delimiter=";", encoding='cp1252', usecols = ['Buchungstag','Betrag_EUR','Verwendungszweck'])
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
                        
    print(df.head())
                                        
                        
    #Export the cleaned data
    df.to_csv('Data_Cleaned.csv', index =False)

    return("Done")


    # In[ ]:


