import requests
from tqdm import tqdm


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
    urls = [
        "https://mirrors.nxtgen.com/linuxmint-mirror/iso/stable/21.3/linuxmint-21.3-cinnamon-64bit.iso",
        "https://kali.download/base-images/kali-2023.4/kali-linux-2023.4-live-amd64.iso",
        "https://download-cdn.jetbrains.com/idea/ideaIC-2023.3.4.exe",
        "https://debian.mirror.digitalpacific.com.au/debian-cd/current/amd64/iso-cd/debian-12.5.0-amd64-netinst.iso",
        "https://mirror.4v1.in/archlinux/iso/2024.02.01/archlinux-2024.02.01-x86_64.iso",
        
    ]
    # for testing only
    # url = "https://download.visualstudio.microsoft.com/download/pr/d601fb18-a930-4042-82f7-a8fb9965f3ec/7d6c1f7945b0f587cd06e74c6e11d3fe/microsoft-jdk-21.0.2-windows-x64.msi"
    
    total_size_in_gb =  float(requests.get(f"{api_url}/usage").json()["value"])
    print("Total Download Completed: {} GB".format(total_size_in_gb))
    while True:
        try:
            for url in urls:
                dataTuple = download(url)
                canDownloaded = dataTuple[0]
                if canDownloaded:
                    total_size_in_gb = total_size_in_gb + float(dataTuple[1]) / float(1024 * 1024 * 1024)
                    if total_size_in_gb != 0.0:
                        # updating api
                        requests.get(f"{api_url}/update/usage/{total_size_in_gb}")
                    res = requests.get(f"{api_url}/usage").json()
                    value = float(res["value"])
                    print(f"Completed Amount : {value:.2f} GB")
                
        except Exception as e:
            print("Downloading error occured...")
            print(e)