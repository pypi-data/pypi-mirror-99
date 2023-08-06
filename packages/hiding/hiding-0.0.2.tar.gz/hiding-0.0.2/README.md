# Hiding
### Just a random python lib that extremely inefficiently hides text in other text. 

---

## Introduction

Hiding is a very simple 25 LOC lib that allows hiding text inside text. 
It could be seen as a rudimentary text based steganography. In fact, during drafting stages, this project was known as "testegano" - a portmanteau of "text" and "stegano". 

## Uses 
Please don't use this in production. This is more a proof of concept than a useful​‌​‌‌​​‌​‌‌​​‌​‌​‌‌‌​​‌‌​​‌​‌‌​​​​‌​​​​​​‌‌​‌‌‌‌​‌‌​​‌‌​​​‌​​​​​​‌‌​​​‌‌​‌‌​‌‌‌‌​‌‌‌​‌​‌​‌‌‌​​‌​​‌‌‌​​‌‌​‌‌​​‌​‌​​‌​​​​​​‌​​‌​​‌​​‌​​‌‌‌​‌‌​‌‌​‌​​‌​​​​​​‌‌​​‌‌‌​‌‌​‌‌‌‌​‌‌​‌​​‌​‌‌​‌‌‌​​‌‌​​‌‌‌​​‌​​​​​​‌‌‌​‌​​​‌‌​‌‌‌‌​​‌​​​​​​‌‌​‌​​​​‌‌​‌​​‌​‌‌​​‌​​​‌‌​​‌​‌​​‌​​​​​​‌‌​‌‌​‌​‌‌​​‌​‌​‌‌‌​​‌‌​‌‌‌​​‌‌​‌‌​​​​‌​‌‌​​‌‌‌​‌‌​​‌​‌​‌‌‌​​‌‌​​‌​​​​​​‌‌​‌​​‌​‌‌​‌‌‌​​​‌​​​​​​‌‌​‌​​​​‌‌​​‌​‌​‌‌‌​​‌​​‌‌​​‌​‌​​‌​‌‌‌​ lib. While it can be useful to hide some text, it's unfeasible to use this for any text bigger than 5 characters. 
It is less secure than conventional image based stegano, as some editors either show the unicode or show them as spaces. 

## Theory
The unicode consortium was founded to make a universial code (as the name suggests). This means they have to factor in edge cases like CJK characters who doesn't have conventional spaces. That's why they've made 2 types of "invisible" space characters.  \u200b and \u200c. Hiding exploits that by converting the message from ascii into binary, then writing the message in the middle of the string, \u200b for 0, \u200c for 1. Because they do not break the text, it would be hard for a naked eye to see them (unless of course, someone puts it in a character count or tries to delete the text by backspace). 

## Limitations
- Because everything is stored in binary, the hidden length will be eight times longer than the normal length. This means you can't hide essaies in text :(.

- It uses ascii, which means diacritics and non-latin letters won't be supported. 

- It's a literal PITA to deal with the text. You'll have to be careful wit​‌​‌​‌‌‌​‌‌​​‌​‌​‌‌​‌‌​​​‌‌​‌‌​​​​‌​​​​​​‌‌​​‌​​​‌‌​‌‌‌‌​‌‌​‌‌‌​​‌‌​​‌​‌​​‌​​​​​​‌‌​​‌‌​​‌‌​‌​​‌​‌‌​‌‌‌​​‌‌​​‌​​​‌‌​‌​​‌​‌‌​‌‌‌​​‌‌​​‌‌‌​​‌​​​​​​‌‌​‌‌​‌​‌‌​​‌​‌​​‌​​​​​​‌‌‌​‌​​​‌‌​‌​​​​‌‌​‌‌‌‌h it because it's invisible. 

## Installation
Install it like any other pypi module.
`python -m pip install hiding`

#### Manual Install
If you are the type of person to install manu​‌​​‌‌​​​‌‌‌​‌​‌​‌‌​‌​‌‌​‌‌​​‌​‌​​‌​​​​​​‌​​‌​​‌​​‌​​​​​​‌‌​‌​​​​‌‌​​​​‌​‌‌‌​‌‌​​‌‌​​‌​‌​​‌​​​​​​‌‌​​​​‌​​‌​​​​​​‌‌​​​‌‌​‌‌‌​​‌​​‌‌‌​‌​‌​‌‌‌​​‌‌​‌‌​‌​​​​​‌​​​​​​‌‌​‌‌‌‌​‌‌​‌‌‌​​​‌​​​​​​‌‌‌‌​​‌​‌‌​‌‌‌‌​‌‌‌​‌​‌​​‌​​​​​​​‌‌‌​‌‌​​‌​‌​​‌ally then you don't need to read this guide.

## Usage 

Since there are only 2 functions, it's better to import them directly. Unless they clash with other functions, in which case you may want to use aliases or just import the whole module. 

```py
from hiding import hide, show
```

Now, you've got the two functions. Simply call them whenever you want to hide or show text. Remember you can only hide very short messages. 

```py
from hiding import hide, show

print(hide("This is a long string of text.","secretmsg"))
```
The above should return "This is a long ​‌‌‌​​‌‌​‌‌​​‌​‌​‌‌​​​‌‌​‌‌‌​​‌​​‌‌​​‌​‌​‌‌‌​‌​​​‌‌​‌‌​‌​‌‌‌​​‌‌​‌‌​​‌‌‌string of text.". 
The usage of `hide()` is `hide("Public-facing text","Message to hide")`. Upon success, it returns a string - the first argument with the message hidden in it.

To get the secret message back from a hidden text, you may use the `show()` function. 

```py
from hiding import hide, show
print(show("This is a long ​‌‌‌​​‌‌​‌‌​​‌​‌​‌‌​​​‌‌​‌‌‌​​‌​​‌‌​​‌​‌​‌‌‌​‌​​​‌‌​‌‌​‌​‌‌‌​​‌‌​‌‌​​‌‌‌string of text."))
```
Show only takes 1 argument, the hidden text. It either returns a string or a None. The None will be returned when the message could not be found. This way, you could check if something contains a message simply by `if show("Message Here"):`. As it would return false if there isn't a message. 

## Support
You are discouraged to use this lib for anything important, but I am happy to give support. Email me at <contact@johnngnky.xyz> and I'd love to help. 

## License 
Do whatever the fuck you want. 
[![](http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-1.png)](http://www.wtfpl.net).
```
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

```


