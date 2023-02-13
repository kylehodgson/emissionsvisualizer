# Emissions Visualization

The idea here is to log all of the data I can log about local conditions.
 - EV chargers from EnelX
 - air quality stats from purple air
 - grid generation stats from gridwatch and possibly pyiso
 - MOER from wattTime
 - electricity usage from my utility possibly green button
 - indoor stats from our Dyson
 - heating stats from thermo, Nest, Flair, and possibly Google Home
..... and then report on them. somehow.

## Sources

### Juice Net / ENELX

If you have a JuiceBox charger, you can get your JuiceNet API key via the [portal](https://home.juice.net/Manage) 

### Purple Air

For a Purple Air API key, check [api.purpleair.com](https://api.purpleair.com/). When I got started with them, one requested an API key at contact@purpleair.com.

### Watt Time

WattTime, at [WattTime.org](https://www.watttime.org/api-documentation), does not at this time extend a portal where you can create an API key. However, using the Python repl you can create one yourself via the simplemoer library:

```python
$ pip install simplemoer
$ python
Python 3.11.2 (main, Feb 11 2023, 22:25:20) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from simplemoer.client import WattTime
>>> wt=WattTime()
>>> resp=wt.register("gudusername1234","!bestpassword1234","your.inbox+simplemoer@gmail.com")
>>> resp
{'user': 'testusername1234', 'ok': 'User created'}
>>> 
```

### GridWatch

GridWatch is a bit more of a screen scrape than a proper API at this time. 

GridWatch only covers Ontario's IESO at this time unfortunately.

I may replace it with WattTime's excellent, though currently uninstallable, [pyiso](https://github.com/WattTime/pyiso).