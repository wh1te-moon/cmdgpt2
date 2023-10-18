import re

from dicts import argDict, conDict,defaultFunc


def argsAnalyze(message: str):
    def replace_param(match):
        key, value1, value2 = match.groups()
        try:
            if key in argDict:
                if value1:
                    if (value1 in conDict):
                        argDict[key](conDict[value1],value2) if value2 else argDict[key](conDict[value1])
                    else:
                        argDict[key](value1)
                else:
                    argDict[key]()
        except Exception as e:
            print(f"{key} {value1} {value2} analyze failed")
        return ''
    for i in defaultFunc:
        message=i(message=message)
    param_pattern = '-(\w+)\s*([\w.]*)\s*([\w.]*)'
    message = re.sub(param_pattern, replace_param, message)
    return message


# if __name__ == "__main__":
#     print(argsAnalyze("hello -t odjad cohia -i acio -a"))
