import requests
from tqdm import tqdm


def update_file(value):
    file = open("data.txt", "w")
    file.write(f"{value}")
    file.close()


def read_file():
    file = open("data.txt", "r")
    line = file.readline()
    value = float(line.strip())
    file.close()
    return value

def download(url_path):
    canDownloaded = True 
    res = requests.get(url_path, stream=True)
    
    if res.status_code != 200:
        canDownloaded = False
        return (canDownloaded, 0)
    size = 1024 * 1024
    total_size_in_bytes = int(res.headers.get('Content-Length', 0))
    
    td_bar = tqdm(res.iter_content(size), 
                          desc='Data Wasting', 
                          total=total_size_in_bytes // size, 
                          unit='MB',
                          colour='green',
                          mininterval=0.2,
                          leave=True,
                          unit_scale=True)
    t = td_bar.last_print_t
    
    count = 0
    for data in td_bar:
        if td_bar.last_print_t - t >= 1.1: 
            count = count +1
        if count >= 5:
            total_size_in_bytes = 0
            break
        t = td_bar.last_print_t
       
    res.close()
    td_bar.close()
    return (canDownloaded, total_size_in_bytes)



if __name__ == "__main__":
    # api_url = "https://testing-one-orpin.vercel.app"
    file =open("urls.txt", "r")
    urls = []
    for x in file:
        urls.append(x.strip())
    file.close()
    
    total_size_in_gb = read_file()
    firstTime = True
    print("Total Download Completed: {} GB".format(total_size_in_gb))
    while True:
        try:
            for url in urls:
                print(f"=> {url}")
                dataTuple = download(url)
                canDownloaded = dataTuple[0]
                if canDownloaded:
                    total_size_in_gb = total_size_in_gb + float(dataTuple[1]) / float(1024 * 1024 * 1024)
                    if total_size_in_gb != 0.0 or firstTime:
                        # updating api
                        update_file(total_size_in_gb)
                        firstTime = False
                    value = read_file()
                    if dataTuple[1] == 0:
                        continue
                    print(f"Completed Amount : {value:.2f} GB")
                
        except Exception as e:
            print("Downloading error occured...")
            print(e)