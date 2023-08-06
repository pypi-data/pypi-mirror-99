## stats
![code-size](https://img.shields.io/github/languages/code-size/NewLife1324/NewLifeUtils-Dev)
![issues](https://img.shields.io/github/issues/NewLife1324/NewLifeUtils-Dev)
![pr](https://img.shields.io/github/issues-pr-raw/NewLife1324/NewLifeUtils-Dev)
![release](https://img.shields.io/github/v/release/NewLife1324/NewLifeUtils-Dev)
![pypi-v](https://img.shields.io/pypi/v/NewLifeUtils)
![contributors](https://img.shields.io/github/contributors/NewLife1324/NewLifeUtils-Dev)
![pypi-format](https://img.shields.io/pypi/format/NewLifeUtils)
![license](https://img.shields.io/github/license/NewLife1324/NewLifeUtils-Dev)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/NewLifeUtils/NewLifeUtils-Dev/issues)
[![Inline docs](http://inch-ci.org/github/NewLifeUtils/NewLifeUtils-Dev.svg?branch=main)](http://inch-ci.org/github/NewLifeUtils/NewLifeUtils-Dev)

## Contact me
[PyPI Page](https://pypi.org/project/NewLifeUtils)

[My website](http://newlife-learn.h1n.ru)

[My VK](https://vk.com/newlife2019_szhs)

My Mail: semechkagent@gmail.com

## News
Recently, the code was rewritten, but without using notepad. I was able to understand and get used to PyCharm, which means that refactoring and quick code writing functions became available to me. This has greatly simplified the work and revealed a lot of bugs in my code, which means that my code is far from perfect and I have something to strive for. In any case, I have fixed quite important flaws in my code and partially rewritten my code once again. It's easier for me to start from scratch than to redo ¯\_(ツ)_/¯

## Modules
- ColorModule
- LoggerModule
- ExceptModule
- FileModule
- StringUtilModule
- TableBuildModule
- UtilsModule
- CustomShellModule
- DatabaseManageModule (working)
### ColorModule
![alt text](https://github.com/NewLife1324/NewLifeUtils-Dev/blob/main/images/ColorModule.jpg?raw=true)
```py
from NewLifeUtils.ColorModule import FGC, ACC

print(f'{FGC.RED}Red text')
print(f'{FGC.GREEN}Green text')
print(f'{ACC.UNDERLINE}UNDERLINE')
print(f'{ACC.RESET}No formating')
```

### LoggerModule
![alt text](https://github.com/NewLife1324/NewLifeUtils-Dev/blob/main/images/LoggerModule-1.jpg?raw=true)
![alt text](https://github.com/NewLife1324/NewLifeUtils-Dev/blob/main/images/LoggerModule-2.jpg?raw=true)
```py
from NewLifeUtils.LoggerModule import log, wrn, err, tip, rea

a = rea('input your data:')
log('My Event')
wrn('Something is wrong')
err('I broke something.')
tip('Tip #1, I recommend it to you...')
log('Event with tag', 'my tag')
```

### ExceptModule
![alt text](https://github.com/NewLife1324/NewLifeUtils-Dev/blob/main/images/ExceptModule.jpg?raw=true)
```py
from NewLifeUtils.ExceptModule import except_print

try:
    a = [1,2,3]
    a[3]
except Exception as e:
    except_print(e,"fatal", tb=True) #Not more working
```

### StringUtilModule
![alt text](https://github.com/NewLife1324/NewLifeUtils-Dev/blob/main/images/StringUtilModule.jpg?raw=true)
```py
from NewLifeUtils.StringUtilModule import screate,remove_csi
from NewLifeUtils.ColorModule import FGC, ACC

text = f'{FGC.RED}r{FGC.GREEN}g{FGC.BLUE}b{ACC.RESET}'
print(f'Original: {text}')
print('|'+screate(text, size=10, insert="r", filler_symbol=" ")+'| - right 10 (" ")')
print('|'+screate(text, size=10, insert="l", filler_symbol=" ")+'| - left 10 (" ")')
print('|'+screate(text, size=10, insert="l", filler_symbol="@")+'| - left 10 ("@")')
print(remove_csi(text))
```

### TableBuildModule
![alt text](https://github.com/NewLife1324/NewLifeUtils-Dev/blob/main/images/TableBuildModule.jpg?raw=true)
```py
from NewLifeUtils.TableBuildModule import *
data = [
    "header", "header number 2", "num",
    "data","tooooooooooooooooo long string", "123",
    "data2", "small","15436"
    ]
table = create_table(3,[],data)
print(table)
```


***Translator used**
