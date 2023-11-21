- [best command line chatgpt or chatgpt kernel](#best-command-line-chatgpt-or-chatgpt-kernel)
  - [for common user](#for-common-user)
    - [what you can do](#what-you-can-do)
    - [what you need](#what-you-need)
  - [want to diy more?](#want-to-diy-more)
    - [for developer](#for-developer)
## best command line chatgpt or chatgpt kernel

Diy your own gpt by making your own functions or your own shortcut key

### for common user

#### what you can do

Modify your own configs in `classes.py`,it will take effect when you start a new chat. Modify your own shortcut key in `dicts.py`,as mentioned below `-n`,`-t` and so on.

Not satisfied with gpt's answer? By using `[your input] -n 2 -t 0` to set amount of answer and its temperature.

Too much trouble when switching models?By using `[your input] -4` to use gpt4 in this conversition.Of course,"-3" is to use gpt3.5.

Save your template by "-savet",load it by "-load"

#### what you need
Set OPENAI_API_KEY as environment variable.
Python environment,with 
```pip
pip install requests
```
That's just all.

And then,you can run ```python gpt.py``` to chat with your own gpt.
### want to diy more? 

#### for developer

You can make your own functions in `utils.py`,
and modify its shortcut key in `dicts.py`,`argDict` will run when your input involve your short cut key with '-' before it.
All functions in defaultDict will run in every input.And Be sure to pass message as an argument and return message.

Its paramters is like "-func para1 para2",para1 and para2 is optional.you can analyze para1 from string into a variable in `constants.py` by modifing `conDict` in dicts.py.

That's all for something.