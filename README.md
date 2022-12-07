# TypoSquash

A tool to detect potential typosquatting packages based on static and dynamic analysis.

> Currently supports NPM, PyPI and RubyGems packages.

## Components

The tool consists of 3 modules:
1. Module 1 - Candidate Name Generator
2. Module 2 - Static Evaluator
3. Module 3 - Dynamic Analyzer

## Module 1 - Candidate Name Generator
This module is responsible for generating potential typosquatting candidates for a package.

### Usage

Compile by running

```
go build -o typogenerator cmd/typogen/main.go
```

```
Usage of ./typogenerator:
  -j=false: Display JSON output
  -r="pypi": Defines the package registry to search in (rubygems, pypi, npm)
  -s="zenithar": Defines package to alternate
  -v=false: Perform validation for generated candidates
```

Example

```
./typogenerator -s through2 -r npm -j -v
```

## Module 2 - Static Evaluator
This module is responsible for evaluating and scoring a package based on reputational factors such as author age, author GitHub activity, package popularity etc.


## Module 3 - Dynamic Analyzer
This module is responsible for evaluating a package dynamically based on the files accessed, sockets created and DNS queries made. It creates baselines from the original valid package and looks for deviations by comparing the output of the typosquatting candidate package with the original package.

### Usage

> Note: Run as `sudo`.

```
usage: module-3.py [-h] [-p [P]] [-t [T]] [-r [R]]

options:
  -h, --help  show this help message and exit
  -p [P]      original package name
  -t [T]      typosquatting package name
  -r [R]      registry name
```

Example

```
sudo python3 module-3.py -p python-dateutil -t python-dateuti -r pypi
```


## Credits

- Module 1 was adapted from [typogenerator][1].

- Module 3 was adapted from [package-analysis][2].

[1]: https://github.com/zntrio/typogenerator
[2]: https://github.com/ossf/package-analysis
