import requests


def download(url_path):
    # print("Starting download..")
    res = requests.get(url_path, stream=True)
    for data in res.iter_content(chunk_size=1024):
        # print(data)
        pass
    if res.status_code != 200:
        print("Download Error.. ")


if __name__ == "__main__":
    url = "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-desktop-amd64.iso"
    for i in range(1, 23):
        print(f"Downloading {i} no. file ")
        download(url)
    # download(url)
