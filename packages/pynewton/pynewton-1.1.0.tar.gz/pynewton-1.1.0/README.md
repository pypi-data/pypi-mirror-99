# PyNewton

An `asnycio`-based  wrapper for [Newton](https://newton.now.sh).
The Github project can be found [here.](https://github.com/aunyks/newton-api)

## Installation
```
pip install git+https://github.com/HitaloSama/pynewton
```

## Example

```py
import asyncio
import pynewton

# Get event loop
loop = asyncio.get_event_loop()

async def main():
    # Get calculation for `to_calculate`.
    to_calculate = input("Expression: ") # 2^2+2(2)
    
    # Return a Result object with `operation`, `expression`
    # and `result` as attributes.
    result = await pynewton.simplify(to_calculate)
    print(result)

loop.run_until_complete(main())
```
