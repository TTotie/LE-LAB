

 #merger les csv
def merge_csv():
  import os
  import glob
  import pandas as pd
  import os
  import shutil
  from pathlib import Path



  os.chdir("C:/Users/Clo/Desktop/LAB")
  extension = 'csv'
  #all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
  all_filenames = [i for i in glob.glob('C:/Users/Clo/Desktop/LAB/result*.csv')]

  # combine all files in the list
  combined_csv = pd.concat([pd.read_csv(f, delimiter=';', encoding='utf-8-sig') for f in all_filenames])
  print(combined_csv)
  # export to csv
  combined_csv.to_csv("C:/Users/Clo/Desktop/LAB/combined_csv.csv", index=False,sep=';',encoding='utf-8-sig')
  for f in all_filenames:
    shutil.copy(f, 'C:/Users/Clo/Desktop/LAB/Daily_row_data')
    os.remove(f)
    #shutil.move(f, 'C:/Users/Clo/Desktop/LAB/Daily_row_data')
  print("merge_csv : fin")
  return

#merge_csv()
