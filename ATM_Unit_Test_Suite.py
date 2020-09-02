import unittest
from Controller import BankController

class TestControllerMethods(unittest.TestCase):
    def test_controller_instantiation(self):
        controller = BankController()
        self.assertIsNotNone(controller)

    def test_validate_card_OK(self):
        controller = BankController()
        valid = controller.validate_card("5555")
        self.assertEqual(valid, True)

    def test_validate_card_number_does_not_exist(self):
        controller = BankController()
        valid = controller.validate_card("0000")
        self.assertEqual(valid, False)
        
    def test_validate_card_number_bad_request(self):
        controller = BankController()
        self.assertRaises(AssertionError, controller.validate_card, "BadRequest")

    def test_validate_card_number_does_not_exist_nonsense_as_card_number(self):
        controller = BankController()
        valid = controller.validate_card("!!!abd---@@3=moreinvalidcharacters")
        self.assertEqual(valid, False)

    def test_validate_pin_OK(self):
        controller = BankController()
        controller.validate_card("5555")
        valid = controller.validate_pin("3204")
        self.assertEqual(valid, True)
    
    def test_validate_pin_wrong_pin(self):
        controller = BankController()
        controller.validate_card("5555")
        valid = controller.validate_pin("0000")
        self.assertEqual(valid, False)

    def test_validate_pin_did_not_validate_card_first(self):
        controller = BankController()
        self.assertRaises(AssertionError, controller.validate_pin, "0000")

    def test_validate_pin_bad_response(self):
        controller = BankController()
        controller.validate_card("1234")
        self.assertRaises(AssertionError, controller.validate_pin, "1234")

    def test_validate_return_accounts_OK(self):
        controller = BankController()
        controller.validate_card("1929")
        controller.validate_pin("1000")
        accounts = controller.return_accounts()
        self.assertEqual(accounts, ["Checkings","Savings", "Credit"])
    
    def test_validate_return_accounts_OK2(self):
        controller = BankController()
        controller.validate_card("5555")
        controller.validate_pin("3204")
        accounts = controller.return_accounts()
        self.assertEqual(accounts, ["Checkings"])

    def test_validate_return_accounts_wrongPin(self):
        controller = BankController()
        controller.validate_card("1929")
        controller.validate_pin("100")
        self.assertRaises(AssertionError, controller.return_accounts)
    
    def test_validate_return_accounts_no_pin_or_card_number(self):
        controller = BankController()
        self.assertRaises(AssertionError, controller.return_accounts)

    def test_validate_return_accounts_bad_response(self):
        controller = BankController()
        controller.validate_card("4444")
        controller.validate_pin("4444")
        controller = BankController()
        self.assertRaises(AssertionError, controller.return_accounts)

    def test_check_balance_OK(self):
        controller = BankController()
        controller.validate_card("5555")
        controller.validate_pin("3204")
        balance = controller.see_balance("Checkings")
        self.assertEqual(balance, 1000)

    def test_check_balance_OK2(self):
        controller = BankController()
        controller.validate_card("1929")
        controller.validate_pin("1000")
        balance = controller.see_balance("Savings")
        self.assertEqual(balance, 1000)

    def test_check_balance_OK3(self):
        controller = BankController()
        controller.validate_card("2000")
        controller.validate_pin("1010")
        balance = controller.see_balance("Credit")
        self.assertEqual(balance, 3000)
    
    def test_check_balance_WrongValue(self):
        controller = BankController()
        controller.validate_card("2000")
        controller.validate_pin("1010")
        balance = controller.see_balance("Credit")
        self.assertNotEqual(balance, 1000)
    
    def test_check_balance_WrongPin(self):
        controller = BankController()
        controller.validate_card("2000")
        controller.validate_pin("1")
        self.assertRaises(AssertionError, controller.see_balance, "Checkings")
    
    def test_check_balance_no_validation(self):
        controller = BankController()
        self.assertRaises(AssertionError, controller.see_balance, "Checkings")

    def test_check_balance_badResponse(self):
        controller = BankController()
        controller.validate_card("9999")
        controller.validate_pin("9999")
        self.assertRaises(AssertionError, controller.see_balance, "Checkings")

    def modify_funds_OK(self):
        controller = BankController()
        controller.validate_card("5555")
        controller.validate_pin("3204")
        controller.modify_funds("Checkings", 500)
        balance = controller.see_balance("Checkings")
        self.assertEqual(balance, 1500)

    def test_modify_funds_OK_chain(self):
        controller = BankController()
        controller.validate_card("2000")
        controller.validate_pin("1010")
        controller.modify_funds("Checkings", 500)
        controller.modify_funds("Checkings", 1000)
        controller.modify_funds("Checkings", 1000)
        balance = controller.see_balance("Checkings")
        self.assertEqual(balance, 9500)

    def test_modify_funds_no_validation(self):
        controller = BankController()
        self.assertRaises(AssertionError, controller.modify_funds, "Checkings", 1000)

    def test_modify_funds_remove_funds_OK(self):
        controller = BankController()
        controller.validate_card("1929")
        controller.validate_pin("1000")
        controller.modify_funds("Savings", -500)
        balance = controller.see_balance("Savings")
        self.assertEqual(balance, 500)

    def test_modify_funds_add_remove_funds_OK(self):
        controller = BankController()
        controller.validate_card("1662")
        controller.validate_pin("9731")
        controller.modify_funds("Checkings", -500)
        balance = controller.see_balance("Checkings")
        self.assertEqual(balance, 500)
        controller.modify_funds("Checkings", 500)
        balance = controller.see_balance("Checkings")
        self.assertEqual(balance, 1000)

        controller.modify_funds("Checkings", -300)
        balance = controller.see_balance("Checkings")
        self.assertEqual(balance, 700)
        controller.modify_funds("Checkings", 500)
        balance = controller.see_balance("Checkings")
        self.assertEqual(balance, 1200)

if __name__ == '__main__':
    unittest.main()