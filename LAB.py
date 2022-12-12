import time
import datetime

def collect_daily_data(date_input):
  import pandas as pd
  import numpy as np
  import datetime
  import chromedriver_autoinstaller
  from selenium import webdriver
  from selenium.webdriver.common.by import By
  from selenium.webdriver.support.ui import Select
  from selenium.webdriver.chrome.service import Service
  import dateutil.parser as dparser
  import datetime
  import os
  import glob

#installe le bon driver si celui ci ne correspond pas au chrome actuel
  chromedriver_autoinstaller.install()

  date_input_form='"' + str(date_input.day) + '/' + str(date_input.month) + '/' + str(date_input.year) + '"'
  #service = Service('C:/Users/Clo/Downloads/chromedriver_win32/chromedriver.exe')
  #service=service
  driver = webdriver.Chrome()
  options = webdriver.ChromeOptions()
  options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
  options.add_argument('headless')
  options.add_argument('window-size=0x0')
  #driver.maximize_window()
  driver.get("https://www.logidents.com/login.php")
  user_name = driver.find_element(By.ID, "logUSE")
  pwd = driver.find_element(By.ID, "logPWD")
  user_name.send_keys("madiermaxime@gmail.com")
  pwd.send_keys("LABO2022")
  login = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/form/div[4]/button")
  login.click()
  driver.get("https://www.logidents.com/orgsor.php")
  select_date= driver.find_element(By.ID,"staSTR")
  select_date.clear()
  select_date.send_keys(date_input_form)
  valider=driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div/div/div[1]/div/form/div/table/tbody/tr/td[1]/div/span[2]/button")
  valider.click()

  #loop sur chaque page si tableau est sur plusieurs plages
  infos_pages_text=driver.find_element(By.XPATH,'//*[@id="exRowTable_info"]').text

  #teste si données dispos
  if(infos_pages_text=='Rien à afficher'):return
  infos_pages= [int(s) for s in infos_pages_text.split() if s.isdigit()]
  print(infos_pages)
  column_names = ["id_sortie", "date_prise_en_charge", "dentiste", "centre", "contenu", "date_saisie_dentiste",
                  "date_prise_en_charge_labo", "date_lecture_arrivee", "date_lecture_retour","partenaire"]
  df2 = pd.DataFrame(columns=column_names)
  df2.set_index(column_names, drop=True, append=True, inplace=False, verify_integrity=True)

  while (infos_pages[1]<=infos_pages[2]):

    rows = len(driver.find_elements(By.XPATH,"//*[@id='exRowTable']/tbody/tr"))

    for t_row in range(1, rows+1):
      if (t_row==rows):
        testt=1
      FinalXPath = "//*[@id='exRowTable']/tbody/tr[" + str(t_row) +"]/td"

      data_num= driver.find_element(By.XPATH,"//*[@id='exRowTable']/tbody/tr[" + str(t_row) +"]").get_attribute("data-num")
      id_sortie= driver.find_element(By.XPATH,FinalXPath+"[3]").text
      print(id_sortie)

      if id_sortie=="837082" :
        verif=1
      date_prise_charge=driver.find_element(By.XPATH,FinalXPath+"[4]").text
      dentiste = driver.find_element(By.XPATH, FinalXPath + "[5]").text
      try:
        centre= driver.find_element(By.XPATH, FinalXPath + " [5]/small/a").text
      except Exception:
        centre=''
      partenaire=driver.find_element(By.XPATH, FinalXPath + "[7]").text
      contenu = driver.find_element(By.XPATH, FinalXPath + "[11]").text
      id_click = driver.find_element(By.XPATH, '//*[@id="exRowTable"]/tbody/tr[' +str(t_row)+']/td[1]')
      driver.execute_script("arguments[0].click();", id_click )
      #initialisation des variables dates

      date_saisie_dentiste=""
      date_prise_charge_labo=""
      date_lecture_retour=""
      date_lecture_arrivee=""
      date_recuperee=""
      erreur=0

      #récupération des dates, il peut y avoir 3 lignes à récupéer ou 4 suivant que la prothese soit envoyée en labo externe
      for i in range(1,8):
        while True:
          try:
            date_recuperee=driver.find_element(By.XPATH,'//*[contains(@id, "bon_eta")]/div/div[1]/small['+str(i)+']').text.replace('-',' ')
            #date_recuperee = driver.find_element(By.XPATH, '//*[contains(@id, "' + data_num[data_num.find(
             # '-')::] + '")]/div/div[1]/small[' + str(i) + ']').text.replace('-', ' ')
            erreur=0
            break
          except Exception:
            try:
              date_recuperee = driver.find_element(By.XPATH, '//*[contains(@id, "bon_eta")]/div/div/b/small[' + str(i) + ']').text.replace('-', ' ')
              erreur = 0
              break
            except Exception:
              erreur=1
              break
        if erreur==1:
          break


        if date_recuperee.find('Saisie le')!=-1:
          date_saisie_dentiste=date_recuperee
          date_saisie_dentiste = dparser.parse(date_saisie_dentiste.replace('March','Marchi').replace('MAY','Mayo'),fuzzy=True, dayfirst=True)
        elif date_recuperee.find('Pris en charge')!=-1:
          date_prise_charge_labo = date_recuperee
          date_prise_charge_labo = dparser.parse(date_prise_charge_labo, fuzzy=True, dayfirst=True)
        elif date_recuperee.find('Lecture en retour ')!=-1:
          date_lecture_retour = date_recuperee
          date_lecture_retour = dparser.parse(date_lecture_retour[:date_lecture_retour.find('Délai') - 1], fuzzy=True, dayfirst=True)
        else:
          date_lecture_arrivee =  date_recuperee
          date_lecture_arrivee= dparser.parse(date_lecture_arrivee, fuzzy=True, dayfirst=True)


      id_click1 = driver.find_element(By.XPATH, '//*[@id="exRowTable"]/tbody/tr[' + str(t_row) + ']/td[1]')
      driver.execute_script("arguments[0].click();", id_click1)

      values_to_add = pd.DataFrame(np.column_stack([id_sortie,date_prise_charge,dentiste ,centre,contenu,date_saisie_dentiste,date_prise_charge_labo,date_lecture_arrivee,date_lecture_retour,partenaire]),
                                     columns=["id_sortie","date_prise_en_charge", "dentiste","centre", "contenu","date_saisie_dentiste","date_prise_en_charge_labo","date_lecture_arrivee","date_lecture_retour","partenaire"])

      df2=df2.append(values_to_add,ignore_index=True)

    if (infos_pages[1]<infos_pages[2]):
      page_suivante = driver.find_element(By.XPATH, '// *[ @ id = "exRowTable_next"] / a')
      page_suivante.click()
      infos_pages_text = driver.find_element(By.XPATH, '//*[@id="exRowTable_info"]').text
      infos_pages = [int(s) for s in infos_pages_text.split() if s.isdigit()]
    else:
      break

  print(df2)
  print(df2.count())
  jour=str(date_input.day)
  mois=str(date_input.month)
  annee=str(date_input.year)
  if len(jour) == 1:
    jour = '0' + jour
  if len(mois) == 1:
    mois = '0' + mois
  csv_name=annee+mois+jour
  #csv_name=date_input.replace('/','-').replace('"','')
  df2.to_csv("//CDSO-BUR/Users/Clo/Desktop/LAB/result_"+csv_name+".csv", sep=';', index=False, encoding='utf-8-sig')
  driver.quit()


  return

#   #merger les csv
# def merge_csv():
#   import os
#   import glob
#   import pandas as pd
#   os.chdir("C:/Users/Clo/Desktop/LAB")
#   extension = 'csv'
#   #all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#   all_filenames = [i for i in glob.glob('C:/Users/Clo/Desktop/LAB/result*.csv')]
#   # combine all files in the list
#   combined_csv = pd.concat([pd.read_csv(f, delimiter=';', encoding='utf-8-sig') for f in all_filenames])
#   print(combined_csv)
#   # export to csv
#   combined_csv.to_csv("C:/Users/Clo/Desktop/LAB/combined_csv.csv", index=False,sep=';',encoding='utf-8-sig')
#

#now = datetime.datetime.today()
#collect_daily_data( datetime.date(now.year, now.month, now.day))