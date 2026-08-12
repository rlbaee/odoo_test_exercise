# Python 3.12
# Author: Gaabriel Ponomarjov

import ast #Builtin library, milles on meetod stringist Python listi tegemiseks
 
search_domain = ['&', '&', 
 ('type', '=', 'science'), 
 ('language_code', '!=', 'en_US'), 
 '|', '|', 
 ('country_code', '=', 'ee'), 
 ('country_code', '=', 'lv'), 
 ('country_code', '=', 'lt')]

domain_str = """['&', '&', 
 ('type', '=', 'science'), 
 ('language_code', '!=', 'en_US'), 
 '|', '|', 
 ('country_code', '=', 'ee'), 
 ('country_code', '=', 'lv'), 
 ('country_code', '=', 'lt')]"""

# Programm kasutab rekursiivset meetodit domaini parsimiseks. Kui programm näeb '&' või '|', siis ta kutsub ennast enda sees välja, et parsida järgmised kaks elementi. Kui programm näeb tuple'it, siis ta genereerib SQL-i. Sellise meetodiga ei pea isegi kasutama loopi.

def parse(search_domain, index, table):
    item = search_domain[index]

    if isinstance(item, tuple): # Programm kontrollib kas item on tuple. Kui on, siis ta genereerib SQL-i
        field, operator, value = item
        if isinstance(value, str):
            value = f"'{value}'"
        return f"{table}.{field} {operator} {value}", index + 1

    if isinstance(item, str): # Kui item ei ole tuple vaid on string, on ta operaator ja funktsioon käivitab ennast enda sees, ja kasutab järgmise elemendi indeksit.
        if item == '&':
            operation1, next_index = parse(search_domain, index + 1, table) # paneb ette ka table'i nime, et SQL-i genereerimisel oleks korrektne tabeli nimi
            operation2, next_index = parse(search_domain, next_index, table)
            return f"({operation1} AND {operation2})", next_index
        elif item == '|':
            operation1, next_index = parse(search_domain, index + 1, table)
            operation2, next_index = parse(search_domain, next_index, table)
            return f"({operation1} OR {operation2})", next_index


def domain_to_sql(search_domain, table): # Lisab SQLile SELECT * FROM clause(sõnad) ette
    where_clause, _ = parse(search_domain, 0, table)
    return f"SELECT * FROM {table} WHERE {where_clause};"


def domain_from_string_to_sql(domain_str, table): # Boonus: võtab domaini sisse stringina ja teeb sellest sama moodi SQL-i. ast.literal_eval teeb stringist Python listi
    search_domain = ast.literal_eval(domain_str)
    return domain_to_sql(search_domain, table)

print(domain_to_sql(search_domain, 'news_article'))

print(domain_from_string_to_sql(domain_str, 'news_article'))

# Programmi tegemisel kasutasin küll AI'd, kuid mitte koodi tuimalt kopeerimiseks