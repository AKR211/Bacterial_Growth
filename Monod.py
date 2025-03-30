import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from Utils import simulate

# This script simulates the growth of cells with different initial cell densities (n0s) and calculates the growth rate (GR), ribosome content (r), and cell size (s) for each density.
def main():

    params = {
    "zeta": 1e-3,
    "n_0": 1,
    "eps": 1e-6,
    "omega": 1.0,
    "phi": 0.5,
    "kQ": 1e-9,
    "kT": 10,
    "s0": 10
    }

    n0s = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0]
    GRs = []
    ribs = []
    cell_sizes = []
    for n0 in tqdm(n0s, desc="n0 loop", total=len(n0s)):

        params["n_0"] = n0

        # Simulate growth of 2000 cells with the given parameters
        cells, cell_types = simulate(params, 2000) # 'cells' has shape (n_cells, n_steps, n_variables) and 'cell_types' has shape (n_cells,)
        vals = []
        for cell in cells:
            c = np.array(cell).T # growth data of the cell
            val = np.average(c[:4], weights=c[-1], axis=1) # Calculate the average values of the n, r, s, m weighted with time
            t = np.sum(c[-1]) # Total doubling time of the cell
            vals.append(val.tolist()+[np.log(2)/t]) # Calculate the growth rate (GR) as the logarithm of 2 divided by the total time

        n, r, s, m, gr = np.average(np.array(vals).T, axis=1) # Calculate the average values of n, r, s, m and gr across all cells

        GRs.append(gr)
        ribs.append(r)
        cell_sizes.append(r+s+m)

    return n0s, GRs, ribs, cell_sizes

if __name__ == "__main__":
    import netCDF4 as nc
    import os

    n0s, GRs, ribs, cell_sizes = main()

    if not os.path.exists("./data/"):
        os.makedirs("./data/")

    ncfile = nc.Dataset("./data/Monod.nc", "w", format="NETCDF4")
    ncfile.createDimension("n0", len(n0s))
    ncfile.createVariable("n0", "f8", ("n0",))[:] = n0s
    ncfile.createVariable("GR", "f8", ("n0",))[:] = GRs
    ncfile.createVariable("ribs", "f8", ("n0",))[:] = ribs
    ncfile.createVariable("cell_sizes", "f8", ("n0",))[:] = cell_sizes
    ncfile.close()
    print("Data saved successfully to Monod.nc")
