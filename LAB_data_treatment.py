
def data_treatment():

    import pandas as pd
    import datetime
    from datetime import datetime
    from datetime import date


    import numpy as np
    path_centres='C:/Users/Clo/Desktop/LAB/centres_correspondance_table.csv'
    path='C:/Users/Clo/Desktop/LAB/combined_csv.csv'
    centres=pd.read_csv(path_centres,sep=";")
    data = pd.read_csv(path,sep=";")
   # print(data)
    print(data.shape)
    #print(data.columns)

    #creation des columns Groupe dentaire et zone geo (column S et T)--------------------------------------------------------------
    print(centres.columns)
    print(centres.shape)
    #on remplace les noms des centres toulouse et marseille
    data.loc[data.centre=="ASBBD MARSEILLE",'centre']="ASBBD Marseille Canebière"
    data.loc[data.centre=="ASBBD Toulouse Dentelia",'centre']="ASBBD Toulouse Lombez"



    #merged_left = pd.merge(left=survey_sub, right=species_sub, how='left', left_on='species_id', right_on='species_id')
    data_new=pd.merge(left=data, right=centres, how='left', left_on='centre', right_on='centre')

    print("apres join avec centre")
    print(data_new.shape)
    #correction de l'id_sortie=876030 , rajout date lecture sortie - RULE #1 (pour les cas 2 etapes identifiés on modifie l'id sortie)
    data_new.loc[data_new['id_sortie']==876030, ['date_lecture_retour']] = datetime.strptime('25/02/2022 00:00:00', '%d/%m/%Y %H:%M:%S')
    data_new.loc[data_new['id_sortie']==876030, ['date_lecture_retour']] = datetime.strptime('25/02/2022 00:00:00', '%d/%m/%Y %H:%M:%S')
    #data_new.date_lecture_retour[data_new.id_sortie=='876030'] = datetime.strptime('25/02/2022 12:02:00', '%d/%m/%Y %H:%M:%S')
    #creation colonnes K,M
    data_new['date_saisie_dentiste']= pd.to_datetime(data_new['date_saisie_dentiste'], format='%Y-%m-%d %H:%M:%S')
    data_new['date_saisie_dentiste']=data_new['date_saisie_dentiste'].dt.normalize()
    data_new['date_prise_en_charge']= pd.to_datetime(data_new['date_prise_en_charge'], format='%d/%m/%Y')
    data_new['date_prise_en_charge']=data_new['date_prise_en_charge'].dt.normalize()
    #print(data_new.dtypes)
    data_new['date_lecture_retour']= pd.to_datetime(data_new['date_lecture_retour'], format='%Y-%m-%d %H:%M:%S')
    data_new['date_lecture_retour']=data_new['date_lecture_retour'].dt.normalize()
    #data_new['date lecture retour format ddmmyyyy']=data_new['date_lecture_retour'].dt.normalize()
    data_new['delai total depuis édition bon']=pd.to_timedelta(data_new['date_lecture_retour']-data_new['date_saisie_dentiste'])
    data_new['delai total depuis édition bon']=data_new['delai total depuis édition bon'].dt.days
    data_new['delai saisie dentiste _ prise en charge labo']=pd.to_timedelta(data_new['date_prise_en_charge']-data_new['date_saisie_dentiste'])
    data_new['delai saisie dentiste _ prise en charge labo']=data_new['delai saisie dentiste _ prise en charge labo'].dt.days
    data_new['délai prise en charge labo_lecture retour']=data_new['date_lecture_retour']-data_new['date_prise_en_charge']
    data_new['délai prise en charge labo_lecture retour']=data_new['délai prise en charge labo_lecture retour'].dt.days
    data_new['delai saisie dentiste _ prise en charge labo'] = data_new['delai saisie dentiste _ prise en charge labo'].fillna(0)
    data_new['délai prise en charge labo_lecture retour'] = data_new['délai prise en charge labo_lecture retour'].fillna(0)
    data_new['delai total depuis édition bon'] = data_new['delai total depuis édition bon'].fillna(0)
    data_new['delai saisie dentiste _ prise en charge labo']=data_new['delai saisie dentiste _ prise en charge labo'].astype(int)
    data_new['délai prise en charge labo_lecture retour']=data_new['délai prise en charge labo_lecture retour'].astype(int)
    data_new['delai total depuis édition bon']=data_new['delai total depuis édition bon'].astype(int)
    data_new['Sortie']=1
    test=data_new[data_new['id_sortie']==845780]
    # CREATION COLONNE Label délai entre édition bon et lecture retour--------------------------------------------------------------------------------------
    # create a list of our conditions
    conditions = [
        (data_new['delai total depuis édition bon'] <= 8),
        (data_new['delai total depuis édition bon'] >= 9) & (data_new['delai total depuis édition bon'] <= 12),
        (data_new['delai total depuis édition bon'] == 13),
        (data_new['delai total depuis édition bon'] == 14 ),
        (data_new['delai total depuis édition bon'] >= 15)
        ]
    # create a list of the values we want to assign for each condition
    values = ['<=8D', 'between 9D and 12D', '13D', '14D','>=15D']

    # create a new column and use np.select to assign values to it using our lists as arguments
    data_new['Label délai entre édition bon et lecture retour'] = np.select(conditions, values)

    # CREATION COLONNE RETARD --------------------------------------------------------------------------------------
    # create a list of our conditions
    # conditions = [
    #     (data_new['delai total depuis édition bon'] >= 14) & (data_new['zone'] =='Province') ,
    #     (data_new['delai total depuis édition bon'] < 14) & (data_new['zone'] =='Province'),
    #     (data_new['delai total depuis édition bon'] >= 15) & (data_new['zone'] == 'IDF'),
    #     (data_new['delai total depuis édition bon'] < 15) & (data_new['zone'] == 'IDF'),
    #     ]
    # # create a list of the values we want to assign for each condition
    # values = [1,0, 1,0]


    conditions = [
        (data_new['delai total depuis édition bon'] >= 15),
        (data_new['delai total depuis édition bon'] < 15)
        ]
    # create a list of the values we want to assign for each condition
    values = [1,0]

    # create a new column and use np.select to assign values to it using our lists as arguments
    data_new['Retard'] = np.select(conditions, values)


    # CREATION COLONNE label delai prise en charge (COLONNE W) --------------------------------------------------------------------------------------
    # create a list of our conditions

    conditions = [
        (data_new['delai saisie dentiste _ prise en charge labo'] <=0),
        (data_new['delai saisie dentiste _ prise en charge labo'] ==1),
        (data_new['delai saisie dentiste _ prise en charge labo'] ==2),
        (data_new['delai saisie dentiste _ prise en charge labo'] ==3),
        (data_new['delai saisie dentiste _ prise en charge labo'] ==4),
        (data_new['delai saisie dentiste _ prise en charge labo'] ==5),
        (data_new['delai saisie dentiste _ prise en charge labo'] >=6 ) & (data_new['delai saisie dentiste _ prise en charge labo'] <=10 ) ,
        (data_new['delai saisie dentiste _ prise en charge labo'] >=11 ) & (data_new['delai saisie dentiste _ prise en charge labo'] <=15 ) ,
        (data_new['delai saisie dentiste _ prise en charge labo'] >= 16)
        ]
    # create a list of the values we want to assign for each condition
    values = ['0D', '1D', '2D', '3D','4D','5D','between 6D and 10D','between 11D and 15D','>=16D']

    # create a new column and use np.select to assign values to it using our lists as arguments
    data_new['label delai prise en charge'] = np.select(conditions, values)



    data_new['semaine_temp']=data_new['date_lecture_retour'].dt.isocalendar().week
    data_new['mois']=data_new['date_lecture_retour'].dt.strftime("%B")
    data_new['year']=data_new['date_lecture_retour'].dt.isocalendar().year
    data_new['semaine']="W"+data_new['semaine_temp'].astype(str)+" "+data_new['year'].astype(str)


    #data_new['date_lecture_retour']= pd.to_datetime(data_new['date_lecture_retour'], format='%Y-%m-%d %H:%M:%S')
    #data_new['semaine'] ="S"+ str(data_new.date_lecture_retour.apply(lambda x: x.weekofyear)[0])
    # CREATION COLONNE SEMAINE ( column L) -----------------------------------------------------------------------
    # for i in range(len(data_new)) :
    #    # print(data_new.loc[i,'date_lecture_retour'])
    #     #jour = datetime.strptime(data_new.loc[i,'date_lecture_retour'], '%Y-%m-%d %H:%M:%S')
    #     jour=data_new.loc[i,'date_lecture_retour']
    #     print(jour)
    #     print(type(jour))
    #     week=date(jour.year,jour.month,jour.day).isocalendar()[1]
    #     print(week)
    #     #creation colonne L ----------------------------------------------------------------------
    #     data_new.loc[i,'semaine']="S"+str(week)+" "+str(jour.year)
        #creation colonne K -------------------------------------------------------------------------
       # data_new.loc[i,'date lecture retour format ddmmyyyy']=jour.strftime('%d/%m/%Y')



    #date_prise_en_charge=data_new.loc[data_new['id_sortie']==845780, data_new['date_prise_en_charge']]
    #print(date_prise_en_charge)
    #date_saisie_dentiste=data_new.loc[data_new['id_sortie']==845780, data_new['date_saisie_dentiste']]
    #print(date_saisie_dentiste)

    #--------------------------------------------------------------------------- RULES --------------------------------------------------------------------------------------------

    print("avant rules")
    print(data_new.shape)
    #on ne garde que les lignes dont edition du bon >= 0 (on retire les cas en 2 étapes)
    data_new = data_new[data_new['delai total depuis édition bon']>= 0]
    print("apres rule delai total depuis edition bon >=0")
    print(data_new.shape)
    #on supprime les lignes ou les date saisie dentiste sont mal renseignées et donnent un delai prise en charge negatif
    data_new = data_new[data_new['delai saisie dentiste _ prise en charge labo']>= 0]
    print("apres rule delai saisie dentiste _ prise en charge labo >=0")
    print(data_new.shape)
    #on supprime les lignes avec partenaires nulls
    data_new = data_new[~data_new.partenaire.isnull()]
    print("apres rule partenaire not null")
    print(data_new.shape)
    #on supprime les lignes avec date lecture retour nulle
    data_new = data_new[data_new['date_lecture_retour'].notnull()]
    print("apres rule date_lecture_retour not null")
    print(data_new.shape)
    # on supprime les quelques cas ou pas de centre dentaire et year = 2021
    indexNames = data_new[(data_new['centre'].isnull()) & (data_new['year'] == 2021)].index
    data_new.drop(indexNames , inplace=True)
    # on supprime les lignes ou le delai total > 25D
    data_new = data_new[data_new['delai total depuis édition bon']<=25]
    print("apres rule delai total > 25D")
    print(data_new.shape)
    #On supprime les doublons
    data_new=data_new.drop_duplicates()
    print("apres supression des doublons")
    print(data_new.shape)

    columns=['id_sortie','date_prise_en_charge','dentiste','centre','contenu','date_saisie_dentiste','date_lecture_retour','groupe dentaire','zone',
             'delai total depuis édition bon',	'delai saisie dentiste _ prise en charge labo',	'délai prise en charge labo_lecture retour','Sortie',
             'Label délai entre édition bon et lecture retour',	'Retard',
             'label delai prise en charge',	'mois',	'year','semaine', 'partenaire']

    df_to_export=data_new[columns]
    print("df to export")
    print (df_to_export.shape)
    df_to_export.to_csv("//CDSO-BUR/Users/Clo/Desktop/LAB/___DAILYRESULT___.csv", sep=';',float_format='%,2f', index=False,date_format='%d/%m/%Y', encoding='utf-8-sig')
    print("data_treatment: fin")
    return
#  ------------------------------------------------------
#data_treatment()