

def retrieve_max_date() :
    import pandas
    excel_path = 'C:/Users/Clo/Desktop/LAB/DATA.xlsx'
    df = pandas.read_excel(excel_path)
    #print(df.info())
    df['date_lecture_retour'] = pandas.to_datetime(df['date_lecture_retour'], format='%d/%m/%Y')
    #print(df.info())
    date_max=df['date_lecture_retour'].max()
    return date_max

#print(retrieve_max_date())