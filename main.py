import requests
import time
import argparse

B = 1
KB = B * 1000
MB = KB * 1000
GB = MB * 1000


def get_chunk_size(max_speed):
    # returns chunk size in bytes from maxspeed in MB/s
    download_chunk = (max_speed * MB)
    return int(download_chunk)


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
    


def download(url_path, max_speed):
    """
    @param max_speed  MB/s unit
    """
    res = requests.get(url_path, stream=True, timeout=2)
    print(f"{res.status_code} => {url}")

    if res.status_code != 200:
        return
    
  
    total_size_in_bytes = int(res.headers.get("Content-Length", 0))
    chunk_size = MB
    downloaded_in_second = 0
    downloaded_bytes =0
    start = time.time()

    for stream in res.iter_content(chunk_size=chunk_size):
        end = time.time()

        # count the percentage
        fstart = time.time()
        current_chunk_size = len(stream)
        downloaded_in_second += current_chunk_size
        duration = end - start

        if duration >= 1.0:
            downloaded_bytes += downloaded_in_second
            percentage = (downloaded_bytes / total_size_in_bytes) * 100
            speed = (downloaded_in_second / MB) / duration
            print(f"Download: {percentage:.2f}% ({speed:.2f}MB/s) \r", end="")
            downloaded_in_second = 0
            start = time.time()
        else:
            fd = time.time() - fstart
            start -= fd  # adjusting the start time to exclude processing time

    res.close()
    
    # Download is complete 
    update_record(total_size_in_bytes)
    return


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="A data waster for the time",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                     )

    parser.add_argument("-m", "--max",type=float, default=1.0,  help="max speed to waste data in MB/s unit")
    args = parser.parse_args()
    max_speed = args.max

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
                    download(url, max_speed)
                except requests.exceptions.ConnectionError as e:
                    # when there is not internet or any connection
                    pass
                except requests.exceptions.ChunkedEncodingError as e:
                    # When not able to download full
                    pass
                