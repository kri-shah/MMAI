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
        table = soup.find("table", {"class": "b-statistics__table-events"})
        # Find all links within the table rows
        links = table.find_all("a", href=True)
        # Extract href attribute from each link and append to self.links
        for link in links:
            self.links.append(link["href"])
    
    


    def get_wins(self):
        fights = []
        total_fights = []
        i = 0 
        for url in self.links:
            #url = "http://ufcstats.com/event-details/c9885b1b7c7055a0"
            page = requests.get(url)

            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find_all("p", class_="b-fight-details__table-text")
            text = [] 
            
            for res in (results):
                t = res.text
                t = " ".join(t.split()) 
                if t == "win" or t == "nc" or t == "draw":
                    if len(text) > 1:
                        if len(text) == 17:
                            text.pop(0)
                        if len(text) >= 16:  # Ensure text has at least 16 elements
                            fights.append(text)
                        text = []
                
                text.append(t)


            if len(text) == 17:
                text.pop(0)
            
            fights.append(text)
            print(url)
        #print(fights)
        t1 = []
        for f in fights:
            if len(f) == 16:
                total_fights.append(f)
            else:
                t1.append(f)
        
        with open("t2", 'w') as file:
                file.write(str(t1))

        df = pd.DataFrame(total_fights, columns=['W/L','WINNER (F1)', 'LOSER (F2)', 'F1 KD', 'F2 KD',
        'F1 STR', 'F2 STR', 'F1 TD', 'F2 TD', 'F1 SUB', 'F2 SUB', 'WEIGHT CLASS','GEN METHOD', 'ACC METHOD', 'ROUNDS','TIME'])
        print(df)
        df.to_csv(r"Fights.csv", index=True) 
    
    def remove_duplicates(self):
        self.links = list(set(self.links))

    def print_links(self):
        for i, link in enumerate(self.links):
            print(f"{i}    {link}")

if __name__ == '__main__':
    start = time.time()
    data = Data_Scalping()
    
    links = []
    
    url = f"http://ufcstats.com/statistics/events/completed?page=all"
    data.get_links(url)
    data.remove_duplicates()
    data.get_wins()
    end = time.time()
    print(f"Total time: {end - start} seconds")
