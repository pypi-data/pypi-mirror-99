# Wrestling

This project is for generating and tracking wrestling statistics.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Docs
Documentation live on ReadTheDocs [here](https://wrestling.readthedocs.io/en/latest/source/wrestling.html#module-wrestling)

### Installing

In order to install this project you must have a working installation of python and the pip package manager.

Install via CLI

```
pip install wrestling
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

I chose to use [pytest](https://docs.pytest.org/en/stable/) and [coverage](https://coverage.readthedocs.io/en/coverage-5.2.1/#).

Tests cover most of the functionality not covered by validators from the attrs library in addition to testing the validators themselves.

All tests w/ coverage:
```
coverage run -m pytest
```

Then to see report:
```
coverage html
```
and open htmlcov/index.html


## Built With

* [Attrs](https://www.attrs.org/en/stable/) - Classes without Boilerplate


## Versioning

I use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/nanthony007/wrestling/tags). 

## Authors

* **Nick Anthony** - *Initial work* 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
