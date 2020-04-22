# Change ringing: exploring method enumeration

## Glossary

In this article, by 'method' I'm referring to place notation which represents a lead (or a six or block etc) of a method.

## Equivelant methods

If we generate a collection of methods, we'll find that although they're distinct in terms of place notation, a lot of them will be the same method for all intents and purposes. This is usually because one or more of the following are true:

1. one method has the reverse place notation of the other (example: x.12.34.16 and 16.34.12.x)
2. one method has place notation which is just a rotation of another (example: x.12.34.16 and 12.34.16.x)

When either (or both) of the above are true for two methods, we say they are *equivalent* methods. We consider them to be duplicates, and we are usually not interested in seeing duplicates when generating methods.

## Canonical form of a method

In order to help with removing duplicate methods during method generation, it's useful to have a way to convert a method's place notation $M$ to a *canonical form*[^1] of place notation $M_c$. We want the canonical form to meet these conditions:

1. $M$ and $M_c$ are *equivelant* (note: we will see that $M = M_c$ when $M$ is already in canonical form by chance)
2. any methods equivalent to $M$ will also have canonical form $M_c$

### An algorithm for finding the canonical form

Suppose we have generated a method $Q$ using a list of $m$ place notations selected from a dictionary $\{p_0, p_1, ... p_{m-1}\}$. 

Our generated method's PN can be written down as a list of indexes into the dictionary, for example: $(0, 2, 0, 7, ...)$.

We can convert such an index list into an integer (call it the 'measure') by considering it to be a string of digits base in L. 

Now, convert *all possible rotations* of our place notation index list and *all possible rotations of its reversal*[^rev] into measures.

The canonical form of our method is the place notation corresponding to the the largest measure.

Note that if find a largest measure in several different rotations, the place notation contains repetitions of a shorter, and you can choose any of the contenders (as they will all be the same place notation).

[^rev] hello

### Worked example of finding canonical form

Suppose we're considering minimus methods. Our dictionary of place notations on stage 4 is $\{``x", ``12", ``14", ``34"\}$, and the method we want to convert to canonical form is Plain Bob Minimus, with PN being ```x.14.x.14.x.14.x.12```.

We re-write each rotation of our PN and its reversal as a measure:

place notation         as indexes into dictionary    as measure integer
---------------------  ----------------------------  ------------------
`x.14.x.14.x.14.x.12`  $(0, 2, 0, 2, 0, 2, 0, 1)$    $02020201_4 = 8737$
`14.x.14.x.14.x.12.x`  $(2, 0, 2, 0, 2, 0, 1, 0)$    $20202010_4 = 34948$
`x.14.x.14.x.12.x.14`  $(0, 2, 0, 2, 0, 1, 0, 2)$    $02020102_4 = 8722$
`14.x.14.x.12.x.14.x`  $(2, 0, 2, 0, 1, 0, 2, 0)$    $20201020_4 = 34888$
`x.14.x.12.x.14.x.14`  $(0, 2, 0, 1, 0, 2, 0, 2)$    $02010202_4 = 8482$
`14.x.12.x.14.x.14.x`  $(2, 0, 1, 0, 2, 0, 2, 0)$    $20102020_4 = 33928$
`x.12.x.14.x.14.x.14`  $(0, 1, 0, 2, 0, 2, 0, 2)$    $01020202_4 = 4642$
`12.x.14.x.14.x.14.x`  $(1, 0, 2, 0, 2, 0, 2, 0)$    $10202020_4 = 18568$

The largest measure here is 34948, for the second row. Therefore the place notation for that row is the canonical form of this method: `14.x.14.x.14.x.12.x`.

You might rightly balk at the idea of a method beginning with the treble making a place! Can we make our canonical notation algorithm more palatable? Happily, yes; items towards the end of the place notation dictionary tend to appear at the start of the canonical place notation produced, so we can tweak our PN dictionary to instead be $\{``12", ``14", ``34", ``x"\}$. This results in our canonical PN for Plain Bob Minimus being the usual PN: `x.14.x.14.x.14.x.12`.


[^1]: Algorithmic aside: canonical form is useful because it reduces runtime complexity in comparing methods to each other, e.g. de-duplicating a collection of methods

## rest

divisor function: $\sigma_x(n)=\sum_{d\mid n} d^x$

https://oeis.org/A051137

Non-reversed and non-rotated.

