package main

import (
	"fmt"
	"log"
	"net/http"
	"bufio"
	"os"
    "strings"
    "encoding/json"
    "github.com/gorilla/mux"
    "strconv"
    "io/ioutil"
)

var card_pin_map = make(map[string]string) // map that will contain our card pin mappings
var card_accounts_map = make(map[string][]string) // map that contains our card_accounts_map
var card_balance_map = make(map[string]map[string]int) // map that contains our card to balance mappings

type pinPayload struct {
    Is_valid_pin bool `json:"is_valid_pin"`
}

type pinPayloadBad struct {
    Blah bool `json:"Blah"`
}

type accountPayload struct { 
    Accounts []string `json: "accounts"`
}

type accountPayloadBad struct { 
    Blah []string `json: "Blah"`
}

type balancePayload struct { 
    Balance int `json: "balance"`
}

func homePage(w http.ResponseWriter, r *http.Request){
    fmt.Fprintf(w, "Welcome to the HomePage!")
}

func cardEndpoint(w http.ResponseWriter, r *http.Request) { 
    w.Header().Set("Content-Type", "application/json")

    vars := mux.Vars(r)
    card_number := vars["card_number"]

    if(card_number == "BadRequest"){
        w.WriteHeader(http.StatusInternalServerError)
        w.Write([]byte("500 - Something bad happened!"))
        return
    }

    cards := []string{}
    for key, _ := range card_pin_map { 
        if key == card_number {
            cards = append(cards, key)
        }
    }

    json.NewEncoder(w).Encode(cards)
}

func validatePinEndpoint(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    card_number := vars["card_number"]
    pin := vars["pin"]

    if card_number ==  "1234" { // testing invalid response
        json.NewEncoder(w).Encode(pinPayloadBad{Blah: true})
        return
    }

    if val, ok := card_pin_map[card_number]; ok {
        if strings.TrimSpace(val) == strings.TrimSpace(pin) {
            json.NewEncoder(w).Encode(pinPayload{Is_valid_pin: true})
            return
        } else {
            json.NewEncoder(w).Encode(pinPayload{Is_valid_pin: false})
            return
        }
    }

    json.NewEncoder(w).Encode(pinPayload{Is_valid_pin: false})
    return
}

func returnAccountsEndpoint(w http.ResponseWriter, r *http.Request) { 
    vars := mux.Vars(r)
    card_number := vars["card_number"]

    if(card_number == "4444"){
        json.NewEncoder(w).Encode(pinPayloadBad{Blah: true})
        return
    }

    if val, ok := card_accounts_map[card_number]; ok {
        json.NewEncoder(w).Encode(accountPayload{Accounts: val})
    } else {
        w.WriteHeader(http.StatusInternalServerError)
        w.Write([]byte("500 - Something bad happened!"))
    }

}

func balanceEndpoint(w http.ResponseWriter, r *http.Request) { 
    vars := mux.Vars(r)
    card_number := vars["card_number"]
    account := vars["account"]

    if r.Method == http.MethodGet { 
        if card_number == "9999"{ // testing bad response
            json.NewEncoder(w).Encode(pinPayloadBad{Blah: true})
            return
        }
    
        if val, ok := card_balance_map[card_number][account]; ok {
            json.NewEncoder(w).Encode(balancePayload{Balance: val})
        } else{
            w.WriteHeader(http.StatusInternalServerError)
            w.Write([]byte("500 - Something bad happened!"))
        }
    } else if r.Method == http.MethodPut { // I was having issues with Json unmarshal :^(
        body, _ := ioutil.ReadAll(r.Body)

        strBody := string(body) 
        split_body := strings.Split(strBody, "&")

        account := strings.Split(split_body[1], "=")[1]
        balance, _ := strconv.Atoi(strings.Split(split_body[0], "=")[1])

        card_balance_map[card_number][account] = balance
    }
}

func handleRequests() {
    myRouter := mux.NewRouter().StrictSlash(true)
    myRouter.HandleFunc("/", homePage)
    myRouter.HandleFunc("/api/v1/cards/{card_number}", cardEndpoint)
    myRouter.HandleFunc("/api/v1/{card_number}", returnAccountsEndpoint)
    myRouter.HandleFunc("/api/v1/{card_number}/{account}/balance", balanceEndpoint)
    myRouter.HandleFunc("/api/v1/{card_number}/{pin}", validatePinEndpoint)
    log.Fatal(http.ListenAndServe(":8080", myRouter))
}

func main() {


	file, err := os.Open("test_card_pins.txt")
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
		line := scanner.Text()
		split_line := strings.Split(line, ",")
        card_pin_map[split_line[0]] = split_line[1]
    
        split_accounts := strings.Split(split_line[2], "|")
        card_accounts_map[split_line[0]] = split_accounts
        
        checkings, _ := strconv.Atoi(split_line[3])
        savings, _ := strconv.Atoi(split_line[4])
        credit, _ := strconv.Atoi(split_line[5])

        
        card_balance_map[split_line[0]] = make(map[string]int)

        card_balance_map[split_line[0]]["Checkings"] = checkings
        card_balance_map[split_line[0]]["Savings"] = savings
        card_balance_map[split_line[0]]["Credit"] = credit
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }

	fmt.Println("starting the webserver")
    handleRequests()
}