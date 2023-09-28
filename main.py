import requests


def download(url_path):
    # print("Starting download..")
    res = requests.get(url_path, stream=True)
    size = 2 * 1024
    for data in res.iter_content(chunk_size=size):
        # print(data)
        pass
    res.close()
    if res.status_code != 200:
        print("Download Error.. ")


if __name__ == "__main__":
    url = "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-desktop-amd64.iso"
    i = 0
    while True:
        print(f"Downloading {i} no. file ")
        download(url)
        i = i +1
    # download(url)
