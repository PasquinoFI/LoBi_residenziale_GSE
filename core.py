"""
LoBi_standard_GSE - core
"""



### CORE - non toccare

def genera_serie(tipologia_bolletta,numero_utenze,name,output=False):
    
    sigla = f"PDM{tipologia_bolletta}"
    
    import pandas as pd
    
    df = pd.read_csv(f"profilo_standard_GSE.csv")
    datetime_index = pd.date_range(start = '01-01-2021 00:00', end   = '31-12-2021 23:00', freq  = 'H')    
    df.index = datetime_index
    df['DayType'] = df.index.weekday  
    df['bolletta'] = 0
    df['correzione'] = 1
    
    if tipologia_bolletta == 'M':
    
        bolletta_mono = pd.read_excel("bolletta_mono.xlsx", header=0, index_col='Mese')
        for i in df.index:
            m = df.loc[i,'Mese']
            df.loc[i,'bolletta'] = bolletta_mono['kW'][m]
        
        
    elif tipologia_bolletta == 'F':
        
        bolletta_tri = pd.read_excel("bolletta_tri.xlsx", header=0, index_col='Mese')
        bolletta_tri = bolletta_tri.rename(columns={'kWh F1':1,'kWh F2':2, 'kWh F3':3})
        
        # Timeslots
        import holidays
        it_holidays = holidays.Italy(years=2021)
        for date in it_holidays:
            for i in df.index:
                if i.date() == date:
                    df.loc[i,'DayType'] = 6
        mask_F1   = (df['DayType'] < 5) & (df.index.hour >= 8)  & (df.index.hour < 19)           # Mask F1 
        mask_F2_m = (df['DayType'] < 5) & (df.index.hour == 7)                                   # Mask F2 workday morning
        mask_F2_e = (df['DayType'] < 5) & (df.index.hour >= 19) & (df.index.hour < 23)           # Mask F2 workday evening   
        mask_F2_s   = (df['DayType'] == 5) & (df.index.hour >= 7)  & (df.index.hour < 23)        # Mask F2 saturday    
        df['TimeSlot'] = 3                                                                       # Set 3 to F3
        df['TimeSlot'].where(~mask_F1, other=1, inplace=True)                                    # Set 1 to F1 for Workdays       
        df['TimeSlot'].where(~mask_F2_m, other=2, inplace=True)                                  # Set 2 to F2 Workdays morning
        df['TimeSlot'].where(~mask_F2_e, other=2, inplace=True)                                  # Set 2 to F2 Workdays evening
        df['TimeSlot'].where(~mask_F2_s, other=2, inplace=True)                                  # Set 2 to F2 Saturdays
            
        for i in df.index:
            m = df.loc[i]['Mese']
            ts = df.loc[i]['TimeSlot']
            df.loc[i,'bolletta'] = bolletta_tri[ts][m]
            
            # correzione profili per leggera inesattezza (alcune fasce di alcuni mesi non sommano perfettamente ad uno)
            condizione1 = df['Mese'] == m
            condizione2 = df['TimeSlot'] == ts
            df.loc[i,'correzione'] = df.loc[condizione1 & condizione2]['PDMF'].sum()
              
    df['kW'] = df[sigla]*df['bolletta']/df['correzione']*numero_utenze
    
    # save file.csv
    directory = './profili_generati'
    import os 
    if not os.path.exists(directory): os.makedirs(directory)
    df['kW'] = df['kW'].round(4)
    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime('%m-%d %H:%M:%S')
    df.index.name = 'time'
    df['kW'].to_csv(f"{directory}/{name}.csv")
    
    if output:
        return(df)