# -*- coding: utf-8 -*-


# Additional string methods to do some things
# Version 1.0.0
# import using: import string_booster


import re
import warnings
import random as r


# Credit Card transformer
# Changes all but last 4 characters to '*'
def cctrans(txt):
    '''
    -Removes any extra whitespace, removes dashes, spaces, and underscores
    -Returns a string of all '*' except the last 4 characters, warns the user
     if the length of the card is not equal to the standard 16 digits

    Parameters
    ----------
    txt : String/Integers

    Returns
    -------
    String
    
    Outputs
    -------
    None

    '''
    
    txt = str(txt)
    txt = txt.strip()
    txt = txt.replace('-', '').replace(' ', '').replace('_', '')
    if len(txt) != 16:
        warnings.warn("Card Number length not equal to standard 16 digits.")
    return len(txt[:-4]) * '*' + txt[-4:]


# Social Security transformer
# Changes all but last 4 characters to '*'
def sstrans(txt):
    '''
    -Removes any extra whitespace, removes dashes, spaces, and underscores
    -Returns a string of all '*' except the last 4 characters, warns the user
     if the length of the socia security number is not equal to the standard
     9 digits

    Parameters
    ----------
    txt : String/Integers

    Returns
    -------
    String
    
    Outputs
    -------
    None

    '''
    
    txt = str(txt)
    txt = txt.strip()
    txt = txt.replace('-', '').replace(' ', '').replace('_', '')
    if len(txt) != 9:
        warnings.warn("Social Security length not equal to 9.")
    return len(txt[:-4]) * '*' + txt[-4:]


# Password generator
# Creates a randomly generated password of user designated length
def passgen(length=8):
    '''
    -Uses chr() function on a random number between 33 and 127 a number of times
     equal to the length parameter (32/whitespace is excluded)
    -Joins these characters together and returns them as a string
    
    Parameters
    ----------
    length : Integer

    Returns
    -------
    String
    
    Outputs
    -------
    None

    '''
    
    return ''.join([chr(r.randrange(33, 127)) for i in range(length)])


# Better Title
# title() with additional flexibility
# Use default 'lowers' or pass your own list of words to keep lowercase
def btitle(txt, lowers=['and', 'the', 'of', 'if', 'in', 'on', 'with']):
    '''
    -Returns a string where each word is capitalized, excluding words in the
     'lowers' list
    -Treats hyphenated words as individual words
    
    Parameters
    ----------
    txt : String
    lowers : List

    Returns
    -------
    String
    
    Outputs
    -------
    None

    '''
    
    return ''.join([i if i in lowers else i.capitalize() for i in re.split('([ -])',txt.lower())])


# Email Finder
# Returns a list of emails from a string
# Credit to Mohd Sanad Zaki Rizvi's article on analyticsvidhya
# ^ https://www.analyticsvidhya.com/blog/2015/06/regular-expression-python/
def emailfinder(txt):
    '''
    -Uses regular expression findall to locate sequences of characters following
     the format: characters@characters.characters etc etc.
    
    Parameters
    ----------
    txt : String

    Returns
    -------
    List
    
    Outputs
    -------
    None

    '''
    
    return re.findall(r'[\w.-]+@[\w.-]+', txt)
    
    
# Censor
# Replace specified 'words' in 'txt' with 'sub'
# txt is a string, words is a list, sub is ideally a single character
def censor(txt, words=[], sub='*'):
    '''
    -Substitutes each character from any word found in 'txt' that is also in
     the 'words' list with the 'sub' character
    -Ignores case when substituting characters
    
    Parameters
    ----------
    txt : String
    words : List
    sub : Character/String

    Returns
    -------
    String
    
    Outputs
    -------
    None

    '''
    
    for word in words:
        txt = re.sub(r'\b{word}\b'.format(word=word), 
                     lambda i: str(sub) * len(i.group(0)), txt, flags=re.IGNORECASE)
    return txt


