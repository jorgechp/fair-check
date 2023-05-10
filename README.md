# Fair-check

Fair-check is a simple script to check [FAIR principles](https://www.go-fair.org/fair-principles/) compliance.

It uses FAIR Evaluator, a service which, using a [SmartAPI](http://w3id.org/FAIR_Evaluator) annotation, can retrieve
information to check whether a resource complies with certain FAIR Maturity Indicator Test.

Unfortunately, currently, only Gen2 Maturity Indicators can be automatically tested, Gen1 MIs should be
checked by humans.  In any case, we can still verify a lot of MIs. Take a look at: https://fairdata.services:7171/FAIR_Evaluator/metrics


## Requirements

Fair-check needs Python 3.10 or higher to be executed. In addition, all the packages listed at
requirements.txt should be installed. The fastest way to do that is executing the following command:

     pip install -r /path/to/requirements.txt

If you're using Conda, then you can also execute the following command:

    conda install --yes --file requirements.txt

And that's all. Fair-check is properly installed.

## How does Fair-check work?

The basic behaviour of Fair-check is to call the script from python with the following command sintax:

    python faircheck.py <resources> <tests>

For example:

    python faircheck.py 10.5281/zenodo.7911779 https://w3id.org/FAIR_Tests/tests/gen2_unique_identifier

But you can also use different parameters:

- -h / --help -> Show help.
- -e / --export EXPORT -> Specify a path to export te results as a csv file.
- -nv / --no_verbosity -> Don't display the test results on the default output.
- -r / --resources -> Path to a resource file.
- -t / --tests -> Path to a test file.

## Examples





