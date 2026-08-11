# Python 3.12
# Author: Gaabriel Ponomarjov

search_domain = ['&', ('type', '=', 'science'), ('language_code', '!=', 'en_US')]

def main(search_domain):
    item1, item2 = '', ''

    for index, item in enumerate(search_domain):
        ...

        if isinstance(item, tuple):

            ...
        else:
            if item == '&':
                field1, operator1, value1 = search_domain[index + 1]
                field2, operator2, value2 = search_domain[index + 2]
                print(f'{field1} {operator1} \'{value1}\' AND {field2} {operator2} \'{value2}\'')
                ...
                

if __name__ == "__main__":
    main(search_domain)