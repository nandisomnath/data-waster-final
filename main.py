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
    size = 2 * 1024
    total_size_in_bytes = int(res.headers.get('Content-Length', 0))
    
    for data in tqdm(res.iter_content(size), 
                          desc='Data Wasting', 
                          total=total_size_in_bytes // size, 
                          unit='KB'):
        pass
    
    res.close()
    
    return (canDownloaded, total_size_in_bytes)



if __name__ == "__main__":
    api_url = "https://testing-one-orpin.vercel.app"
    file =open("urls.txt", "r")
    urls = []
    for x in file:
        urls.append(x.strip())
    file.close()
    # for testing only
    # url = "https://download.visualstudio.microsoft.com/download/pr/d601fb18-a930-4042-82f7-a8fb9965f3ec/7d6c1f7945b0f587cd06e74c6e11d3fe/microsoft-jdk-21.0.2-windows-x64.msi"
    
    # total_size_in_gb =  float(requests.get(f"{api_url}/usage").json()["value"])
    total_size_in_gb = read_file()
    firstTime = True
    print("Total Download Completed: {} GB".format(total_size_in_gb))
    while True:
        try:
            for url in urls:
                dataTuple = download(url)
                canDownloaded = dataTuple[0]
                if canDownloaded:
                    total_size_in_gb = total_size_in_gb + float(dataTuple[1]) / float(1024 * 1024 * 1024)
                    if total_size_in_gb != 0.0 or firstTime:
                        # updating api
                        update_file(total_size_in_gb)
                        firstTime = False
                    value = read_file()
                    print(f"Completed Amount : {value:.2f} GB")
                
        except Exception as e:
            print("Downloading error occured...")
            print(e)