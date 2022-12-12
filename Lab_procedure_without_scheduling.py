
import schedule
import time
import datetime
from LAB import *
from Lab_merge_csv import *
from LAB_data_treatment import *
from LAB_copy_to_excel import *
from Send_email import *
from LAB_functions import *


def job():
     #datetime.datetime.today()
        start_date = retrieve_max_date()

     #retrieve_max_date()
            #retrieve_max_date()
        #datetime.date(2022, 5, 11)
            #datetime.date(2022, 5, 13)

        end_date=datetime.date.today()

            #datetime.date.today()
            #datetime.date(2022, 5, 10)
        delta = datetime.timedelta(days=1)
        # etape 1 on collecte la donnée avec la fonction collect_daily_data du fichier Lab.py
        while start_date <= end_date:
            print(start_date)
            collect_daily_data(start_date)
            start_date += delta


        print("Collect daily data : fin")
        #etape 2 on cree le fichier csv merge avec les nouvelles donnees
        merge_csv()
        #etape 3 : on lance le traitement des donnees
        data_treatment()
        #etape 4 : on incorpore dans le fichier excel
        copy_to_excel()
        #etape 5: on envoie par mail
        excel_new_path_name = 'C:/Users/Clo/Desktop/LAB/Daily_reports/LAB_DAILY_REPORT-' + datetime.datetime.today().strftime(
            '%Y-%m-%d') + '.xlsx'
        send_email(excel_new_path_name)
        print("Everything fine")
        return

job()

