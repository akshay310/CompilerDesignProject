import numpy as np 
import pandas as pd 
LEXER_TABLE=pd.DataFrame(columns=['TOKEN','IDENTITY'],index=range(1)) 
 
def lexer(): 
    with open('program.txt', 'r') as myfile: 
        string = myfile.read().replace('\n', ' ') 
 
    SYMBOLS = ['(', ')', ';', ',', ':', '\''] 
    SYMBOLS_1 = SYMBOLS + ['+', '='] 
    SYMBOLS_1_DEF = [['Open bracket', '('], ['Close bracket', ')'], ['Semi colon', ';'], ['Comma', ','], 
                     ['Colon', ':'], ['Single quote', '\''], ['plus', '+'], ['equal', '=']] 
 
    keywords = ['int', 'main', 'while', 'begin', 'end', 'expr', '', '\n'] 
    keywords_def = [['t', 'int'], ['m', 'main'], ['l', 'while'], ['b', 'begin'], ['d', 'end'], ['e', 'expr'], 
                    ['s', ' '], ['o', '+'], ['o', '='], ['n', '\n']] 
    KEYWORDS = SYMBOLS_1 + keywords 
 
    white_space = ' ' 
    lexeme = '' 
    list = [] 
    string = string.replace('\t', '') 
 
    for i, char in enumerate(string): 
        if char != white_space: 
            lexeme += char 
 
        if i + 1 < len(string): 
            if string[i + 1] == white_space or string[i + 1] in KEYWORDS or lexeme in KEYWORDS: 
                if lexeme != '': 
                    list.append(lexeme.replace('\n', '<newline>')) 
                    lexeme = '' 
                    list.append(lexeme.replace('\n', '<newline>')) 
 
    s = '' 
    j = 0 
    try: 
        while True: 
            list.remove('') 
    except ValueError: 
        pass 
 
    for item in list: 
        for i in keywords_def: 
 
            if i[1] == item: 
                s = s + i[0] 
        if item in SYMBOLS: 
            s = s + item 
        elif item.isdigit(): 
            s = s + 'a' 
        elif item not in KEYWORDS: 
            s = s + 'v' 
 
    for i in list: 
        for k in SYMBOLS_1_DEF: 
            if i == k[1]: 
                LEXER_TABLE.at[j, 'TOKEN'] = i 
                LEXER_TABLE.at[j, 'IDENTITY'] = k[0] 
                j = j + 1 
                break 
        if i in keywords: 
            LEXER_TABLE.at[j, 'TOKEN'] = i 
            LEXER_TABLE.at[j, 'IDENTITY'] = 'Keyword' 
            j = j + 1 
            continue 
        if i.isdigit(): 
            LEXER_TABLE.at[j, 'TOKEN'] = i 
            LEXER_TABLE.at[j, 'IDENTITY'] = 'Digit' 
            j = j + 1 
            continue 
        elif i not in KEYWORDS: 
            LEXER_TABLE.at[j, 'TOKEN'] = i 
            LEXER_TABLE.at[j, 'IDENTITY'] = 'Identifier' 
            j = j + 1 
    print(LEXER_TABLE) 
    return s 
