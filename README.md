# Fair-check

Fair-check is a simple script to check [FAIR principles](https://www.go-fair.org/fair-principles/) compliance.

It uses FAIR Evaluator, a service which, using a [SmartAPI](http://w3id.org/FAIR_Evaluator) annotation, can retrieve
information to check whether a resource complies with certain FAIR Maturity Indicator Test.

Unfortunately, currently, only Gen2 Maturity Indicators can be automatically tested, Gen1 MIs should be
checked by humans.  In any case, we can still verify a lot of MIs. Take a look at: https://fairdata.services:7171/FAIR_Evaluator/metrics

## Resources and interfaces

A **resource** is any element that can be accessed through an uri. For example, this repository is a resource
(and can be accessed with the uri https://github.com/jorgechp/fair-check).

An **interface** is the uri of a service that is used to test a Maturity Indicator. For 
example, https://w3id.org/FAIR_Tests/tests/gen2_unique_identifier.

You can find a complete list of FAIR Evaluator endpoints at https://fairdata.services:7171/FAIR_Evaluator/metrics


## Requirements

Fair-check needs Python 3.10 or higher to be executed. In addition, all the packages listed at
requirements.txt should be installed. The fastest way to do that is executing the following command:

     pip install -r /path/to/requirements.txt

If you're using Conda, then you can also execute the following command:

    conda install --yes --file requirements.txt

And that's all. Fair-check is properly installed.

## How does Fair-check work?

The basic behaviour of Fair-check is to call the script from python with the following command syntax:

    python faircheck.py <resources> <tests>

For example:

    python faircheck.py 10.5281/zenodo.7911779 https://w3id.org/FAIR_Tests/tests/gen2_unique_identifier


    Executing tests
    Generating output file
     Testing resource: 'https://10.5281/zenodo.7911779'
         Test: 'https://w3id.org/FAIR_Tests/tests/gen2_unique_identifier'
             SUCCESS: "INFO: TEST VERSION 'Hvst-1.4.4:Tst-0.2.2'\n\nSUCCESS: Found an identifier of type 'uri'"
         Passed: 1/1 
    Done

You can also use a list of resources or a list of interfaces as input (using commas as separator):

    python faircheck.py https://10.5281/zenodo.7911779,https://doi.org/10.1007/s11192-023-04720-7 https://w3id.org/FAIR_Tests/tests/gen2_unique_identifier,https://w3id.org/FAIR_Tests/tests/gen2_metadata_identifier_persistence

    
    Executing tests
    Generating output file
     Testing resource: 'https://10.5281/zenodo.7911779'
         Test: 'https://w3id.org/FAIR_Tests/tests/gen2_metadata_identifier_persistence'
             FAILED!: "INFO: TEST VERSION 'Hvst-1.4.4:Tst-0.2.3'\n\nINFO: END OF HARVESTING\n\nINFO: The metadata GUID appears to be a URL.  Testing known URL persistence schemas (purl, oclc, fdlp, purlz, w3id, ark, doi(as URL)).\n\nFAILURE: The metadata GUID does not conform with any known permanent-URL system."
         Test: 'https://w3id.org/FAIR_Tests/tests/gen2_unique_identifier'
             SUCCESS: "INFO: TEST VERSION 'Hvst-1.4.4:Tst-0.2.2'\n\nSUCCESS: Found an identifier of type 'uri'"
         Passed: 1/2 

     Testing resource: 'https://doi.org/10.1007/s11192-023-04720-7'
         Test: 'https://w3id.org/FAIR_Tests/tests/gen2_metadata_identifier_persistence'
             SUCCESS: "INFO: TEST VERSION 'Hvst-1.4.4:Tst-0.2.3'\n\nINFO: END OF HARVESTING\n\nINFO: The metadata GUID appears to be a URL.  Testing known URL persistence schemas (purl, oclc, fdlp, purlz, w3id, ark, doi(as URL)).\n\nSUCCESS: The metadata GUID conforms with doi.org, which is known to be persistent."
         Test: 'https://w3id.org/FAIR_Tests/tests/gen2_unique_identifier'
             SUCCESS: "INFO: TEST VERSION 'Hvst-1.4.4:Tst-0.2.2'\n\nSUCCESS: Found an identifier of type 'uri'"
         Passed: 2/2 
    Done


But you can also use different parameters:

- -h / --help -> Show help.
- -e / --export EXPORT -> Specify a path to export te results as a csv file.
- -nv / --no_verbosity -> Don't display the test results on the default output.
- -r / --resources -> Path to a resource file.
- -t / --tests -> Path to a test file.

Remember that if no interfaces are provided, Fair-check will use all the interfaces listed on
config/tests file.

## Resources and test files

You can save all the tests and resources into files. The resources file requires to input
one resource per line. 

For tests files, you can put one endpoint per line or using the following line format:

    <Name of the Maturity Indicator>,<interface>

### 



