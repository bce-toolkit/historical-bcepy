BCE Core
===================

The main function of this program is to **balance chemical equations** and help you **deal with complex chemical equations**. It also contains some unique features.

Features
-------------

 - Balance chemical equations (includes ionic equations, equations with multi-solutions, equations with SRU, equations with hydrates, electronic transferring equations, equations with abbreviations and indefinite equations).
 - Substitute unknown symbols in chemical equations which contain one or more unknown symbols.
 - Auto-correction (wrong side, useless substance or wrong balanced coefficient).
 - Predefined abbreviations and user custom abbreviations.
 - Humanity error output.
 - High precision calculation, hardware is the only limitation.
 - Cross platform (fully written by Python).
 - Multi languages support (English and Simplified-Chinese are supported currently).
 - Simple API to help you integrate this library to your own application.
 - Output to BCE-syntax-based expression or MathML.

Installation
-------------

Type following commands in your terminal to install BCE:

```
python setup.py build
python setup.py install
```

If you are using Linux/UNIX, please run these commands in root privilege. Typically, you can use command **su** or **sudo**.

Usage
-------------

After installation, you can run BCE in your terminal by typing following command:
```
bce-cli
```
It has following arguments:

| Argument        | Description                    |
|-----------------|--------------------------------|
| -h, --help      | Show the help message.         |
| --output-mathml | Show output in MathML format.  |
| --no-banner     | Don't show banner when loaded. |

Syntax (and examples)
-------------

### Basic syntax

The BCE syntax is simple and just like the hand-writing style. For example:

```
>> Na2CO3+HCl=NaCl+H2O+CO2
Na2CO3+2HCl=2NaCl+H2O+CO2
```

Here are the basic rules:

> 1. Use '=' to separate the reactants and the products.
> 2. Use '+' to connect each substance.
> 3. The syntax of the atom symbol is case-sensitive. The first letter of one atom symbol must be upper-case and others must be lower-case. 

In one molecule, you can specify the charge by adding "<{n}e+>" or "<{n}e->" at the end. {n} is a variable and it can be ignored if {n} equals to 1. For example:

```
>> Cl2+<e->=Cl<e->
Cl2+2<e->=2Cl<e->
>> Cu+Fe<3e+>=Cu<2e+>+Fe<2e+>
Cu+2Fe<3e+>=Cu<2e+>+2Fe<2e+>
```

Equations with multi-solutions are also supported. For example:

```
>> C+O2=CO+CO2
{2*Xa+2*Xb}C+{Xa+2*Xb}O2={2*Xa}CO+{2*Xb}CO2
>> Cu+HNO3=Cu(NO3)2+NO+NO2+H2O
{-Xa+3*Xb}Cu+{8*Xb}HNO3={-Xa+3*Xb}Cu(NO3)2+{-2*Xa+2*Xb}NO+{4*Xa}NO2+{4*Xb}H2O
```

In this example, 'Xa' and 'Xb' are variables. You can do subsitution by assigning values to them.

### Hydrates

Hydrate molecules are supported. Use "." to describe hydrate dots. For example:

```
>> CuSO4.5H2O=CuSO4+H2O
CuSO4.5H2O=CuSO4+5H2O
>> LiOH+H2O2+H2O=Li2O2.H2O2.3H2O
2LiOH+2H2O2+H2O=Li2O2.H2O2.3H2O
```

### Abbreviations

In hand writing, we always use abbreviations such as Et, Ph and Ac. In BCE, you can also use abbreviations. Just surround the abbreviation with "[" and "]". For example:

```
>> [Et]OH+O2=CO2+H2O
[Et]OH+3O2=2CO2+3H2O
```

For all supported abbreviations, please open "docs/abbreviations/abbr_ref_book.pdf".

### Variables and expressions

You can use expressions and variables in your chemical equation. For example:

```
>> C{n}H{2n+2}+O2=CO2+H2O
{(n+1)^(-1)}C{n}H{2*n+2}+{(1/2)*(3*n+1)/(n+1)}O2={n/(n+1)}CO2+H2O
>> CH3(CHCH){n}CH3+Cl2=CH3(CHClCHCl){n}CH3
CH3(CHCH){n}CH3+{n}Cl2=CH3(CHClCHCl){n}CH3
>> X-<e->=X<{n}e+>
X-{n}<e->=X<{n}e+>
```

One thing that you may need to pay attention to is that the first letter of the variables you use can't be 'X'. Variables start with 'X' are reserved by the program.

In one expression, you can use operators "+", "-", "*", "/" and "^" ("^" means power, such as 2^3=8). You can also use functions listed in following table:

| Function | Description                      |
|----------|----------------------------------|
| sqrt(x)  | The square root of variable 'x'. |
| pow(x,y) | Equals to x^y.                   |

### Automatic side arranging

If you get several substances and you don't know which are reactants and which are products, you can use ";" to separate each substance and type them to BCE. The program will help you decide the reactants and the products. For example:

```
>> NH4Cl;K2(HgI4);KCl;KI;H2O;Hg2NH2OI;KOH
NH4Cl+2K2(HgI4)+4KOH=KCl+7KI+3H2O+Hg2NH2OI
```

We have to acknowledge that the solving algorithm has some limitations. Currently, the algorithm can't decide the reaction direction precisely. You may have to decide it yourself. For example:

```
>> CH4;HCN;NH3;O2;H2O
2HCN+6H2O=2CH4+2NH3+3O2
```

The correction result should be:

```
2CH4+2NH3+3O2=2HCN+6H2O
```

To avoid this condition, you can specify the status of each substance by adding "(g)", "(l)", "(s)", "(aq)" at the end to let the program guess the reaction direction. For example.

```
>> CH4(g);HCN(g);NH3(g);O2(g);H2O(g)
2CH4(g)+2NH3(g)+3O2(g)=2HCN(g)+6H2O(g)
```

It is correct now.

Also, the program can't balance the equation if it has multi solutions. The program will report a logic error in such condition. For example:

```
>> C;CO2;CO;O2
A logic error occurred (Code: LE.BCE.ARMW):

Description:

    Can't balance chemical equations that have multiple answers.
```

Reusable components
-------------------
 - The whole program can be used as a library.
 - Chemical equation parser (with BCE syntax).
 - Molecule equation parser (with BCE syntax).
 - Electronic expression parser (with BCE syntax).
 - Math expression parser.
 - Linear equations solver.

Dependencies
-------------

 - [SymPy](http://www.sympy.org/)

Documentation
--------------------

See the files in "docs" directory.
