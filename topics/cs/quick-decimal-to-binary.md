What I remembered today! :D I got fascinated by the topic of bitwise operations in Python - I didn't know this topic
well and decided to fill this gap, and as usual, it raised even more questions. I realized that I need to refresh my
basic knowledge of numeral systems. So, behold a quick way to convert numbers from the decimal system to binary.

1. Firstly, you need to know the powers of 2, it's easy: 2**0=1, 2**1=2, 2**2=4, 8, 16, 32, 64, 128, etc.

2. Next, you should know that the number of bits of your number in the binary system is the highest power of 2 that does
   not exceed the original number, plus 1 (because the number of bits starts from zero). For, example for 45 the largest
   power is 2**5(32) - this is 6 bits(from 0 to 5) in binary

3. Also, we need to consider that to convert, we must check EACH power of two, starting from the largest power, and
   answer the question: do we use this value to obtain the original number? If yes, we use 1; if no, we use 0. We do
   this from the largest power down to zero.

So, for example you need to convert 45(decimal) to binary. The minimum power of 2 for 45 is 2**5(32) - this is 6 bits in
binary.

45 = 32 + 8 + 4 + 1 = 2**5 + 2*3 + 2**2 + 2**0

1. 2**5(32): - OK, 1
2. 2**4(16): - NO, 32 + 16 = 48 is too large, 0
3. 2**3(8): - OK, 32 + 8 = 40, 1
4. 2**2(4) - OK, 32 + 8 + 4 = 44, 1
5. 2**1(2) - MO, 32+ 8 + 4 + 2 = 46 is too large, 0
6. 2**0(1) - OK, 32 + 8 + 4 + 1 = 45, 1

In conclusion, 45 = 101101(6 bits)


