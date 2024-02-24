import requests


def download(url_path):
    canDownloaded = True 
    res = requests.get(url_path, stream=True)
    size = 2 * 1024
    for data in res.iter_content(chunk_size=size):
        pass
    res.close()
    if res.status_code != 200:
        canDownloaded = False
        print("Unable to find file.. ")
    return canDownloaded


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
    while True:
        print(f"Downloading {i} no. file ")

        try:
             canDownloaded = download(url)
             if current_url == len(urls):
                 print("No supported url found..")
             if not canDownloaded:
                 current_url = current_url+1
                 url = urls[current_url]
        except Exception as e:
            print("Downloading error occured...")
            print(e)

        i = i +1
    # download(url)
