def concat_arg(currency_in_list): 
    currency_name = ''
    for i in range (len(currency_in_list)):
        currency_name += str(currency_in_list[i]) + " "
    return currency_name[:-1]     

def extract_arg(arg):
    return arg.split()[1:]