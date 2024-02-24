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
    urls = [
        "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-desktop-amd64.iso",
        "https://mirrors.nxtgen.com/linuxmint-mirror/iso/stable/21.3/linuxmint-21.3-cinnamon-64bit.iso",
        "https://kali.download/base-images/kali-2023.4/kali-linux-2023.4-live-amd64.iso",
        "https://download-cdn.jetbrains.com/idea/ideaIC-2023.3.4.exe",
        "https://debian.mirror.digitalpacific.com.au/debian-cd/current/amd64/iso-cd/debian-12.5.0-amd64-netinst.iso",
        "https://mirror.4v1.in/archlinux/iso/2024.02.01/archlinux-2024.02.01-x86_64.iso",
        
    ]
    url = urls[0]
    i = 0
    current_url = 0
    total_size_in_mb = 0
    while True:
        try:
             dataTuple = download(url)
             total_size_in_mb = total_size_in_mb + (dataTuple[1] // (1024*1024))
             canDownloaded = dataTuple[0]
             if current_url == len(urls):
                 print("No supported url found..")
             if not canDownloaded:
                 current_url = current_url+1
                 url = urls[current_url]
             else:
                 print(f"Completed Amount : {total_size_in_mb} MB")
        except Exception as e:
            print("Downloading error occured...")
            print(e)

        i = i +1
    # download(url)