$$
T(n, k) = \frac{k^{\lfloor (n+1)/2 \rfloor} + k^{\lceil (n+1)/2 \rceil}} {4} + \frac{ \sum_{d\mid n} \phi (d) \cdot k^{n/d} } {2n}
$$

```
T(n, k) = (k^floor((n+1)/2) + k^ceiling((n+1)/2)) / 4 + (1/2n) * Sum_{d divides n} phi(d) * k^(n/d)
```

If we want to try to count how many possible methods there are of various types (plain, treble bob, etc) on different stages, we start with a fundamental question: 

*How many distinct place notations are there for a row on stage* n?

Let's start with an example, a list of all possible place notation[^2] for stage 4:

[^2]: We only deal with well-formed place notation in this article. By this we mean that all places made are explicit. For example, on stage 6, these are badly formed: `1` (should be `16`), `134` (should be `1234`).

Schematic  Place notation
---------  -------------------
`1234`       
`><><`       `x`
`><||`       `34`
`|><|`       `14`
`||><`       `12`
`||||`       `1234`
---------  -------------------

Table: All possible place notations for stage 4

Note that we use `><` to represent two bells crossing: we use two characters because of course two bells are involved. The `|` character represents a bell remaining in place.

This is looking like a combinatorial problem -- given $a$ items, choose $b$ of them -- but there's a catch here: the `><` occupies two characters, but it represents a single thing conceptually: two bells crossing. To add some clarity, let's rewrite our table, but using `x` instead of `><`:

Schematic  Place notation
---------  -------------------
`xx`       `x`
`x||`      `34`
`|x|`      `14`
`||x`      `12`
`||||`     `1234`
---------  -------------------

Table: Altered schematic for all possible PN for stage 4

Since the string for each code above contains a single character -- "`x`" or "`|`" -- for each possibility, it's more like an *a choose b* combinatorial problem. But note that we have strings of varying lengths. 

With a little thought you can see that the length of each string is $n$ minus the count of $x$ in the string. And from there we can break this down into $_n\mathrm{C}_r$ expressions for combinations of `x` in the string:

Code       string length $x$ count Combinations for $x$ occuring
---------  ------------- --------- -----------------------------
`xx`        2            2         $_2\mathrm{C}_2 = 1$ 
`x||`       3            1         ]
`|x|`       3            1         ] $_3\mathrm{C}_1 = 3$
`||x`       3            1         ]
`||||`      4            0         $_4\mathrm{C}_0 = 1$
---------  ------------- -------   -----------------------------

 
Let's use $\mathbb{P}(n)$ to denote 'number of possible place notations on stage $n$'. In this case we have:

$$\mathbb{P}(4) = {_2\mathrm{C}_2} + {_3\mathrm{C}_1} + {_4\mathrm{C}_0} = 5$$

If you analyse stage 5, you get:

$$\mathbb{P}(5) = {_3\mathrm{C}_2} + {_4\mathrm{C}_1} + {_5\mathrm{C}_0} = 5$$


And for stage 6:

$$\mathbb{P}(6) = {_3\mathrm{C}_3} + {_4\mathrm{C}_2} + {_5\mathrm{C}_1} + {_6\mathrm{C}_0} = 8$$

There's a pretty obvious pattern emerging. The equation for any stage is:

\begin{equation}
\mathbb{P}(n) = \sum_{i=0}^{\lfloor n/2 \rfloor} {_{n-i}\mathrm{C}_i}
\end{equation}

If you look at the first few values for the $\mathbb{P}$ function, you'll see a familiar sequence emerging:

n                0  1  2  3  4  5  6  7  8  9
---              -- -- -- -- -- -- -- -- -- --
$\mathbb{P}(n)$  1  1  2  3  5  8  13 21 34 55

It's the Fibonacci sequence[^3]. So we now have a tidy definition for $\mathbb{P}$:
 
\begin{equation}
\begin{split}
\mathbb{P}(n) = fib(n+1)
\end{split}
\end{equation}

See Appendix A for an aside on Fibonacci in Pascal's Triangle.

 [^3]: Proofs are available, e.g. by induction, that the given combinatorial sum in (1) gives the terms in the Fibonacci sequence

## No-constraint method with plain lead length

This is a method of lead length $2n$ and no other restrictions on content.

## Plain hunt methods

