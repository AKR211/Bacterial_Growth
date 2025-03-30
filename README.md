# Bacterial Growth

This repository contains a complete Python implementation of the model described in the paper:

**Simple bacterial growth model for the formation of spontaneous and triggered dormant subpopulations**  
*Mikkel Skjoldan Svenningsen and Namiko Mitarai, Physical Review Research 6, 033072 (2024)*  
DOI: [10.1103/PhysRevResearch.6.033072](https://doi.org/10.1103/PhysRevResearch.6.033072)

## Purpose of this repo

The implementation is entirely in done in Python and is designed to reproduce results (currently Mean behavior and Distributions of division times) of the referenced paper.

## Repository Structure

- **`Cell.py`**: Contains the main class for simulating the growth of a single bacterium.
- **`Utils.py`**: Contains utility functions for the simulation.
- **`Monod.py`**: Generate data for mean behaviour analysis
- **`Monod_plot.py`**: Generate plots for mean behaviour analysis
- **`Interdivision.py`**: Generate data for Distribution of Division times analysis
- **`Interdivision_plot.py`**: Generate plots for Distribution of Division times analysis
- **`README.md`**: This file.

## Requirements

- Python 3.7 or higher
- NumPy
- Matplotlib
- netCDF4
- tqdm


