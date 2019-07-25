# BFB pyrolyzer model

This repository contains Python code for modeling a bubbling fluidized bed (BFB) biomass reactor operating at fast pyrolysis conditions. The model can be applied to other BFB pyrolyzer reactors given the appropriate parameters and reaction mechanisms. See the [mfix-bfb-pyrolyzer](https://github.com/ccpcode/mfix-bfb-pyrolyzer) repository for a CFD example.

## Installation and usage

The BFB pyrolysis model was developed with Python 3.7 and the Chemics Python package. To ensure proper execution, the Anaconda Python distribution is recommended for all platforms.

- [Anaconda](https://www.anaconda.com/distribution/)
- [Chemics](https://chemics.github.io)

Command line options for running the model are shown below.

```bash
# Run the BFB calculations for each case
python main.py twofbr --run

# Cleanup files from previous runs
python main.py twofbr --clean

# View available arguments and options
python main.py --help
```

## Contributing

Contributions from the community are welcome. Please create a new branch then submit a Pull Request. Questions and other feedback can be submitted on the Issues page. Below are some items that need to be reviewed or added to the model:

- **Run model for multiple cases**. Currently, each case is represented by a single parameters file (Python module) and must be run individually. An approach to run all the parameter files is needed along with comparing the results from each case.
- **Parameters and Results**. Review current approach for handling parameters and associated results.
- **Classes**. Review the use of class objects and whether the current approach is reasonable.

## License

Code in this repository is available under the MIT License - see the [LICENSE](LICENSE) file for more information.
