String Booster Pack

-A small collection of semi-useful functions for strings


-Content List:

    cctrans(txt)
        -Credit Card Transformer
        -Replaces all but the last 4 characters of a string with '*'
        -Warns if not 16 characters
        
    sstrans(txt)
        -Social Security Transformer
        -Replaces all but the last 4 characters of a string with '*'
        -Warns if not 9 characters
        
    passgen(length=8)
        -Password Generator
        -Generates a random password of a specified length (default 8 characters)
    
    btitle(txt, lowers=['and', 'the', 'of', 'if', 'in', 'on', 'with'])
        -Better Title
        -Like title(), but better!
        -Capitalizes all words in a string excluding some words commonly kept lowercase
        
    emailfinder(txt)
        -Email Finder
        -Finds email addresses in a string and returns a list of them
        
    censor(txt, words=[], sub='*')
        -Censor
        -Replaces designated words in a string with '*'
        
    redactor(txt, words=[], replacement='[redacted]')
        -Redactor
        -Replaces designated words in a string with '[redacted]'
        
    asciifinder(txt)
        -ASCii Finder
        -Creates a dictionary of each unique character in a string and its ASCii value
         
    asciicipher(txt, seed=None)
        -ASCii Cipher
        -A simple substitution cipher that encrypts a string
        -Changes each character into a new one by adding a random number (1-10) to its ASCii value
        
    asciidecrypter(txt, key=None)
        -ASCii Decrypter
        -Returns the transformed string from ASCii Cipher to its original form
        
        
Please visit my page (https://github.com/coy0tecode/String-Booster-Pack)
for more information on this package/questions/concerns/to have a look around.