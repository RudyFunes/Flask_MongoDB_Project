
import requests as requests
import main_functions

def get_key():
    key_dict = main_functions.read_from_file("JSON_Files/Currency_API.json")
    return key_dict["key"]



def Currency():
    url = "http://api.currencylayer.com/live?access_key="  + get_key()
    response = requests.get(url).json()
    return response

def get_Currencies_in_JSON():

    currencies_dict = main_functions.read_from_file("JSON_Files/Currencies.json")
    return  currencies_dict