![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xltoy)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/glaucouri/xltoy)
![Travis (.com)](https://img.shields.io/travis/com/glaucouri/xltoy)


## XLtoy: 

The ultimate toolkit for Microsoft Excel modelers and model-ops. 

#### The name

*XLtoy* it's a word pun that starts from **exel to py** concept, but the *p* seem superfluous here and *xlto(p)y* became 
XLtoy, more funny.

### Description

Excel is a good instrument to do analysis activities, model design, reporting and so on, his intuitiveness is the 
main reason why it is so diffused all around the world. On the other hand, its great diffusion sees it involved in other 
phases of deploy process. Generally, when excel cross the frontier in processes that involve IT departments it does not perform 
very well, i mean: change management, error handling, big data, parallel execution, cross platform, deploy on cloud and so on.
Much of this work is entrusted to the IT department, which works to address these shortcomings.

XLtoy framework come to help this side, it can read, parse, diff, validate, manage changes and run out of the box complicated 
models written using Microsoft Excel. Not all features are ready up to now, but the development plan is show below.

This tool is useful for users that write, share, maintain and deploy models written in Excel. 

- It can:
   - Read data and formulas and store they in standard formats like json or YAML.
   - Parse formulas and identify interdependencies between equations.
   - Many kind of model are well handled by XLtoy like:
       - validation models
       - rule based models
       - financial models   
       - forecasting models

In a collaborative environment, for example, a change management tools, can save a lot of time and money. 
No less, dev-ops (od mod-ops) than need an instrument to identify uniquely model, data, and changes on each delivery. 
Model differ can identify precisely which and where are the differences using syntactic or semantic algorithm.
Topological analisys can help to identify interdependencies between formulas.


### How it works
Analyze an entire workbook, is too difficult, and often useless, this approach force to write unpredictable an inefficient 
algorithms and doesn't work because often we are interested only in a subset of an entire workbook. So main idea, is to 
identify a subset of areas of interest, defined as *working areas* and focus XLtoy only on these.
Working areas are Named range defined by user,  they follow some pattern and address algotithms. So with minimum changes 
to an existent sheet, the parser can handle it and produce useful information. 
If you can apply some **simple [rules](https://raw.githubusercontent.com/glaucouri/xltoy/main/rules.md)**
you are ready to go!
All other operations are done *out of the box* using command line in order to promote automations and compatibility with 
all platforms.


### Installation
It's strongly suggested to use virtualenv:
```
>pip3 install virtualenv
>python3 -m venv XLtoy_pyenv
>source XLtoy_pyenv/bin/activate
```

```
>pip install xltoy

# Or from source:

>git clone https://github.com/glaucouri/XLtoy.git
>cd XLtoy/
>python setup.py install
```

All features now are accessible via *xltoy* cli command.

```
$ xltoy --help

Usage: xltoy [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  collect
  diff

```
### Documentation

```
$ xltoy collect --help
Usage: xltoy collect [OPTIONS] FILENAME

Options:
  --timeit            Print out how many times it takes for the task
  --yaml              Print out the yaml hierarchical view
  --json              Print out the json hierarchical view
  --gml_graph PATH    save to a file the topology of models in gml format
  --data              Collect only data, it will ignore formulas
  -v, --verbose       verbose output (repeat for increased verbosity)
  --add_fingerprint   Enable fingerprint metadata informations, under section
                      xltoy

  --parsed            Parse formulas and use this version instead of excel
                      syntax

  --tag TEXT          Add a tag attribute to fingerprint eg: --tag v1.0
  --description TEXT  Add a description attribute to fingerprint eg:
                      --description model 2020Q1

  --help              Show this message and exit.

$ xltoy diff  --help
Usage: xltoy diff [OPTIONS] FILENAME1 FILENAME2

Options:
  --timeit         Print out how many times it takes for the task
  --data           Collect only data, it will ignore formulas
  --relative       Areas are handled as relative, each starts from row1,col1
  -v, --verbose    verbose output (repeat for increased verbosity)
  --nofingerprint  Ignore fingerprint metadata, under section xltoy
  --parsed         Parse formulas and use this version instead of excel syntax
  --json           Print out in json format instead of default YAML
  --help           Show this message and exit.

 
```
Follow tutorials to a deep dive into all features 
* [working rules](https://raw.githubusercontent.com/glaucouri/xltoy/main/rules.md)  How to manage working areas and how works the parser
* [Tutorial1](https://raw.githubusercontent.com/glaucouri/xltoy/main/tutorial.md) How to manage values 
* [Tutorial2](https://raw.githubusercontent.com/glaucouri/xltoy/main/tutorial2.md) How to manage models and formulas


#### Framework descriptions

The XLtoy Framework is composed of many subpackages, all of them are reachable via cli sub command.

* **xltoy.collector** : It read an excel workbook and extract all needed information, following rules described here. 
This means equations, named or anonymous exogenous data and parameters. 
Result can be represented as hierarchical yaml or json. This functionality solve problem related 
to *change management*, *versioning*, *model governance* and *diff* operation.

* **xltoy.parser** : It can parse all collected equation in order to understand for each all the dependencies, 
and transliterate each in a readable and working python code.
All relations between formulas are stored in a dependency graph in a key:value structure 
using the mnemonic name for each equation. This data structure allow us to do a topological analysis of entire
system of equations

## Time line
The framework will be finished in some steps, i want to share the release plane because 
with the release of first version i will need feedback, use cases and tester.  

#### Version 0.1: first working version:
* it define [working rules](https://raw.githubusercontent.com/glaucouri/xltoy/main/rules.md)
* fully testes with py3.6 to py3.8
* collector can read data,formulas and can show an entire workbook as yaml or json.
* **diff** works with data and formulas too, it can compare 2 workbook or a representation of it yaml 
or json.
* with fingerprint option model can be marked (like a md5 for a file)

#### Version 0.2: parser feature:
* parser can understand excel formula (probably not all syntax)
* in memory graph representation with all relation between equations.
* can find all predecessors and successors of a given equation.
* models can be exported as graph or python code.
* execution of python version can be done in a notebook or a stand alone env.

#### Version 0.3: executor feature:
* data can be stored as pandas DataFrame
* models can be binded to external data. Binding feature. and can be run on huge data set.

#### Version 0.4: big data feature:
* model can be distributed on a spark cluster and executed in order to work on big data

