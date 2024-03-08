package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
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
	defer file.Close()

	if !isContains {
		// os.WriteFile("urls.txt", []byte(), os.ModeAppend)
		_, err = file.WriteString(fmt.Sprintf("%s\n", url))
		try(err)
	}

	return isContains
}

func SendRequest(url string) {
	response, err := http.Get(url)
	if err != nil {
		return
	}
	reader := bufio.NewReader(response.Body)
	var buffer = make([]byte, 2048)
	_, err = reader.Read(buffer)

	for err != io.EOF {
		if err != nil {
			return
		}
		_, err = reader.Read(buffer)
	}
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
