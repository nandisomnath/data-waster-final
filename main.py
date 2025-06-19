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


def update_record(total_size_in_bytes):
    total_size_in_gb = read_file()
    print("Total Download Completed: {} GB".format(total_size_in_gb))
    total_size_in_gb = total_size_in_gb + float(total_size_in_bytes) / float(
                            1024 * 1024 * 1024
                        )
    update_file(total_size_in_gb)
    


def download(url_path, max_speed, percentage_limit):
    """
    max_speed in Mbs unit like 50 Mbs -> (50 /8) MB/s
    """
    res = requests.get(url_path, stream=True, timeout=5)

    if res.status_code != 200:
        return
    
    print(f"=> {url}")

    total_size_in_bytes = int(res.headers.get("Content-Length", 0))

    td_bar = tqdm(
        desc="Data Wasting",
        total=total_size_in_bytes,
        unit="B",
        colour="green",
        unit_scale=True
    )
    size = get_limit_size(max_speed, percentage_limit) # download size per second in bytes
    for data in res.iter_content(chunk_size=size):
        td_bar.update(len(data))
        if percentage_limit == 100:
            continue
        time.sleep(0.99) # sleep for second to adjust the speed

    res.close()
    td_bar.close()

    # Download is complete 
    update_record(total_size_in_bytes)
    return


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

    
    firstTime = True

    while True:
            for url in urls:
                try:
                    download(url, max_speed, percentage_limit)
                except requests.exceptions.ConnectionError as e:
                    # when there is not internet or any connection
                    pass
                except requests.exceptions.ChunkedEncodingError as e:
                    # When not able to download full
                    pass
                

        # except Exception as e:
        #     print("Downloading error occured...")
        #     print(e)
