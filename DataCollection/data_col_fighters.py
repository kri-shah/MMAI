from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd
from queue import Queue
import time 

class Data_Scalping:
    def __init__(self):
        self.links = []

    def get_links(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # Find the table containing fighter information
        table = soup.find("table", {"class": "b-statistics__table"})
        # Find all links within the table rows
        links = table.find_all("a", href=True)
        # Extract href attribute from each link and append to self.links
        for link in links:
            self.links.append(link["href"])

#print(f"Name:{name}; Height:{height}; Weight:{weight}; Reach:{reach}; Stance:{stance}; DOB:{BD}")
#print(f"SLpM:{SLpM}; StAC:{StAC}; SApM:{SApM}; TDAVG:{td_Avg}; TDACC:{td_ACC}; TDDEF:{TDDEF}; SUBAVG:{SUBAVG}") 
    def collect_f_stats(self):
        count = 0
        name_list = []
        height_list = []
        weight_list = []
        reach_list = []
        stance_list = []
        DOB_list = []
        SLpM_list = []
        StAC_list = []
        SApM_list = []
        TD_AVG_list = []
        TDACC_list = []
        TDDEF_list = []
        SUBAVG_list = []
        record_list = []
        for link in self.links:
            url = link
            url_content = urlopen(url)
            mybytes = url_content.read()

            mystr = str(mybytes.decode("utf8"))
            url_content.close()
            
            name_indx = mystr.find("b-content__title-highlight") + 28
            if name_indx > -1:
                name = mystr[name_indx:name_indx+40]
                name = " ".join(name.split())

            height_indx = mystr.find("Height") +19
            if name_indx > -1:
                height = mystr[height_indx:height_indx+11]
                height = " ".join(height.split())

            weight_indx = mystr.find("Weight") +19
            if name_indx > -1:
                weight = mystr[weight_indx:weight_indx+10]
                weight = " ".join(weight.split())

            reach_indx = mystr.find("Reach") +19
            if name_indx > -1:
                reach = mystr[reach_indx:reach_indx+7]
                reach = " ".join(reach.split())

            stance_indx = mystr.find("STANCE") +19
            if name_indx > -1:
                stance = mystr[stance_indx:stance_indx+19]
                stance = " ".join(stance.split())
                if "</li>" in stance:
                    stance = "--"
                if "Switch" in stance:
                    stance = "Switch"

            DOB_indx = mystr.find("DOB:") +25
            if DOB_indx > -1:
                BD = mystr[DOB_indx:DOB_indx+18]
                BD = " ".join(BD.split())

            SLpM_indx = mystr.find("SLpM:") +25
            if DOB_indx > -1:
                SLpM = mystr[SLpM_indx:SLpM_indx+18]
                SLpM = " ".join(SLpM.split())
            
            StAC_indx = mystr.find("Str. Acc")+26
            if StAC_indx > -1:
                StAC = mystr[StAC_indx:StAC_indx+12]
                StAC = " ".join(StAC.split())
                if StAC == "0%":
                    StAC = "0"

            SApM_indx = mystr.find("Str. Def:") +26
            if SApM_indx > -1:
                SApM = mystr[SApM_indx:SApM_indx+11]
                SApM = " ".join(SApM.split())
                if SApM == "0%":
                    SApM = "0"
            
            TDAVG_indx = mystr.find("TD Avg.:") + 26
            if TDAVG_indx > -1:
                td_Avg = mystr[TDAVG_indx:TDAVG_indx+12]
                td_Avg = " ".join(td_Avg.split())
            
            TDACC_indx = mystr.find("TD Acc.:") + 26
            if TDACC_indx > -1:
                td_ACC = mystr[TDACC_indx:TDACC_indx+10]
                td_ACC = " ".join(td_ACC.split())
                if td_ACC == "0%":
                    td_ACC = "0"
            
            TDDEF_indx = mystr.find("TD Def.:") + 26
            if TDDEF_indx > -1:
                TDDEF = mystr[TDDEF_indx:TDDEF_indx+10]
                TDDEF = " ".join(TDDEF.split())
                if TDDEF == "0%":
                    TDDEF = "0"

            SUBAVG_indx = mystr.find("Sub. Avg.:") + 26
            if SUBAVG_indx > -1:
                SUBAVG = mystr[SUBAVG_indx:SUBAVG_indx+20]
                SUBAVG = " ".join(SUBAVG.split())
                if SUBAVG == "0%":
                    SUBAVG = "0"
            
            r_indx = mystr.find("Record:") +7
            if r_indx > -1:
                r = mystr[r_indx:r_indx+9]
                r= r.replace('(', '')
                r = " ".join(r.split()) 
                

            name_list.append(name)
            height_list.append(height)
            weight_list.append(weight)
            reach_list.append(reach)
            stance_list.append(stance)
            DOB_list.append(BD)
            SLpM_list.append(SLpM)
            StAC_list.append(StAC)
            SApM_list.append(SApM)
            TD_AVG_list.append(td_Avg)
            TDACC_list.append(td_ACC)
            TDDEF_list.append(TDDEF)
            SUBAVG_list.append(SUBAVG)
            record_list.append(r) 
            
            print(f"Name:{name}; Height:{height}; Weight:{weight}; Reach:{reach}; Stance:{stance}; DOB:{BD}; Record:{r}")
            count +=1
            #if count == 20:
            #    break
        data = {
            "Name": name_list,
            "Height": height_list,
            "Weight": weight_list,
            "Reach": reach_list,
            "Stance":stance_list,
            "DOB":DOB_list,
            "SLpM":SLpM_list,
            "StAC":StAC_list,
            "SApM":SApM_list,
            "TDAVG":TD_AVG_list,
            "TDACC":TDACC_list,
            "TDDEF":TDDEF_list,
            "SUBAVG":SUBAVG_list,
            "Record":record_list
        }
        
        df = pd.DataFrame(data)
        df.to_csv(r"Fighter_Stats4.csv", index=True)

        print(df)

        #print(f"Name:{name_list}; Height:{height_list}; Weight:{weight_list}; Reach:{reach_list}; Stance:{stance_list}; DOB:{DOB_list}")
        #print(f"SLpM:{SLpM_list}; StAC:{StAC_list}; SApM:{SApM_list}; TDAVG:{TD_AVG_list}; TDACC:{TDACC_list}; TDDEF:{TDDEF_list}; SUBAVG:{SUBAVG_list}") 

    def remove_duplicates(self):
        self.links = list(set(self.links))

    def print_data(self):
        for i, link in enumerate(self.links):
            print(f"{i} {link}")
        print(f"len is {len(self.links)}")

if __name__ == '__main__':
    start = time.time()
    data = Data_Scalping()
    
    links = []
    for x in range(26):
        temp = chr(97 + x)
        url = f"http://www.ufcstats.com/statistics/fighters?char={temp}&page=all"
        data.get_links(url)

    data.remove_duplicates() 
    #data.print_data()
    data.collect_f_stats()
    end = time.time()
    print(f"Time spent was {(end - start) / 60} min")
    
