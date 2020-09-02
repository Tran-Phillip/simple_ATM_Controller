# Simple ATM Controller

## How to Install
------------------
### Requirements 
- Docker 
------
First clone the repo. Then type
```
docker build . -t <your tag name> 
```
Once it's finished building you can access the enviorment by using

```
docker run -it <your tag name> 
```

## Test Webserver 
----
To test the controller, I made a little spoof webserver in Go that pretends to be a backend. I know I didn't need to do this, but I am a very visual person and I really prefer seeing my code execute. The dockerfile automatically starts the test web server, (using localhost:8080) so don't worry about that file.

## Usage 
------
To run the Test Suite, first bring up our spoof web server then run our test suite in the container
```
go run test_webserver.go &
python3 ATM_Unit_Test_suite.py -v
```
It should run all the tests for you.

The main file is Controller.py, and that contains the class definitions and methods for our controller class. You can mess around with that file however you want as long as you are inside the container.

## test_card_pins.txt
---
These are the test card, pin, accounts, and balances I use for my test suite. The format of each row is
```
card_number,pin_number,Account1|Account2|Account3,Balance1,Balance2,Balance3
```
if you wanted to add your own. 

## Assumptions
----
I made a couple of assumptions for this project. 

1) The atm will connect to some sort of server in order to get information like balance info or to do deposits. 
2) Enforced that some members have to be in the body response. For example: when validating if a pin is correct. I expect the backend to take care of the validation and to send the controller a "is_pin_valid" key inside it's response that contains whether or not the pin was valid. 
3) There is a strict order of operations for the user 
- Insert card => Type Pin number => Select Account => Execute action <br> The reason I mention this is because for some test cases I don't bother testing for certain things because if the user has reached a certain stage in the process, it is a given that the previous stages were valid. For example: during the "Select Account" implimentation, I don't check to see if the user has a valid card because when the user types in their pin, I enforce that the card must be valid at that step. 
## Some Design Decisions 
---
I decided to make everything request based because I think it'd be nicer for integration for a real bank. The issue is that my endpoints right now are pointing to the test_webserver that I made for testing so someone would have to go in and change the endpoints. I also enforce things that a bank might not enforce, for example when getting the accounts from a card, I enforce that they will be obtained from the response of an api call and contain a key \<accounts\>. However a bank may not do it this way. Fortunately it is a easy fix as one would just need to change the key or remove the assert all together if its unnecesary. 

