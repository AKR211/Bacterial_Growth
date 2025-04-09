import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma

def plot1(phis, omegas, n_list, r_list, m_list, doubling_times_list):

    m = np.array(m_list).mean(axis=1).reshape(len(omegas), len(phis)).T
    n = np.array(n_list).mean(axis=1).reshape(len(omegas), len(phis)).T
    r = np.array(r_list).mean(axis=1).reshape(len(omegas), len(phis)).T
    gr = np.array(np.log(2)/doubling_times_list).mean(axis=1).reshape(len(omegas), len(phis)).T

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(m, aspect='auto', cmap='viridis')
    plt.colorbar()

    plt.xticks(ticks=np.arange(len(omegas)), labels=omegas, rotation=45)
    plt.yticks(ticks=np.arange(len(phis)), labels=phis)
    plt.xlabel(r'$\phi$', fontsize=14)
    plt.ylabel(r'$\omega$', fontsize=14)
    plt.title('m', fontsize=20)

    plt.subplot(2, 2, 2)

    plt.imshow(r, aspect='auto', cmap='viridis')
    plt.colorbar()

    plt.xticks(ticks=np.arange(len(omegas)), labels=omegas, rotation=45)
    plt.yticks(ticks=np.arange(len(phis)), labels=phis)
    plt.xlabel(r'$\phi$', fontsize=14)
    plt.ylabel(r'$\omega$', fontsize=14)
    plt.title('r', fontsize=20)

    plt.subplot(2, 2, 3)

    plt.imshow(n, aspect='auto', cmap='viridis')
    plt.colorbar()

    plt.xticks(ticks=np.arange(len(omegas)), labels=omegas, rotation=45)
    plt.yticks(ticks=np.arange(len(phis)), labels=phis)
    plt.xlabel(r'$\phi$', fontsize=14)
    plt.ylabel(r'$\omega$', fontsize=14)
    plt.title('n', fontsize=20)

    plt.subplot(2, 2, 4)

    plt.imshow(gr, aspect='auto', cmap='inferno')
    plt.colorbar()

    plt.xticks(ticks=np.arange(len(omegas)), labels=omegas, rotation=45)
    plt.yticks(ticks=np.arange(len(phis)), labels=phis)
    plt.xlabel(r'$\phi$', fontsize=14)
    plt.ylabel(r'$\omega$', fontsize=14)
    plt.title('Growth Rate', fontsize=20)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig("./figures/resource_alloc.png", dpi=300)
    plt.close()

def plot2(phis, omegas, cell_types):
    
    cell_types = np.transpose(np.array(cell_types).reshape(len(omegas), len(phis), cell_types.shape[1]), (1, 0, 2))

    plt.figure(figsize=(15, 5))

    for i in range(1,4):

        cells = ma.array(cell_types)
        total = cells.count(axis=2)
        cells.mask = cells != i
        count = cells.count(axis=2)

        fraction = count / total
        plt.subplot(1, 3, i)

        plt.imshow(fraction, aspect='auto', cmap='winter', norm='log', vmin = 1e-9, vmax=1)
        plt.colorbar()

        plt.xticks(ticks=np.arange(len(omegas)), labels=omegas, rotation=45)
        plt.yticks(ticks=np.arange(len(phis)), labels=phis)
        plt.xlabel(r'$\phi$', fontsize=14)
        plt.ylabel(r'$\omega$', fontsize=14)

        plt.title(f'Fraction of cell type {i}', fontsize=20)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig("./figures/resource_alloc_cell_types.png", dpi=300)
    plt.close()

        


if __name__ == "__main__":
    import os
    import netCDF4 as nc

    if not os.path.exists("./figures/"):    
        os.makedirs("./figures/")

    ncfile = nc.Dataset("./data/resource_alloc.nc", "r")
    n_list = ncfile.variables["n"][:,:]
    r_list = ncfile.variables["r"][:,:]
    m_list = ncfile.variables["m"][:,:]
    phis = ncfile.variables["phi"][:]
    omegas = ncfile.variables["omega"][:]
    doubling_times_list = ncfile.variables["doubling_times"][:,:]
    cell_types = ncfile.variables["cell_types"][:,:]
    ncfile.close()

    plot1(phis, omegas, n_list, r_list, m_list, doubling_times_list)
    plot2(phis, omegas, cell_types)