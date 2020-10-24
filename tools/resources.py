import re
import random


def fillspace(field_len, inpt):
    if len(inpt) < field_len:
        a = re.sub(r'[^a-zA-Z0-9 ]', '', inpt)
        b = field_len - len(a)
        c = ' ' * b
        return a + c
    else:
        a = re.sub(r'[^a-zA-Z0-9 ]', '', inpt)
        if len(a) < field_len:
            b = field_len - len(a)
            c = ' ' * b
            return a + c
        else:
            b = a[:field_len]
            return b


def name_truncate(name):
    cleanName = re.sub(r'[^a-zA-Z0-9 ]', '', name)
    cleanName = cleanName[:15]
    return cleanName + ' '


def date_convert(date):
    converter = re.compile(r'(\d\d|\d)/(\d\d|\d)/(\d\d\d\d|\d\d)')
    try:
        d = converter.match(date)
    except:
        raise ValueError('Date input was not correct')
    year = d.group(3)[:2]
    month = d.group(1)
    day = d.group(2)
    if len(day) < 2:
        day = '0'+ day
    if len(month) < 2:
        month = '0' + month

    return year + month + day


def generate_trace(ein):
    new_ein = ein[:5]
    trace = str(random.randrange(10000000000))
    if len(trace) < 10:
        a = 10 - len(trace)
        b = '0' * a
        trace = b + trace
    return new_ein + trace

def pad_zeros(field_len, inpt):
    b = field_len - len(inpt)
    c = '0' * b
    return c + inpt

def clean_amount(inpt, field_len):
    clean = re.sub(r'[^0-9.]', '', inpt)
    if '.' in clean:
        a = re.compile(r'(\d+)\.(\d\d|\d)')
        b = a.search(clean)
        dollars = b.group(1)
        cents = b.group(2)
        if len(cents) < 2:
            cents = cents + '0'
        amt = dollars + cents
        return pad_zeros(field_len, amt)

    else:
        a = re.compile(r'(\d+)')
        b = a.search(clean)
        val = b.group()
        amt = val + '00'
        return pad_zeros(field_len, amt)


def nameFill(field_len, inpt):
    if len(inpt) < field_len:
        a = re.sub(r'[^a-zA-Z0-9]', '', inpt)
        b = field_len - len(a)
        c = ' ' * b
        return a + c
    else:
        a = re.sub(r'[^a-zA-Z0-9]', '', inpt)
        if len(a) < field_len:
            b = field_len - len(a)
            c = ' ' * b
            return a + c
        else:
            b = a[:field_len]
            return b


def truncate_hash(hash_total):
    end = len(hash_total)
    if end > 10:
        start = end - 10
        hash = hash_total[start:end]
        return hash
    else:
        return pad_zeros(10, hash_total)



