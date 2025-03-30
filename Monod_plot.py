import matplotlib.pyplot as plt

# This script generates plots from the data saved in Monod.py.
# It visualizes the relationship between initial cell density (n0), growth rate (GR), ribosome content (r), and cell size (s) for different initial cell densities.
# The first plot shows the relationship between n0 and GR, while the second plot shows the relationship between GR and ribosome content/cell size.
def plot(n0s, GRs, ribs, cell_sizes):
    plt.scatter(n0s, GRs, marker='o', alpha=0.5, color='magenta', edgecolor='black')
    plt.xlabel(r'$n_0$', fontsize=12, labelpad=10)
    plt.ylabel(r'GR', fontsize=12, labelpad=10)
    plt.tight_layout()
    plt.grid(alpha=0.5)
    plt.savefig("./figures/GR_vs_n0.png", dpi=300)
    plt.close()

    plt.scatter(GRs, ribs, marker='o', alpha=0.5, color='blue', edgecolor='black', label='r')
    plt.scatter(GRs, cell_sizes, marker='o', alpha=0.5, color='red', edgecolor='black', label='cell size')
    plt.yscale('log')
    plt.xlabel(r'$GR$', fontsize=12, labelpad=10)
    plt.ylabel('Mean content number per cell', fontsize=12, labelpad=10)
    plt.tight_layout()
    plt.grid(alpha=0.5)
    plt.legend()
    plt.savefig("./figures/GR_vs_ribs_cell_sizes.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    import os
    import netCDF4 as nc

    if not os.path.exists("./figures/"):
        os.makedirs("./figures/")

    ncfile = nc.Dataset("./data/Monod.nc", "r")
    n0s = ncfile.variables["n0"][:]
    GRs = ncfile.variables["GR"][:]
    ribs = ncfile.variables["ribs"][:]
    cell_sizes = ncfile.variables["cell_sizes"][:]
    ncfile.close()
    print("Data loaded successfully from Monod.nc")

    plot(n0s, GRs, ribs, cell_sizes)

    print("Plots saved successfully.")
