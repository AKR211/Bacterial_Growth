import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from Utils import simulate

# This script simulates the growth of cells under different values of phi and calculates the doubling times for different cell types.
def main():

    params = {
    "zeta": 1e-3,
    "n_0": 1.0,
    "eps": 1e-6,
    "omega": 0.5,
    "phi": 0.5,
    "kQ": 1e-9,
    "kT": 10.0,
    "s0": 10
    }

    phis = [0.1, 0.3, 0.6]
    N = int(1e6) # Number of cells to simulate

    doubling_times_list = []
    cell_types_list = []

    for idx,phi in tqdm(enumerate(phis), desc="n0 loop", total=len(phis)):

        params["phi"] = phi

        # Simulate growth of N cells with the given parameters
        cells, cell_types = simulate(params, N) # 'cells' has shape (n_cells, n_steps, n_variables) and 'cell_types' has shape (n_cells,)
        doubling_times = []
        for cell in cells:
            c = np.array(cell).T # growth data of the cell
            t = np.sum(c[-1]) # Total doubling time of the cell
            doubling_times.append(t)

        doubling_times, cell_types = np.array(doubling_times), np.array(cell_types)

        doubling_times_list.append(doubling_times)
        cell_types_list.append(cell_types)

    return phis, doubling_times_list, cell_types_list

if __name__ == "__main__":
    import netCDF4 as nc
    import os

    if not os.path.exists("./data/"):
        os.makedirs("./data/")

    phis, doubling_times_list, cell_types_list = main()

    ncfile = nc.Dataset("./data/Interdivision.nc", "w", format="NETCDF4")
    ncfile.createDimension("phi", len(phis))
    ncfile.createDimension("doubling_time", len(doubling_times_list[0]))
    ncfile.createVariable("phi", "f8", ("phi",))[:] = phis
    ncfile.createVariable("doubling_times", "f8", ("phi", "doubling_time"))[:,:] = np.array(doubling_times_list)
    ncfile.createVariable("cell_types", "i4", ("phi", "doubling_time"))[:,:] = np.array(cell_types_list)
    ncfile.close()

    print("Data saved successfully to Interdivision.nc")