Schematic               Combos
-----------------       -------------------
`12345678`   
`><......`                $\mathbb{P}(6)$ or $\mathbb{S}(0,6)$ 
`|><.....`                $\mathbb{P}(5)$ or $\mathbb{S}(1,5)$
`..><....`                $\mathbb{S}(2,4)$
`...><...`                $\mathbb{S}(3,3)$
`....><..`                $\mathbb{S}(4,2)$ 
`.....><|`                $\mathbb{P}(5)$ or $\mathbb{S}(5,1)$
`......><`                $\mathbb{P}(6)$ or $\mathbb{S}(6,0)$
`.......|`                $\mathbb{P}(7) - 1$
\hphantom{xxxxx}`><|`
\hphantom{xxxx}`><`
\hphantom{xxx}`><`
\hphantom{xx}`><`
`|><`
`><`
`|.......`                $\mathbb{P}(7) - 1$
-----------------       --------------------

Table: Plain Hunt Major combinations schematic



Schematic               Combos
-----------------       -------------------
`123456789`   
`><.......`                $\mathbb{P}(7)$ or $\mathbb{S}(0,7)$ 
`|><......`                $\mathbb{P}(6)$ or $\mathbb{S}(1,6)$ 
`..><.....`                $\mathbb{S}(2,5)$
`...><....`                $\mathbb{S}(3,4)$
`....><...`                $\mathbb{S}(4,3)$ or $\mathbb{S}(3,4)$
`.....><..`                $\mathbb{S}(5,2)$ or $\mathbb{S}(2,5)$
`......><|`                $\mathbb{P}(6)$ or $\mathbb{S}(6,1)$ 
`.......><`                $\mathbb{P}(7)$ or $\mathbb{S}(7,0)$
`........|`                $\mathbb{P}(8) - 1$
\hphantom{xxxxx}\vdots
`|........`                $\mathbb{P}(8) - 1$
-----------------       --------------------

Table: Plain Hunt Caters combinations schematic




Schematic               Combos
-----------------       -------------------
`123456789E`   
`><........`                $\mathbb{P}(8)$
`|><.......`                $\mathbb{P}(7)$
`..><......`                $\mathbb{S}(2,6)$
`...><.....`                $\mathbb{S}(3,5)$
`....><....`                $\mathbb{S}(4,4)$
`.....><...`                $\mathbb{S}(5,3)$ or $\mathbb{S}(3,5)$
`......><..`                $\mathbb{S}(6,2)$ or $\mathbb{S}(2,6)$
`.......><|`                $\mathbb{P}(7)$
`........><`                $\mathbb{P}(8)$
`.........|`                $\mathbb{P}(9) - 1$
\hphantom{xxxxx}\vdots
`|.........`                $\mathbb{P}(9) - 1$
-----------------       --------------------

Table: Plain Hunt Royal combinations schematic

$$\mathbb{C}_p(n) = \prod_{i=2}^{n-4} fib(i)$$

# scratch 

## Fibonacci factorial ('fibofac') definition

Method type             Denoted           Definition
------------         --------------       ----------------
Plain Double         $\mathbb{C}_{pd}(n)$ $f\!\!f(n)$
Plain                $\mathbb{C}_p(n)$    $f\!\!f(n)^2$
Treble Bob Double    $\mathbb{C}_{td}(n)$ $f\!\!f(n)^4$
Treble Bob           $\mathbb{C}_t(n)$    $f\!\!f(n)^8$
---------            --------------       ----------------

$$ f\!\!f(n) = \prod_{i=0}^{n} fib(i)$$

$$ \dot a = fib(a)$$


${n \choose x}$

## Split parity paradox

$_n\mathrm{C}_{r-1} \cdot b$

$_n\mathrm{C}_r-1$

$\ddot 8 \cdot \dot 7 !$

$f\!\!f(7)$

$ff(7)$

\newpage

# Appendix A: Fibonacci and Pascal's Triangle

We know that $\mathbb{P}(n)$ is the sum of $_n\mathrm{C}_r$ combinatorial terms, and that these terms can be read off Pascal's Triangle.

This means that if you view Pascal's triangle left-aligned, the Fibonacci numbers (and hence $\mathbb{P}(n)$) appear as the sum of diagonals running SW-NE:

![](images/pascalsDiagonalsFibonacci.png "title"){height=300px}

If you skew the triangle rows more to the right, the pattern is even more obvious:

![](images/pascalsDiagonalsFibonacci-sheared5.png "title"){height=300px}

[comment]: <> (\includegraphics{images/pascalsDiagonalsFibonacci.png})


