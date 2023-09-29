from threading import Timer
import requests
import pandas as pd
from time import localtime, strftime
 
# Inspired by https://datacorner.fr/velib/


durationinsec = 1*60*60
iteration = 1   

def update():
    getData()
    set_timer()
    
def set_timer():
    Timer(durationinsec, update).start()

def main():
    update()

def getData():
    global iteration
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"  # replace with your actual URL
    mytime = strftime("%Y-%m-%d %H:%M:%S", localtime())
 
    resp = requests.get(url)
    if resp.status_code != 200:
        print(mytime, " - ", iteration, " - Error fetching data")
    else:
        data = resp.json()
        dff = pd.DataFrame(columns=['Timer', 'Station Code', 'Station ID', 'Number of Bikes Available',
                                    'Number of Mechanical Bikes', 'Number of Ebikes', 'Number of Docks Available',
                                    'Is Installed', 'Is Returning', 'Is Renting', 'Last Reported'])
        for station in data['data']['stations']:
            num_mechanical = 0
            num_ebike = 0
            for bike_type in station['num_bikes_available_types']:
                if 'mechanical' in bike_type:
                    num_mechanical = bike_type['mechanical']
                if 'ebike' in bike_type:
                    num_ebike = bike_type['ebike']
            
            dff.loc[len(dff)] = [mytime,
                                 station['stationCode'],
                                 station['station_id'],
                                 station['num_bikes_available'],
                                 num_mechanical,
                                 num_ebike,
                                 station['num_docks_available'],
                                 station['is_installed'],
                                 station['is_returning'],
                                 station['is_renting'],
                                 station['last_reported']]
        if len(dff) > 0:
            with open("velib_batch_parheure.csv", 'a') as f:
                dff.to_csv(f, header=True, index=False)
                print(mytime, " - ", iteration, " - Data fetching complete. Number of records fetched: ", len(dff))
        else:
            print(mytime, " - ", iteration, " - No data to fetch.")
    iteration = iteration + 1

 
if __name__ == "__main__":
    main()