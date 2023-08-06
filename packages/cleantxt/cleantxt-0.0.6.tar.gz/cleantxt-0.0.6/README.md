# cleantxt

cleaning text from noise for nlp tasks

## installation 
with pip

`pip install cleantxt`

install from source

`git clone https://github.com/jemiaymen/cleantxt.git`

go to the cleantxt directory

`cd cleantxt`

install with pip

`pip install .`

## cli usage

`cleantxt --doc=[path_to_doc] 
                  --out=[path_out_file]
                  --f=[0] 
                  --t=[100] 
                  --do_lower=True
                  --white_space=True 
                  --punctuation=True 
                  --duplicated_chars=True
                  --alpha_num=True 
                  --accent=True 
                  --escape key,value ə,a œ,oe`

check example 

![](example.gif)

## api usage

import text module

`from cleantxt import text`

clean text

`txt = text.clean_text('mella 7ayawaaanéé hadddddda mta3@@@@@ @tfih')`

print the result

`mella 7ayawane hada mta3 tfih`

## params

text : -> (str) raw text

whitespace : -> (boolean) escape spaces [default True ]

punctuation : -> (boolean) escape punctuation [default True ]

duplicated : -> (boolean) escape duplicated chars [default True ]

alphanum : -> (boolean) escape non alpha numeric chars [default True ]

accent : -> (boolean) escape accent [default True ]

do_lower : -> (boolean) lower case text [default True ]

others : -> ( list( tuple() ) ) escape rules [ default [('ə', 'a')] ]

## new function

### word count
wc => (word count) params (path :str, unique=False, both=False)

`from cleartxt import text`
`print( text.wc('file.txt',both=True) ) `

(51515,5547)

output tuple (all words , unique words)

### word frequency
word_frequency => params (path : str, top=100)

`from cleartxt import text`
`print( text.word_frequency('file.txt') ) `

[('\n', 54898), ('', 48757), ('w', 27717), ('el', 16679), ('fi', 9399), ('ya', 8611)]

output list of tuples (word , frequency)