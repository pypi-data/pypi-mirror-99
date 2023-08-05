<h1 align="center">quantuiti</h1>

<p align="center">
  <a href='https://quantuiti.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/quantuiti/badge/?version=latest' alt='Documentation Status' />
  </a>
</p>

quantuiti is a platform designed to make automated trading easier

currently quantuiti only allows backtesting of algorithms with a limited amount of indicators, we plan on expanding to paper trading and live trading with a lot more indicators.


### To get started install qantuiti python package:
- windows
```Shell
python -m pip install quantuiti
```
- Linux/MacOS
```Shell
python3 -m pip install quantuiti
```

### Create a new python file then import quantuiti engine
```Python
from quantuiti import Engine
```

### Initalize quantuiti engine
```Python
Engine = Engine()
```

### Instantiate algorithm
```Python
@Engine.algorithm
def algo():
  if self.ema(20) > self.ema(100):
    self.buy()
  else:
  self.sell()
```

### example of an EMA crossover strategy
```Python
from quantuiti import Engine
Engine = Engine()

@Engine.algorithm
def algo():
  if self.ema(20) > self.ema(100):
    self.buy()
   else:
    self.sell()
```