

def copy_to_excel():
    import os
    import xlsxwriter
    import openpyxl
    import datetime
    import pandas as pd
    import time
    from win32com.client import Dispatch
    import shutil
    t0 = time.time()


    #options['strings_to_url']=False
    data_to_copy='C:/Users/Clo/Desktop/LAB/___DAILYRESULT___.csv'
    excel_path='C:/Users/Clo/Desktop/LAB/DATA.xlsx'
    excel_path_to_open='C:/Users/Clo/Desktop/LAB/LAB_DAILY_REPORT- REF.xlsx'
    excel_new_path_name ='C:/Users/Clo/Desktop/LAB/Daily_reports/LAB_DAILY_REPORT-'+ datetime.datetime.today().strftime('%Y-%m-%d') +'.xlsx'

    #excel_path_new='C:/Users/Clo/Desktop/LAB/Lab_daily_report - '+ datetime.datetime.today().strftime('%Y-%m-%d') +'.xslx'
    #excel_path_new='C:/Users/Clo/Desktop/LAB/Lab_daily_report - 15.xslx'
    sheet='data'
    df=pd.read_csv(data_to_copy, delimiter=';', encoding='utf-8-sig')
    print("nouvelles donnees à copier df")
    print(df.shape)
    data_old = pd.read_excel(excel_path)
    print("anciennes donnees DATA")
    print(data_old.shape)


    columns=['id_sortie','dentiste','centre','groupe dentaire','zone','contenu','date_saisie_dentiste','date_prise_en_charge','date_lecture_retour',
            'delai total depuis édition bon','Label délai entre édition bon et lecture retour',
            'delai saisie dentiste _ prise en charge labo','label delai prise en charge','délai prise en charge labo_lecture retour',
             'Retard','Sortie','semaine', 'mois','year','partenaire']

    data_new=pd.concat([df, data_old], ignore_index=True)

    print("donnees concatenees")
    print(data_new.shape)
    # Keep only LAST record from set of duplicates
    data_new=data_new.drop_duplicates(keep="last")
    print("donnees dedoublonnees")
    print(data_new.shape)
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        data_new.to_excel(writer, sheet_name='data',index=False, columns=columns, startrow=0, startcol=0)
        writer.save()
    #writer.close()
    #data_new.to_excel(excel_path, index=False)

    xl = Dispatch("Excel.Application")
    xl.Visible = True # otherwise excel is hidden
    #xl.DisplayAlerts = False
    # newest excel does not accept forward slash in path
    wb = xl.Workbooks.Open(excel_path_to_open)
    time.sleep(60)
    wb.Close(True)
    #wb.Close()
    #xl.DisplayAlerts = True
    xl.Quit()


    shutil.copyfile(excel_path_to_open, excel_new_path_name)

    #writer.close()
    #writer = pd.ExcelWriter(excel_path,engine='openpyxl',mode='a',if_sheet_exists='overlay')


    #engine='xlsxwriter'






    #engine='io.excel.xlsm.writer'

    #
    # workbook = writer.book
    #
    # workbook.filename =
    # #workbook.add_vba_project('C:/Users/Clo/Desktop/LAB/vbabin folder/xl/vbaProject.bin')
    t1 = time.time()
    total=t1-t0
    #print(total)
    print("copy_to_excel: fin")
    return
#copy_to_excel()

    #os.remove(excel_path)
    #os.system("TASKKILL /F /IM Excel.exe")