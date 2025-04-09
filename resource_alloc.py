import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from Utils import simulate

def main(N):

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

    phis = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] # Different values of phi to test
    omegas = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0] # Different values of omega to test

    doubling_times_list = []
    cell_types_list = []
    n_list = []
    r_list = []
    s_list = []
    m_list = []

    PHIs, OMEGAs = np.meshgrid(phis, omegas) # Create a meshgrid for phi and omega
    PHIs = PHIs.flatten()
    OMEGAs = OMEGAs.flatten()

    for idx in tqdm(range(len(PHIs)), desc="phi-omega loop", total=len(PHIs)):

        params["phi"] = PHIs[idx]
        params["omega"] = OMEGAs[idx]

        # Simulate growth of N cells with the given parameters
        cells, cell_types = simulate(params, N, tqdm_flag=False) # 'cells' has shape (n_cells, n_steps, n_variables) and 'cell_types' has shape (n_cells,)
        doubling_times = []
        cell_contents = []
        for cell in cells:
            c = np.array(cell).T # growth data of the cell
            val = np.average(c[:4], weights=c[-1], axis=1) # Calculate the average values of the n, r, s, m weighted with time
            t = np.sum(c[-1]) # Total doubling time of the cell
            doubling_times.append(t)
            cell_contents.append(val)

        n, r, s, m = np.array(cell_contents).T

        doubling_times, cell_types = np.array(doubling_times), np.array(cell_types)

        doubling_times_list.append(doubling_times)
        cell_types_list.append(cell_types)
        n_list.append(n)
        r_list.append(r)
        s_list.append(s)
        m_list.append(m)

    return phis, omegas, doubling_times_list, cell_types_list, n_list, r_list, s_list, m_list

if __name__ == "__main__":
    import netCDF4 as nc
    import os
    import argparse

    parser = argparse.ArgumentParser(description="Simulate cell growth and save results to a NetCDF file.")
    parser.add_argument("--n", type=float, default=1e4, help="Number of cells to simulate.")
    parser.add_argument("--rpt", type=int, default=10, help="Number of repetitions for the simulation.")

    args = parser.parse_args()
    N = args.n
    repeats = args.rpt

    if not os.path.exists("./data/"):
        os.makedirs("./data/")

    #phi, omegas, doubling_times_list, cell_types_list, n_list, r_list, s_list, m_list = main()

    tot = []
    for rpt in tqdm(range(repeats), desc="Repeating"):
        out = main(int(N))
        tot.append(out[2:])
        if rpt == 0:
            phi, omegas = out[0], out[1]

    doubling_times_list, cell_types_list, n_list, r_list, s_list, m_list = np.concatenate(tot, axis=-1)

    ncfile = nc.Dataset("./data/resource_alloc.nc", "w", format="NETCDF4")
    ncfile.createDimension("phi-omega", len(phi)*len(omegas))
    ncfile.createDimension("phi", len(phi))
    ncfile.createDimension("omega", len(omegas))
    ncfile.createDimension("n_cells", len(doubling_times_list[0]))
    ncfile.createVariable("phi", "f8", ("phi",))[:] = phi
    ncfile.createVariable("omega", "f8", ("omega",))[:] = omegas
    ncfile.createVariable("doubling_times", "f8", ("phi-omega", "n_cells"))[:,:] = np.array(doubling_times_list)
    ncfile.createVariable("cell_types", "i4", ("phi-omega", "n_cells"))[:,:] = np.array(cell_types_list)
    ncfile.createVariable("n", "f8", ("phi-omega", "n_cells"))[:,:] = np.array(n_list)
    ncfile.createVariable("r", "f8", ("phi-omega", "n_cells"))[:,:] = np.array(r_list)
    ncfile.createVariable("s", "f8", ("phi-omega", "n_cells"))[:,:] = np.array(s_list)
    ncfile.createVariable("m", "f8", ("phi-omega", "n_cells"))[:,:] = np.array(m_list)
    ncfile.close()

    print("\nData saved successfully to resource_alloc.nc")