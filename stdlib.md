# Pain Standard Library

This document describes all built-in functions available in the Pain language.

---

## Math Functions

### `abs`

Returns the absolute value of an integer

**Signature:**
```pain
fn abs(x: int) -> int
```

**Parameters:**
- `x`: int

**Returns:**
- `int`


### `abs`

Returns the absolute value of a float

**Signature:**
```pain
fn abs(x: float64) -> float64
```

**Parameters:**
- `x`: float64

**Returns:**
- `float64`


### `min`

Returns the minimum of two integers

**Signature:**
```pain
fn min(a: int, b: int) -> int
```

**Parameters:**
- `a`: int
- `b`: int

**Returns:**
- `int`


### `max`

Returns the maximum of two integers

**Signature:**
```pain
fn max(a: int, b: int) -> int
```

**Parameters:**
- `a`: int
- `b`: int

**Returns:**
- `int`


### `sqrt`

Returns the square root of a number

**Signature:**
```pain
fn sqrt(x: float64) -> float64
```

**Parameters:**
- `x`: float64

**Returns:**
- `float64`


### `pow`

Returns base raised to the power of exp

**Signature:**
```pain
fn pow(base: float64, exp: float64) -> float64
```

**Parameters:**
- `base`: float64
- `exp`: float64

**Returns:**
- `float64`


### `sin`

Returns the sine of x (in radians)

**Signature:**
```pain
fn sin(x: float64) -> float64
```

**Parameters:**
- `x`: float64

**Returns:**
- `float64`


### `cos`

Returns the cosine of x (in radians)

**Signature:**
```pain
fn cos(x: float64) -> float64
```

**Parameters:**
- `x`: float64

**Returns:**
- `float64`


### `floor`

Returns the floor of x

**Signature:**
```pain
fn floor(x: float64) -> float64
```

**Parameters:**
- `x`: float64

**Returns:**
- `float64`


### `ceil`

Returns the ceiling of x

**Signature:**
```pain
fn ceil(x: float64) -> float64
```

**Parameters:**
- `x`: float64

**Returns:**
- `float64`



## String Functions

### `len`

Returns the length of a string

**Signature:**
```pain
fn len(s: str) -> int
```

**Parameters:**
- `s`: str

**Returns:**
- `int`


### `concat`

Concatenates two strings

**Signature:**
```pain
fn concat(a: str, b: str) -> str
```

**Parameters:**
- `a`: str
- `b`: str

**Returns:**
- `str`


### `substring`

Returns a substring from start to end (exclusive)

**Signature:**
```pain
fn substring(s: str, start: int, end: int) -> str
```

**Parameters:**
- `s`: str
- `start`: int
- `end`: int

**Returns:**
- `str`


### `contains`

Returns true if string contains substring

**Signature:**
```pain
fn contains(s: str, substr: str) -> bool
```

**Parameters:**
- `s`: str
- `substr`: str

**Returns:**
- `bool`


### `starts_with`

Returns true if string starts with prefix

**Signature:**
```pain
fn starts_with(s: str, prefix: str) -> bool
```

**Parameters:**
- `s`: str
- `prefix`: str

**Returns:**
- `bool`


### `ends_with`

Returns true if string ends with suffix

**Signature:**
```pain
fn ends_with(s: str, suffix: str) -> bool
```

**Parameters:**
- `s`: str
- `suffix`: str

**Returns:**
- `bool`


### `trim`

Returns string with leading and trailing whitespace removed

**Signature:**
```pain
fn trim(s: str) -> str
```

**Parameters:**
- `s`: str

**Returns:**
- `str`


### `to_int`

Converts string to integer

**Signature:**
```pain
fn to_int(s: str) -> int
```

**Parameters:**
- `s`: str

**Returns:**
- `int`


### `to_float`

Converts string to float

**Signature:**
```pain
fn to_float(s: str) -> float64
```

**Parameters:**
- `s`: str

**Returns:**
- `float64`


### `to_string`

Converts integer to string

**Signature:**
```pain
fn to_string(x: int) -> str
```

**Parameters:**
- `x`: int

**Returns:**
- `str`



