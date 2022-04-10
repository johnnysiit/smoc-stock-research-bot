import dictionary_making as dm
import pandas as pd
import time
all_tickers = open("./Tickers.txt", "r").readlines()
tickers = []
for i in all_tickers:
    tickers.append(i.strip())
final_data = dict()
tickers.sort()
for j in tickers:
    all_data = dm.data_dictionary(0,j,2)
    try:
        final_data[j] = all_data["Total_Avg_Grading"]
    except:
        final_data[j] = "0.00"
    print ("%4s : %1.2f"%(j,final_data[j]))
    time.sleep(25)
df = pd.DataFrame(final_data)
df.to_excel("ranking.xlsx")
