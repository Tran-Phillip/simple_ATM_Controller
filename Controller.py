
import requests as res
class BankController:
    def __init__(self):
        self.currently_used_card = None
        self.valid_pin = False
    
    def validate_card(self, card_number):
        '''
        Takes the card number from the scanner and checks to see if it exists in our system. Then if valid, set the <currently_used_card> to the card_number and return True, 
        else return false

        @params
        card_number (string) => the card number that was inserted

        @returns
        (bool) => True if valid card, False if invalid
        '''
        CARD_ENDPOINT = "http://localhost:8080/api/v1/cards/" + card_number 
        
        r = res.get(CARD_ENDPOINT)
        if(r.status_code != 200 ):
            raise AssertionError("Status code was not 200. Instead: "+ str(r.status_code))
            
        json_body = r.json()

        if(len(json_body) == 0):
            return False 

        self.currently_used_card = card_number
        return True 

    def validate_pin(self, pin_number):
        '''
        Takes the user typed pin and compares it to what our system says the pin should be for the <currently_used_card>.
        If the comparison is True we will return True and set the <valid_pin> member to True. Else return False
        
        For security purposes, this function should NOT
        return the pin as part of the body in order to validate, but rather the api should 
        do the comparison in the backend and return to us in the response <is_valid_pin>

        @errors
        Throws an AssertionError if the response body does not contain <is_valid_pin> key

        @params:
        pin_number(string) => The pin number the user typed 

        @returns:
        (bool) => True if pin is valid, else False 
        '''
        if (self.currently_used_card is None): 
            raise AssertionError("currently_used_card == None")
        
        PIN_VALIDATE_ENDPOINT = "http://localhost:8080/api/v1/" + self.currently_used_card + "/" + pin_number
        r = res.get(PIN_VALIDATE_ENDPOINT)

        if(r.status_code != 200):
            raise AssertionError("Status code was not 200. Instead: " + str(r.status_code))

        json_data = r.json()
        try:
            valid = json_data['is_valid_pin']
            self.valid_pin = valid
            return valid 
        except KeyError:
            raise AssertionError("<is_valid_pin> is not a part of the response body. FULL BODY: " + str(json_data))


    def return_accounts(self):
        '''
        Persuming that all validation checked out beforehand, this function will make an api request 
        to get all the accounts for the <currently_used_card>.

        @errors
        Throws an AssertionError if 
          - the response body does not contain <accounts> key 
          - <currently_used_card> is None or <valid_pin> is None
          - response.status_code is not 200

        @params:
        None, but uses <currently_used_card>

        @returns 
        (list) => all the accounts assosiated with this card number 
        '''

        if (self.currently_used_card is None or not self.valid_pin): # Do not let user proceed unless the card and pin are valid
            raise AssertionError("currently_used_card == None or self.valid_pin == False")

        ACCOUNTS_ENDPOINT = "http://localhost:8080/api/v1/" + self.currently_used_card

        r = res.get(ACCOUNTS_ENDPOINT)

        if(r.status_code != 200):
            raise AssertionError("Status code was not 200. Instead: "+ str(r.status_code))

        json_data = r.json()

        try:
            accounts = []
            for account in json_data['Accounts']:
                accounts.append(account)
            return accounts
        except KeyError:
            raise AssertionError("<Accounts> not found in response body. FULL BODY: " + str(json_data))

    def see_balance(self, account):
        '''
        Checks the balance of the account selected by the user from the UI

        @errors:
        Throws an AssertionError if 
          - the response body does not contain <balance> key 
          - <currently_used_card> is None or <valid_pin> is None
          - response.status_code is not 200

        @params
        account (string) => the account the user wants to see the balance of 

        @returns
        (int) => The amount of money in a account
        '''
        if (self.currently_used_card is None or not self.valid_pin): # Do not let user proceed unless the card and pin are valid
            raise AssertionError("currently_used_card == False or self.valid_pin == False")

        BALANCE_ENDPOINT = "http://localhost:8080/api/v1/" + self.currently_used_card+ "/" + account + "/" + "balance"
        r = res.get(BALANCE_ENDPOINT)

        if(r.status_code != 200):
            raise AssertionError("Status code was not 200. Instead: " + str(r.status_code))

        json_data = r.json()
        try:
            return json_data['Balance']
        except KeyError:
            raise AssertionError("<Balance> not found in response body. FULL BODY: " + str(json_data))

    def modify_funds(self, account, amount):
        '''
        Adds or removes munny to an account by making a PUT request 

        @errors:
        Throws an AssertionError if 
          - <currently_used_card> is None or <valid_pin> is None
          - response.status_code is not 200

        @params
        account(string) => the account to update 
        amount(int) => The amount of munny to add or subtract. Use a positive number to add to an account and use a negative number to subtract from it.

        @returns
        (bool) => True if deposit was successful, else throw exception
        '''
        if (self.currently_used_card is None or not self.valid_pin): # Do not let user proceed unless the card and pin are valid
            raise AssertionError("currently_used_card == False or self.valid_pin == False")

        BALANCE_ENDPOINT = "http://localhost:8080/api/v1/" + self.currently_used_card+ "/" + account + "/" + "balance"
        balance = self.see_balance(account)
        r = res.put(BALANCE_ENDPOINT, data = {'Balance': balance + amount, 'Account': account} )

        if(r.status_code != 200):
            raise AssertionError("Status code was not 200. Instead: " + str(r.status_code))
        
        return True

   