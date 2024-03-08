package main

import (
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"

	progressbar "github.com/schollz/progressbar/v3"
)

func try(err error) {
	if err != nil {
		panic(err)
	}
}

func GetUrls() []string {
	dataOfFile, err := os.ReadFile("urls.txt")
	try(err)
	rawStringData := string(dataOfFile)
	var urls = strings.Split(rawStringData, "\n")
	return urls
}

func SetUrls(url string) bool {
	dataOfFile, err := os.ReadFile("urls.txt")
	try(err)
	rawStringData := string(dataOfFile)
	isContains := strings.Contains(rawStringData, url)
	file, err := os.OpenFile("urls.txt", os.O_APPEND, 0644)
	try(err)
	defer func() {
		file.Close()
	}()

	if !isContains {
		_, err = file.WriteString(fmt.Sprintf("%s\n", url))
		try(err)
	}

	return isContains
}

// io.Copy(io.MultiWriter(f, bar), resp.Body)

func SendRequest(url string) {
	response, err := http.Get(url)
	if err != nil {
		return
	}

	bar := progressbar.DefaultBytes(
		-1,
		strings.TrimSpace(url),
	)
	io.Copy(io.MultiWriter(bar), response.Body)

}

func main() {
	url := flag.String("u", "", "Enter a url for add")
	flag.Parse()
	if *url != "" {
		isDup := SetUrls(*url)
		if isDup {
			fmt.Println("Duplicate: ", *url)
		} else {
			fmt.Println("Successfully Added: ", *url)
		}
		os.Exit(0)
	}

	urls := GetUrls()

	for {
		for _, url := range urls {
			SendRequest(strings.TrimSpace(url))
		}
	}

}
