# mcuser


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)
> Module for parsing Minecraft playerdb.co

> testing python version 3.8

## Synchronous
```py
from mcuser import MCuser


def main():
    Main = MCuser.lookup("username or user uuid of id")
    Text = Main.user_check() #return dict
    User = Main.user_name() #return str
    Userid = Main.user_id() #return str
    Userrawid = Main.user_rawid() #retrun str
    Useravatar = Main.user_avatar() #return str url

main()
```

## Asynchronous
```py
import asyncio
from mcuser import asyncMCuser


async def main():
    Main = await asyncMCuser.lookup("username or user uuid of id")
    Text = await Main.user_check() #return dict
    User = await Main.user_name() #return str
    Userid = await Main.user_id() #return str
    Userrawid = await Main.user_rawid() #retrun str
    Useravatar = await Main.user_avatar() #return str url

asyncio.run(main())
```

