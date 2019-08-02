# Algebraic Place Notation

APN is used to generate place notation, and hence method designs, in such a way that a method can be generated for any valid stage.

It is based on overlaying repeated place patterns to build up place notation for a method.

# Example: Plain Hunt
Standard PN on 4 bells is: ```x.14.x.14.x.14.x.14```

Standard PN on 6 bells is: ```x.16.x.16.x.16.x.16.x.16.x.16```

So the pattern we're seeing is "keep repeating the place notation pattern ```x.1n``` until we have ```2*n``` bits of place notation", with n being the stage.

In APN we write this as a 'script' that looks like this[^1]:

[^1]: If this script is run through an APN tool, it can produce the PN for any (even) stage we want

```
	base="x.1n"
	length="2*n"
```




Similarly, given the PN for plain hunt on odd stages:

PN on 5 bells is: ```5.1.5.1.5.1.5.1.5.1```

PN on 7 bells is: ```7.1.7.1.7.1.7.1.7.1.7.1.7.1.```

... the pattern is "keep repeating the place notation pattern ```n.1``` until we have ```2*n``` bits of place notation" (again, n is the stage).

In APN we would write this as:

```
	base="n.1"
	length="2*n"
```

# Example: Plain Bob

Plain Bob is the same as plain hunt, except that we change the last piece of place notation to ```12``` (on even bells).

To do this, our APN script is as follows::

```
	base="x.1n"
	length="2*n"
	pn[8]="12"
```

The ```pn[8]="12"``` line is saying "make the eighth piece of place notation be 12". This overrides the automatically generated place notation in that position taken from the ```base``` and ```length``` parts previously.

Here's a demonstration of how the ```pn[...]``` numbering applies to our Plain Bob Minor place notation:

```
    Plain Bob Minimus (one lead)

    x      <-- pn[1]
    14     <-- pn[2]
    x      <-- pn[3]
    14     <-- pn[4]
    x      <-- pn[5]
    14     <-- pn[6]
    x      <-- pn[7]
    12     <-- pn[8]

```

There's a problem with this APN though: APN is supposed to generate a method design on any number of bells, but the script given only works on 4 bells, due to the 8 in ```pn[8]="12"```.

To fix this, we can rewrite that line as:

```
    pn[2*n]="12"
```

There's an even easier way though: we can use negative numbers to signal we are counting the place notation position _backwards_ from the end of the lead, as illustrated here[^2]:

```
    Plain Bob Minimus (one lead)

    x      <-- pn[-8]
    14     <-- pn[-7]
    x      <-- pn[-6]
    14     <-- pn[-5]
    x      <-- pn[-4]
    14     <-- pn[-3]
    x      <-- pn[-2]
    12     <-- pn[-1]

```

[^2]: This is an idea borrowed from the Python programming language

So we can specify that troublesome line as ```pn[-1]="12"```. 

And so now this APN correctly generates Plain Bob on any stage of bells:

```
	base="x.1n"
	length="2*n"
	pn[-1]="12"
```

Finally, it would be useful if we could merge the even and stage variants into one script! This can be done with the ```|``` operator, which specifies two expressions: one for when T is even, and one for when T is odd, in the form ```<even expression>|<odd expression>```.

To illustrate, here's the script that generates Plain Bob for both even and odd stages:

```
	# we use pipe operator here to mean "use x1n on even stages, and n.1 on odd stages"
	base="x.1n|n.1"
	length="2*n"
	# we use pipe operator here to mean "use 12 on even stages, and 12n on odd stages"
	pn[-1]="12|12n"
```

Finally, note the use of ```#``` in this script - any lines beginning with this character are 'comments' for human consumption only.

# Metadata in APN

The ```name```, ```info``` and ```author``` tags are for self-explanatory stuff:

```
	name="My Fantastic Method"
	info="I made this method while feeding my cats"
	author="Alex"
```

## Stage info

Although APN is meant to describe methods in a general multi-stage way, sometimes there are limitations to a method, such as it being even or odd bell only, or only working on certain specific range of stages.

Such limitations can be put into the APN script; see the following examples:

```
	# this method is ony valid on odd stages
	validstages=odd

	# this method is only valid on even stages from 6 upwards (e.g. Cambridge Surprise)
	validstages=even
	minimumstage=6

	# this method is only valid on even stages from 6 to 10
	validstages=even
	minimumstage=6
	maximumstage=10

	# this method is only valid on exactly these stages
	validstages=7,9,11
```

# Treble-bob hunting

This is the 'grid' or basis for surprise methods:

```
	name="Treble Bob Hunting"
	info="This is false, obviously"
	validstages=even
	base="x.1n.x.x"
	length="4*n"
```


# Further APN examples

## Grandsire

```
	minimumstage=5
	base="x.1n|n.1"
	length="2*n"
	pn[1]="3n|3"
```

## Little Bob

```
	validstages=even
	minimumstage=6
	base="x.1n"
	# a lead in LB is 8 changes on every stage
	length="8"
	pn[4]="14"
	pn[-1]="12"
```

## Odd Little Bob


Just for hoots; the nearest thing structurally to Little Bob on odd numbers:

```
	validstages=odd
	minimumstage=7
	base="n.1"
	length="8"
	pn[4]="147"
	pn[-1]="127"
```

I use the word 'pesudo' because this method has a different structure to Little Bob - it's a two-part differential, with half of the bells doing only the 'quick' work (dodges in 3-4, no 2nds), and half doing only the 'slow' work (no dodge in 3-4, make 2nds over treble). Every working bell makes 4 blows when lying (and no dodging at the back).


# Hints on working out the APN for a method

Concentrate on the places, not on dodges, in much the same way as place notation; once the places are nailed down, the correct dodging, points etc just happens.

Examining the higher stages of the method is most useful. For example, looking at Bristol 8 and 10 almost gives you the pattern; but looking at 8, 10 and 16 is better.

Start from the basic 'grid' for your kind of method (e.g. plain hunt or treble bob) then add the refinements that make it into the target method.


-----------------

```
alex.hunsley@gmail.com
```


