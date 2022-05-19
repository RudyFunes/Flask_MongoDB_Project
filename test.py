import json
import main_functions
import api_methods


if __name__ == '__main__':
    currencyAPI = api_methods.Currency()
    # main_functions.save_to_file(currencyAPI, 'JSON_Files/Currencies.json')
    currencies_dict = api_methods.get_Currencies_in_JSON()

    print(currencies_dict['quotes']['USDJPY'])

    x = 46.55
    y = currencies_dict['quotes']['USDCAD']
    x = x / y

    print (x)

    x = 46.55
    y = currencies_dict['quotes']['USDEUR']
    x = x / y
    print (x)
