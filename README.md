AlgLearn by ddthj/SquidFairy
Alglearn is a tool to help cubers learn new algorythms.

The user can set up the algorythms they wish to learn in the program's "algset.txt," and Alglearn will then test the user on their ability
to solve these algorithms quickly.

There are a few different modes Alglearn can use, the mode is selected in the "algset.txt" file.
In mode 0, AlgLearn chooses from the given algorithms randomly
In mode 1, AlgLearn chooses algorithms based on which one has your highest average solve time
In mode 2, AlgLearn chooses the algorithm with your lowest average turns per second, this one is probably best for practice
In mode 3, Alglearn chooses any algorithm with an average above a set time in the format: #!mode:3:<time to beat>

The minimum information required to create a custom algset.txt file is as follows:

```
#!mode:2 
Name:Algorithm
```

Note that any mode could be used

If for some reason AlgLearn is only giving you one algorithm, you might have an improperly formatted algset file.
