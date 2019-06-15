# BFB pyrolyzer model

This repository contains Python code for modeling a bubbling fluidized bed (BFB) biomass reactor operating at fast pyrolysis conditions. The model can be applied to other BFB pyrolyzer reactors given the appropriate parameters and reaction mechanisms. See the [mfix-bfb-pyrolyzer](https://github.com/ccpcode/mfix-bfb-pyrolyzer) repository for a CFD example.

## Installation and usage

The BFB pyrolysis model was developed with Python 3.7 and the Chemics Python package. To ensure proper execution, the Anaconda Python distribution is recommended for all platforms.

- [Anaconda](https://www.anaconda.com/distribution/)
- [Chemics](https://chemics.github.io)

Command line options for running the model are shown below.

```bash
# Run the model with a specified parameters file
python main.py twofbr/params.py -p

# Run specified parameters file and save results and figures
python main.py twofbr/params.py -pf

# Run the model for a range of temperatures
# Temperature range is specified in `case` within parameters file
python main.py twofbr/params.py -t

# Cleanup the project folder to remove results and figures
python main.py twofbr/params.p -c
```

## Contributing

Contributions from the community are welcome. Please create a new branch then submit a Pull Request. Questions and other feedback can be submitted on the Issues page.

## License

Code in this repository is available under the MIT License - see the [LICENSE](LICENSE) file for more information.
