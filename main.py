import requests
import time
import argparse


B = 1
KB = B * 1024
MB = KB * 1024
GB = MB * 1024


def get_limit_size(max_speed, percentage_speed_limit):
    # returns a size/sec in bytes
    if percentage_speed_limit > 100:
        print("Using speed limit greater then 100% ")
        return None
    
    user_speed_limit = (
        (percentage_speed_limit) / 100 # 0.x
        * max_speed # 6 mb/s * 0.x
        * MB
    )

    # user_speed_limit = (
    #     (percentage_speed_limit) / 100 
    #     * max_speed
    #     / 8
    #     * MB
    # )
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
    
    total_size_in_gb = total_size_in_gb + float(total_size_in_bytes) / float(GB)
    print("Total Download Completed: {:.2f} GB".format(total_size_in_gb))
    update_file(total_size_in_gb)
    


def download(url_path, max_speed, percentage_limit):
    """
    @param max_speed  MB/s unit
    """
    res = requests.get(url_path, stream=True, timeout=2)
    print(f"{res.status_code} => {url}")

    if res.status_code != 200:
        return
    
  
    total_size_in_bytes = int(res.headers.get("Content-Length", 0))
    chunk_size = get_limit_size(max_speed, percentage_limit)
    downloaded_bytes = 0
    start = time.time()

    for stream in res.iter_content(chunk_size=chunk_size):

        end = time.time()

        # count the percentage
        downloaded_bytes += chunk_size
        percentage = (downloaded_bytes / total_size_in_bytes) * 100
        
        duration = end - start
        current_chunk_size = len(stream)
        speed = current_chunk_size / duration / MB

        print(f"Download: {percentage:.2f}% ({speed:.2f}MB/s) \r", end="")
        if duration < 1:
            time.sleep(1 - duration)

        
        start = time.time()

        # if percentage_limit != 100:
            
        
    res.close()
    

    # Download is complete 
    update_record(total_size_in_bytes)
    return


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="A data waster for the time",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                     )

    parser.add_argument("-m", "--max",type=float, default=1.0,  help="max speed of your internet connection in MB/s unit")
    parser.add_argument("-l", "--limit",type=int, default=100, help="Limit of the downloading speed in percentage [1..100]")

    args = parser.parse_args()

    max_speed = args.max
    percentage_limit = args.limit
    


    file = open("urls.txt", "r")
    urls = []
    for x in file:
        urls.append(x.strip())
    file.close()


    while True:
            for url in urls:
                # a protecting layer for the blank lines
                if url == '':
                    continue
                try:
                    download(url, max_speed, percentage_limit)
                except requests.exceptions.ConnectionError as e:
                    # when there is not internet or any connection
                    pass
                except requests.exceptions.ChunkedEncodingError as e:
                    # When not able to download full
                    pass
                