def get_productions(X): 
    productions = [] 
    for prod in grammar: 
        lhs, rhs = prod.split('->') 
        if lhs == X: 
            rhs = '.' + rhs 
            productions.append('->'.join([lhs, rhs])) 
    return productions 
 
 
def closure(I): 
    for production, a in I: 
        if production.endswith("."): 
            continue 
        lhs, rhs = production.split('->') 
        alpha, B_beta = rhs.split('.') 
        B = B_beta[0] 
        beta = B_beta[1:] 
        beta_a = beta + a 
        first_beta_a = first(beta_a) 
        for b in first_beta_a: 
            B_productions = get_productions(B) 
            for gamma in B_productions: 
                new_item = (gamma, b) 
                if new_item not in I: 
                    I.append(new_item) 
    return I 
 
def get_symbols(grammar): 
    terminals = set() 
    non_terminals = set() 
     
    for production in grammar: 
        lhs, rhs = production.split('->') 
        non_terminals.add(lhs) 
         
        for x in rhs: 
            if not x.isupper() and x!='|': 
                terminals.add(x)  
             
    terminals.add('$') 
    return terminals, non_terminals 
 
def first(symbols): 
    final_set = [] 
 
     
    for X in symbols: 
        first_set = []  
         
        if is_terminal(X): 
            final_set.extend(X) 
            return final_set 
        else: 
            for production in grammar: 
                lhs, rhs = production.split('->') 
                 
                if lhs == X: 
                    for i in range(len(rhs)): 
                        y = rhs[i] 
                        if y == X: 
                            continue 
                             
                        first_y = first(y) 
                        first_set.extend(first_y) 
                        break 
            final_set.extend(first_set)            
    return final_set 
 
def is_terminal(symbol): 
    return symbol in terminals 
 
def shift_dot(production): 
    lhs, rhs = production.split('->') 
    x, y = rhs.split(".") 
     
    if len(y) == 0: 
        print("Dot at the end!") 
        return 
    elif len(y) == 1: 
        y = y[0] + "." 
    else: 
        y = y[0] + "." + y[1:] 
         
    rhs = "".join([x, y]) 
    return "->".join([lhs, rhs]) 
 
def goto(I, X): 
    J = [] 
     
    for production, look_ahead in I: 
        lhs, rhs = production.split('->') 
         
        if "." + X in rhs and not rhs[-1] == '.': 
 
            new_prod = shift_dot(production) 
            J.append((new_prod, look_ahead))         
    return closure(J) 
 
def set_of_items(display=False): 
    num_states = 1 
    states = ['I0'] 
    items = {'I0': closure([('A->.S', '$')])} 
     
    for I in states: 
        for X in pending_shifts(items[I]): 
            goto_I_X = goto(items[I], X) 
             
            if len(goto_I_X) > 0 and goto_I_X not in items.values(): 
                new_state = "I" + str(num_states) 
                states.append(new_state) 
                items[new_state] = goto_I_X 
                num_states += 1 
                 
    if display: 
        for i in items: 
            print("State", i, ":") 
            for x in items[i]: 
                print(x) 
            print() 
             
    return items 
 
def pending_shifts(I): 
    symbols = []  
     
    for production, _ in I: 
        lhs, rhs = production.split('->') 
        if rhs.endswith('.'): 
            continue 
             
        beta = rhs.split('.')[1][0] 
        if beta not in symbols: 
            symbols.append(beta) 
             
    return symbols 
 
def done_shifts(I): 
    done = [] 
    for production, look_ahead in I: 
        if production.endswith('.') and production != 'A->S.': 
            done.append((production[:-1], look_ahead))         
    return done 
 
 
def get_state(C, I): 
    key_list = list(C.keys()) 
    val_list = list(C.values()) 
    i = val_list.index(I)     
    return key_list[i] 
 
def CLR_construction(num_states): 
    C = set_of_items() 
    ACTION = pd.DataFrame(columns=list(terminals), index=range(num_states)) 
    GOTO = pd.DataFrame(columns=list(non_terminals), index=range(num_states)) 
     
    for Ii in C.values(): 
        i = int(get_state(C, Ii)[1:]) 
        pending = pending_shifts(Ii) 
         
        for a in pending: 
            Ij = goto(Ii, a) 
            j = int(get_state(C, Ij)[1:]) 
             
            if is_terminal(a): 
                ACTION.at[i, a] = "Shift " + str(j) 
            else: 
                GOTO.at[i, a] = j 
                 
        for production, look_ahead in done_shifts(Ii): 
            ACTION.at[i, look_ahead] = "Reduce " + str(grammar.index(production) + 1) 
             
        if ('A->S.', '$') in Ii: 
            ACTION.at[i, '$'] = "Accept" 
             
    ACTION.replace(np.nan, '', regex=True, inplace=True) 
    GOTO.replace(np.nan, '', regex=True, inplace=True) 
    return ACTION, GOTO 
 
 
def parse_string(string, ACTION, GOTO): 
    row = 0 
    cols = ['Stack', 'Input', 'Output'] 
    if not string.endswith('$'): 
        string = string+'$' 
    ip = 0  
    PARSE = pd.DataFrame(columns=cols) 
    input = list(string) 
    stack = ['$', '0'] 
    while True: 
        S = int(stack[-1]) 
        a = input[ip] 
 
        action = ACTION.at[S, a] 
        new_row = ["".join(stack), "".join(input[ip:]), action] 
        if 'S' in action: 
            S1 = action.split()[1] 
            stack.append(a) 
            stack.append(S1) 
            ip += 1 
        elif "R" in action: 
            i = int(action.split()[1])-1 
            A, beta = grammar[i].split('->') 
            for _ in range(2*len(beta)): 
                stack.pop() 
 
            S1 = int(stack[-1]) 
            stack.append(A) 
            stack.append(str(GOTO.at[S1, A])) 
            new_row[-1] = "Reduce "+grammar[i] 
 
        elif action == "Accept": 
            PARSE.loc[row] = new_row 
            print(PARSE,"\n") 
            print("\nThe Source code entered is according to the grammar\n") 
            return PARSE 
        else: 
            print(PARSE,"\n") 
            print("\nThe Source code entered is incorrect\n") 
            break 
        PARSE.loc[row] = new_row 
        row += 1 
 
 
def get_grammar(filename): 
    grammar = [] 
    F = open(filename, "r") 
    for production in F: 
        grammar.append(production[:-1]) 
    return grammar 
 
 
if __name__ == "__main__": 
    grammar = get_grammar("grammar.txt") 
    terminals, non_terminals = get_symbols(grammar) 
    symbols = terminals.union(non_terminals) 
 
     
     
    print("\n\n------TOKENS-----\n") 
    string = "".join(lexer()) 
print("\n\n------STATES-----\n") 
start = [('A->.S', '$')] 
C = set_of_items(display=True) 
ACTION, GOTO = CLR_construction(num_states=len(C)) 
print("\n\n------PARSE TABLE-----\n") 
print("\n\n------ACTION-----\n") 
print(ACTION) 
print("\n\n------GOTO-----\n") 
print(GOTO) 
print("\n\n------PARSING-----\n") 
PARSE_TABLE = parse_string(string, ACTION, GOTO)
