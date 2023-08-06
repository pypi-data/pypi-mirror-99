# treepathmap

**treepathmap** is a package for mostly navigating, tagging and make selections
of nested collections. A limited possibility of setting/replacing items within
the nested collection is also supported. This package was mainly developed for
tagging and grouping items within nested collections with mostly reading items
and replacing values at leaf level rather complete branches. For such tasks a 
different package is redeveloped, from which this package origins.

With **treepathmap** items of nested collection can be

- selected by their paths using unix filename pattern or regular expressions,
- build relations by tagging items with key-value pairs,
- define a different view of the nested collection by using additional paths,
- set value of items within nested collections using selections of these,
- and direct interaction with the nested data.

## Installation

Installing the latest release using pip is recommended.

```` shell script
    $ pip install treepathmap
````

The latest development state can be obtained from gitlab using pip.

```` shell script
    $ pip install git+https://gitlab.com/david.scheliga/treepathmap.git@dev
````

## Alpha Development Status

The current development state of this project is *alpha*. Towards the beta

- naming of modules, classes and methods will change, since the final wording is not
  done.
- Code inspections are not finished.
- The documentation is broad or incomplete.
- Testing is not complete, as it is added during the first test phase. At this
  state mostly doctests are applied at class or function level.


## Basic Usage

[Read-the-docs](https://treepathmap.readthedocs.io/en/latest/) for the basic usage.

## Contribution

Any contribution by reporting a bug or desired changes are welcomed. The preferred 
way is to create an issue on the gitlab's project page, to keep track of everything 
regarding this project.

### Contribution of Source Code
#### Code style
This project follows the recommendations of [PEP8](https://www.python.org/dev/peps/pep-0008/).
The project is using [black](https://github.com/psf/black) as the code formatter.

#### Workflow

1. Fork the project on Gitlab.
2. Commit changes to your own branch.
3. Submit a **pull request** from your fork's branch to our branch *'dev'*.

## Authors

* **David Scheliga** 
    [@gitlab](https://gitlab.com/david.scheliga)
    [@Linkedin](https://www.linkedin.com/in/david-scheliga-576984171/)
    - Initial work
    - Maintainer

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the
[LICENSE](LICENSE) file for details

## Acknowledge

[Code style: black](https://github.com/psf/black)