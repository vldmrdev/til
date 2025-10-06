### Bitwise operations in Python are interesting! 
As you know, all symbols can be converted to a numeric representation in Unicode, and thus, through the numeric representation, one symbol can be replaced with another.

We will use:

- ord() - converts characters to Unicode number
- chr() - converts Unicode number to characters 
- ^ or XOR(Exclusive OR)  - gives 1 if the bits differ and 0 if they are the same.

For example, we need convert 'A' to 'X'. In bitwise it's:
```
'0b1000001'
^
'0b1011000' =
'0b0011001'
```
because ```bin(ord('A')) == '0b1000001'```, ```bin(ord('X')) =='0b1011000' ``` and using XOR we get ```'0b11001'``` or ```'0b0011001'``` - I added zeros to the left for proportion but this doesn't affect the result because multiplying 0 by a power of 2 when converting from binary to decimal still gives 0.

Or like this:

```python
>>> 65 ^ 88
25
```

### How to use it in Python?

- Get Unicode numbers:

```python
>>> ord('A')
65
>>> ord('X')
88
```

- Get a bitmask - it's the difference between the Unicode values of the characters:
```python
>>> ord('A') ^ ord('X')
25
```

- Convert A to X:

```python
>>> chr(ord('A') ^ 25)
'X'
```
A to X in binary:
```
'0b1000001'
^
'0b0011001'=
'0b1011000'
```

or X to A:
```python
>>> chr(ord('X') ^ 25)
'A'
```

X to A in binary:
```
'0b1011000'
^
'0b0011001'=
'0b1000001'
```

Reverse conversion from binary to Unicode decimal numbers:

```python
>>> int('0b11001', 2)
25
>>> int('0b0011001', 2)
25
>>> int('0b1000001', 2)
65
>>> int('0b1011000', 2)
88
```


