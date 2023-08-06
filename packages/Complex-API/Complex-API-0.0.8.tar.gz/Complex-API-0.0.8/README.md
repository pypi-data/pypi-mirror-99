# Complex API.py
This the source code for the python module I have built/working on.

This module makes it easy to use my <a href="https://github.com/JagTheFriend/APICode"> API </a>

Currently, the API supports:
  + compiling the code(of different languages) and getting the output
  + getting a random post from a _subreddit_
  + getting the lyrics of a song

  + generating pixel art
  + getting the weather of a place
  + finding the length of a youtube playlist

  + getting a random inspirational text
  + getting a result of a calculation
  + converting hexadecimal to decimal(or denary)
  + converting decimal(or denary) to binary


# Code snippets
In order to use the API,
you need to first download <a href="https://pypi.org/project/Complex-API/">this module (`pip install Complex-API`)</a>

## Compile API:
<a href="https://API.jagthefriend.repl.co/compile=python_print('This works')">
  Example:
</a>

```py
from Complex_API import complex_api
# run python
lang = "python"
code = '''
print('hello')
'''
print(complex_api.compile(lang=lang, code=code))
# run java
lang = "java"
code = '''
class Compiler{
    public static void main(String[] args){
        System.out.println("This works");
    }
}
'''
print(complex_api.compile(lang=lang, code=code))
```

<a href="https://API.jagthefriend.repl.co/compile=support_support">
  Get all the supported languages here
</a>

## Reddit API:
<a href="https://API.jagthefriend.repl.co/reddit=meme+10">
  Example:
</a>

```py
from Complex_API import complex_api
# example: name_of_subreddit = "meme"
name_of_subreddit = "name_of_a_valid_subreddit"
number_of_posts = 10 # number of posts to be returned
print(complex_api.reddit(limit=number_of_posts, subreddit=name_of_subreddit))
```

## Lyrics API:
<a href="https://API.jagthefriend.repl.co/lyrics+falling">
  Example:
</a>

```py
from Complex_API import complex_api
SongName = "name of song"
print(complex_api.lyrics(song=SongName))
```

## Pixel Art:
<a href="https://API.jagthefriend.repl.co/ascii_hello">
  Example:
</a>

```py
from Complex_API import complex_api
text = "Hello gammer"
print(complex_api.ascii(text=text))
```

## Weather API:
<a href="https://API.jagthefriend.repl.co/temp=Cape Town+metric">
  Example:
</a>

```py
from Complex_API import complex_api
# example: place = Cape Town
place = "name of a place"
unit = "metric" # or imperial
print(complex_api.temp(place=place, unit=unit))
```

## Youtube Playlist length finder:
<a href="https://API.jagthefriend.repl.co/length+PL59LTecnGM1OGgddJzY-0r8vdqibi3S2H">
  Example:
</a>

```py
from Complex_API import complex_api
# example URL: https://www.youtube.com/playlist?list=PL59LTecnGM1OGgddJzY-0r8vdqibi3S2H
# id = PL59LTecnGM1OGgddJzY-0r8vdqibi3S2H
play_list_link = "id"
print(complex_api.length(playlist=play_list_link))
```

## Calculator:
<a href="https://API.jagthefriend.repl.co/cal_6*9+6+9">
  Example:
</a>

```py
from Complex_API import complex_api
formula = "6*9+6+9"
print(complex_api.calculator(formula=formula))
```

## Inspire API:
<a href="https://API.jagthefriend.repl.co/inspire">
  Example:
</a>

```py
from Complex_API import complex_api
print(complex_api.inspire())
```

## Hexadecimal to Decimal(or Denary) converter:
<a href="https://API.jagthefriend.repl.co/hex+ABCDEF">
  Example:
</a>

```py
from Complex_API import complex_api
formula = "A6B9C1D1E1"
print(complex_api.hex_to_denary(hex_code=formula))
```

## Decimal(or Denary) to Binary converter:
<a href="https://API.jagthefriend.repl.co/binary=4969">
  Example:
</a>

```py
from Complex_API import complex_api
formula = "45713" # any number
print(complex_api.binary_to_denary(binary=formula))
```

If you find any bugs _or have new ideas_, <br>
Feel free to raise a
  <a href="https://github.com/JagTheFriend/Complex-API/issues">
    new issue
  </a> <br>
Or a
  <a href="https://github.com/JagTheFriend/Complex-API/pulls">
    pull request
  </a>
