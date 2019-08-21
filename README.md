# BFB pyrolyzer model

This repository contains Python code for modeling a bubbling fluidized bed (BFB) biomass reactor operating at fast pyrolysis conditions. The goal of this model is to evaluate different operating conditions of the reactor and compare the results from each case.

See the [mfix-bfb-pyrolyzer](https://github.com/ccpcode/mfix-bfb-pyrolyzer) repository for a CFD example.

## Installation and usage

The BFB pyrolysis model was developed with Python 3.7 and requires the following packages:

- Chemics
- Matplotlib
- NumPy
- SciPy
- Pandas

The main entry point for the program is `__main__.py` which is located in the `bfblib` package. To execute the model, clone this repository then run the following command from within the repo:

```bash
# Run the BFB calculations for each case
python bfblib twofbr --run

# Run the BFB calculations for each case in parallel
python bfblib twofbr --mprun
```

Other command line options are demonstrated as follows:

```bash
# Cleanup files from previous runs
python bfblib twofbr --clean

# View available arguments and options
python bfblib --help
```

The model performs various calculations based on the input parameters specified in a Python module. This repo provides input parameters for the NREL 2FBR system which are available in the `twofbr` folder. The parameter files are organized by case such as case1 and case2. Each case represents a particular set of input parameters.

## Contributing

Contributions from the community are welcome. Please create a new branch then submit a Pull Request. Questions and other feedback can be submitted on the Issues page.

Below are some items that need to be reviewed or improved upon for the current state of project. These can be discussed on the Issues page before submitting a Pull Request.

- **Parameter files** - Parameter files for each case are organized by folder. Should a single file be used instead of multiple parameter files? Is the current implementation good enough?
- **Parameter file structure** - The same structure of the parameters file is used for each case. When defining a new case, the parameters file from the previous case is copied then values are edited for that new case. Is there a better approach to accomplishing this?
- **Comparing results** - Results for each case are saved as a JSON file into each case's folder. Once the case results are saved, the results are read by the Plotter class to produce Matplotlib figures. Does this approach seem reasonable? Can it be sped up with the multiprocessing module?

## License

Code in this repository is available under the MIT License - see the [LICENSE](LICENSE) file for more information.
