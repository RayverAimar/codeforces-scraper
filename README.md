<div align="center">

# codeforces-scraper

</div>

Codeforces scraper made to retrieve public information about specific users in codeforces like rating changes, solved problems in specific contests or not among others functionalities.

## Usage
You may need to know the `user_name` for almost all functionalities for the scraper
```
1. Display codeforces top-ten-rated info
2. Get historical solved problems by an user
3. Get solved problems with specific tag by an user
4. Get rating change of an user
5. Get solved problems in a contest by an specific user
Type your option: 4
User name: tourist
```
This option gets the historical rating change in codeforces, pointing out the highest rating got and an additional plot about its rating change


```
Displaying info of tourist...
        Total of participated public contests: 238
        Highest rating got: 3979
Current user rating: 3706
```
<div align="center">

![rating change](https://media.discordapp.net/attachments/886256698640171008/1086456023587487765/image.png?width=445&height=334)

</div>

You can also get solved problems in an specific contest by knowin its id, the method can retrieve between the problems solved as a `CONTESTANT` or as a `PRACTICING` (it returns problems solved as a `CONTESTANT` by default)
```
...
Type your option: 5
User name: tourist
contestId: 1774

8 solved problems.
    1) Segment Covering
    2) Magician and Pigs (Hard Version)
    3) Magician and Pigs (Easy Version)
    4) Two Chess Pieces
    5) Ice and Fire
    6) Coloring
    7) Same Count One
    8) Add Plus Minus Sign
```