# Redactor
# Replace specified 'words' in 'txt' with 'replacement'
# txt is a string, words is a list, replacement is a string or character
def redactor(txt, words=[], replacement='[redacted]'):
    '''
    -Replaces any words in 'txt' found in the 'words' list with 'replacement'
    -Ignores case when substituting words
    
    Parameters
    ----------
    txt : String
    words : List
    replacement : String/Character
    
    Returns
    -------
    String
    
    Outputs
    -------
    None

    '''
    
    for word in words:
        txt = re.sub(r'\b{word}\b'.format(word=word),
                     str(replacement), txt, flags=re.IGNORECASE)
    return txt


# ASCii finder
# Returns a dictionary of the characters and ASCii values from 'txt'
# txt is a string/character
def asciifinder(txt):
    '''
    -Creates a list of a set of characters in 'txt'
    -Gets the ord values for all characters in txt_list
    -Returns a dictionary, mapping the chracter from txt_list as the key and
     the corresponding acii number as the value
    
    Parameters
    ----------
    txt : String/Character

    Returns
    -------
    Dictionary
    
    Outputs
    -------
    None

    '''
    
    txt_list = list(set([w for w in txt]))
    ascii_list = [ord(w) for w in txt_list]
    return {txt_list[i]: ascii_list[i] for i in range(len(txt_list))}


# ASCii cipher
# Returns an encrypted string, writes key to .text file at cwd
# txt is a string/character
def asciicipher(txt, seed=None):
    '''
    -Creates a list of characters in txt
    -Loops through the list offsetting each ord value of each character in
     the list by increasing it by a random number 1-10
    -If the new ord number is greater than 127, it will be subtracted from
     127 and this value added to 31 to get the ord number to be used
    -The text file it outputs is overwritten if a text file of the same name
     already exists in the directory

    Parameters
    ----------
    txt : String/Character

    Returns
    -------
    String
    
    Outputs
    -------
    .txt file to cwd

    '''
    import os
    
    txt_list = [w for w in txt]
    offsets = []
    encrypted = []
    r.seed(seed)
    for w in txt_list:
        offset = r.randint(1, 10)
        offsets.append(offset)
        new_w = ord(w) + offset
        if new_w > 127:
            new_w = 31 + (new_w - 127)
        encrypted.append(chr(new_w))
    f = open(os.getcwd() + '/cipher_key.txt', 'w')
    f.write(''.join(str(offsets)))
    f.close()
    return ''.join(encrypted)


# ASCii decrypter
# Decrypt the returned object from asciicipher
# txt is the string to be decrypted, key is list of offsets
def asciidecrypter(txt, key=None):
    '''
    -Uses the cipher_key file output from asciicipher function if key is not
     specified
    -Reads file, removes all trailing characters, removes all non-numeric
     characters (brackets,commas and spaces from list format)
    -Can also use a list passed directly as 'key'
    -Iterates through each character in txt_list and integer in key_list,
     subtracting the key_list value from the txt_list ord value to arrive at
     the original character before being encrypted by the cipher
    -If this new value is less than 32, it is subtracted from 32 and the
     remaining difference is subtracted from 128 to get the correct character
     ord value

    Parameters
    ----------
    txt : String/Character
    key : list/None

    Returns
    -------
    String
    
    Outputs
    -------
    None

    '''
    
    if key==None:
        import os
        f = open(os.getcwd() + '/cipher_key.txt', 'r')
        keys = f.read()
        keys = keys.rstrip('\n')
        keys = keys.translate({ord(' '): None})
        keys = keys.translate({ord(w): None for w in '[],'})
        f.close()
    else: 
        keys=list(key)
    txt_list = [w for w in txt]
    key_list = [int(w) for w in keys]
    decrypted = []
    for i in range(len(txt_list)):
        new_w = ord(txt_list[i]) - key_list[i]
        if new_w < 32:
            decrypted.append(chr(128 - (32 - new_w)))
        else:
            decrypted.append(chr(new_w))
    return ''.join(decrypted)
    
    


    
    
    




