import sys 
try:
    from solution.exceptions import InvalidTokenException, NotClosedParenthesesException
except ImportError:
    from exceptions import InvalidTokenException, NotClosedParenthesesException

tokens = ['(', ')']

def find_matching_pair(text, idx):
    """For a given text of parentheses and idx, find the index of matching parentheses in the text. 

    Args:
        str text 
        int idx 
    Returns:
        int
    Raises:
        InvalidTokenException: When the input contains invalid character.
        NotClosedParenthesesException: When it is impossible to find the matching parentheses. 
        ValueError: When the input idx is larger or equal to len(text) or is smaller than 0. 
    
    Examples:
        find_matching_pair('()', 0)
        >> 1 
        find_matching_pair('(())', 1)
        >> 2
        find_matching_pair(')', 0)
        >> NotClosedParenthesesException 
    """

    return -1 

def determine_if_rule0(text):
    return text == '' 

def determine_if_rule1(text):
    return False 

def determine_if_rule2(text):
    return False 

def parse_empty_string():
    return {'node': '', 'rule': 0}

def default_node_information(text, offset):
    res = {}
    res['node'] = text 
    res['start'] = offset 
    res['end'] = len(text) - 1 + offset 
    return res

def update_rule1_data(text, res):
    assert determine_if_rule1(text)
    
    res['rule'] = 1
    res['left'] =  {'node': '(', 'start': 0, 'end': 0, }
    res['right'] = {'node': ')', 'start': len(text) - 1, 'end': len(text) - 1, }

    return res 

def update_rule1_mid(text, res):
    assert determine_if_rule1(text)
    
    res['mid'] = parse_parentheses_with_offset(text[1:-1])

    return res 

def update_rule2_data(text, res):
    assert determine_if_rule2(text)
    
    res['rule'] = 2

    return res 

def update_rule2_nodes(text, res):
    assert determine_if_rule2(text)

    text_segments = []
    idx = 0

    while idx < len(text) - 1:
        jdx = find_matching_pair(text, idx) 
        text_segments.append((text[idx:jdx+1], idx))
        idx = jdx + 1 
    
    res_nodes = []
    for t, i in text_segments:
        res_nodes.append(parse_parentheses_with_offset(t, i))
    res['nodes'] = res_nodes 
    
    res['nodes'] = [
        parse_parentheses_with_offset(t, i) 
            for t, i in text_segments
        ]
    return res 

def parse_parentheses(text):
    """For the given string, parse it in the form of dict. 

    For detailed explanation about the parsing process and the result format, consult parentheses/documents/assignment.txt file. 

    Args:
        str text
    Returns:
        dict 
    Raises:
        InvalidTokenException: When the input contains invalid character.
        NotClosedParenthesesException: When the input have a syntax error.
    Examples:

    parse_parentheses('')
    >> {
            'node': '',
            'rule': 0,  
    }
    parse_parentheses('()')
    >> {
            'node': '()', 
            'start': 0, 
            'end': 1,
            'rule': 1, 
            'left': {
                'node': '(', 
                'start': 0, 
                'end': 0, 
            },
            'mid': {
                'node': '', 
                'rule': 0, 
            }, 
            'right': {
                'node': ')',
                'start': 1, 
                'end': 1,   
            },
    }
    parse_parentheses('(())')
    >> {
            'node': '(())', 
            'start': 0, 
            'end': 3, 
            'rule': 1, 
            'left': {
                'node': '(', 
                'start': 0, 
                'end': 0, 
            }, 
            'mid': {}, // Same as parse_parentheses('()'), except for start/end attributes. 
            'right': {
                'node': ')', 
                'start': 3, 
                'end': 3, 
            }
    }
    parse_parentheses('()()')
    >> {
            'node': '()()', 
            'start': 0, 
            'end': 3, 
            'rule': 2, 
            'nodes': [
                {...},  // Same as parse_parentheses('()').
                {...},  // Same as parse_parentheses('()'), except for start/end attributes. 
            ]
    }
    parse_parentheses('(()())')
    >> {
            'node': '(()())', 
            'start': 0, 
            'end': 5, 
            'rule': 1, 
            'left': {...}, // Same as parse_parentheses('()')['left'] 
            'mid': {...}, // Same as parse_parentheses('()()'), except for start/end attributes. 
            'right': {...}, // Same as parse_parentheses('()')['left'], except for start/end attributes. 
    }
    """ 

    return parse_parentheses_with_offset(text)

def parse_parentheses_with_offset(text, offset = 0):
    rule0 = determine_if_rule0(text)
    rule1 = determine_if_rule1(text) 
    rule2 = determine_if_rule2(text) 

    if rule0: # rule 0 : para -> '' 
        return parse_empty_string()
    
    res = default_node_information(text, offset)

    if rule1: # rule 1 : para -> ( para ) 
        res = update_rule1_data(text, res)
        res = update_rule1_mid(text, res)
        res = update_rule1_mid(text, res)
    elif rule2: # rule 2 para -> para1 para2 ... 
        res = update_rule2_data(text, res) 
        res = update_rule2_nodes(text, res)     
    else:
        assert False, 'Something goes wrong' 
    
    return res 

def main():
    args = sys.argv
    with open(f'{sys.argv[1]}', 'r') as f:
        text = f.read().strip()
        print(parse_parentheses(text))

if __name__ == '__main__':
    print(determine_if_rule0(''))
    print(determine_if_rule0('()'))
    print(find_matching_pair('()', 0))