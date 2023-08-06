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
import sys

def nested(the_list,indent=False, level=0, fh=sys.stdout):
    for each in the_list:
        if isinstance(each,list):
            nested(each,indent,level+1,fh)
        else:
            if indent:
                print("\t"*level,end='',file=fh)
            print(each,file=fh)
