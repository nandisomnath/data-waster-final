import requests
from tqdm import tqdm
import time
import argparse


B = 1
KB = B * 1000
MB = KB * 1000
GB = MB * 1000


def get_limit_size(max_speed, percentage_speed_limit):
    # returns a size/sec in bytes
    if percentage_speed_limit > 100:
        print("Using speed limit greater then 100% ")
        return None
    user_speed_limit = (
        (percentage_speed_limit) / 100 
        * max_speed
        / 8
        * MB
    )
    return int(user_speed_limit)


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


def download(url_path, max_speed, percentage_limit):
    """
    max_speed in Mbs unit like 50 Mbs -> (50 /8) MB/s
    """
    canDownloaded = True
    res = requests.get(url_path, stream=True, timeout=20)

    if res.status_code != 200:
        canDownloaded = False
        return (canDownloaded, 0)
   
    total_size_in_bytes = int(res.headers.get("Content-Length", 0))

    td_bar = tqdm(
        desc="Data Wasting",
        total=total_size_in_bytes,
        unit="B",
        colour="green",
        unit_scale=True
    )
    t = td_bar.last_print_t
    # size = MB * 2  # download size per second in bytes
    size = get_limit_size(max_speed, percentage_limit)
    count = 0
    for data in res.iter_content(chunk_size=size):
        td_bar.update(len(data))
        time.sleep(0.99) # sleep for second to adjust the speed
        if td_bar.last_print_t - t >= 1.1:
            count = count + 1
        if count >= 5:
            total_size_in_bytes = 0
            break
        t = td_bar.last_print_t

    res.close()
    td_bar.close()
    return (canDownloaded, total_size_in_bytes)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="A data waster for the time",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                     )

    parser.add_argument("-m", "--max",type=int, default=8,  help="max speed of your internet connection in Mbs unit")
    parser.add_argument("-l", "--limit",type=int, default=100, help="Limit of the downloading speed in percentage [1..100]")

    args = parser.parse_args()

    max_speed = args.max
    percentage_limit = args.limit
    


    file = open("urls.txt", "r")
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
                dataTuple = download(url, max_speed, percentage_limit)
                canDownloaded = dataTuple[0]
                if canDownloaded:
                    total_size_in_gb = total_size_in_gb + float(dataTuple[1]) / float(
                        1024 * 1024 * 1024
                    )
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
