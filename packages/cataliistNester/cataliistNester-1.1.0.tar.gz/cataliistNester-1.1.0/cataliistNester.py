"""
This is cataliistNester.py
The script prints lists that may or may not be included nested lists

Usages:
nested(list,indent)
list - This argument could be list or list with nested list
indent - tab stop for each list/nested list

Output:
Prints each item recursively on each line with defined indent
"""

def nested(the_list,indent=0):
    for each in the_list:
        if isinstance(each,list):
            nested(each,indent+1)
        else:
            for tab in range(indent):
                print("\t",end='')
            print(each)
