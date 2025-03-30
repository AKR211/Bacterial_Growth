import matplotlib.pyplot as plt
import numpy as np

# This function splits the doubling times into different cell types based on the provided cell type labels.
def split_cell_types(doubling_times_list, cell_types):

    normals = []
    m_dorms = []
    r_dorms = []
    mr_dorms = []

    for i in range(len(doubling_times_list)):
        normal = doubling_times_list[i][cell_types[i] == 0]
        m_dorm = doubling_times_list[i][cell_types[i] == 1]
        r_dorm = doubling_times_list[i][cell_types[i] == 2]
        mr_dorm = doubling_times_list[i][cell_types[i] == 3]

        normals.append(normal)
        m_dorms.append(m_dorm)
        r_dorms.append(r_dorm)
        mr_dorms.append(mr_dorm)

    return normals, m_dorms, r_dorms, mr_dorms


# This script generates plots from the data saved in Interdivision.py.
# It visualizes the distribution of doubling times for different cell types (normal, m-Dormant, r-Dormant, mr-Dormant) under different values of phi.
def plot(phis, doubling_times_list, normals, m_dorms, r_dorms, mr_dorms):

    plt.figure(figsize=(10, 3))

    for idx,phi in enumerate(phis):

        plt.subplot(1, 3, idx + 1)
       
        normal = np.array(normals[idx])
        m_dorm = np.array(m_dorms[idx])
        r_dorm = np.array(r_dorms[idx])
        mr_dorm = np.array(mr_dorms[idx])
        doubling_times = np.array(doubling_times_list[idx])
        
        # Calculate the histogram of doubling times for each cell type
        # Use logarithmic bins for better visualization of the distribution
        bins = np.logspace(np.log10(np.min(doubling_times)), np.log10(np.max(doubling_times)), 50)
       
        hist_normal, _ = np.histogram(normal, bins=bins)
        hist_m_dorm, _ = np.histogram(m_dorm, bins=bins)
        hist_r_dorm, _ = np.histogram(r_dorm, bins=bins)
        hist_mr_dorm, _ = np.histogram(mr_dorm, bins=bins)
       
        # Normalize the histograms
        X = np.sqrt(bins[:-1] * bins[1:])
        norm = np.sum(hist_normal * X) + np.sum(hist_m_dorm * X) + np.sum(hist_r_dorm * X) + np.sum(hist_mr_dorm * X)
       
        normal_norm = hist_normal / norm
        m_dorm_norm = hist_m_dorm / norm
        r_dorm_norm = hist_r_dorm / norm
        mr_dorm_norm = hist_mr_dorm / norm
       
        plt.subplot(1, 3, idx + 1)
        plt.title(f"$\\phi={phi}$")
       
        # Plot the normalized histograms
        plt.bar(X, normal_norm, width=np.diff(bins), alpha=0.4, color='blue', label='Normal')
        plt.bar(X, m_dorm_norm, width=np.diff(bins), alpha=0.4, color='orange', label='m-Dormant')
        plt.bar(X, r_dorm_norm, width=np.diff(bins), alpha=0.4, color='green', label='r-Dormant')
        plt.bar(X, mr_dorm_norm, width=np.diff(bins), alpha=0.4, color='red', label='mr-Dormant')

        # Add a line to indicate the maximum of the distributions
        outline = np.max([normal_norm, m_dorm_norm, r_dorm_norm, mr_dorm_norm], axis=0)
        plt.plot(X, np.convolve(outline, [0.15,0.7,0.15], mode='same'), color='black', linewidth=1)
    
        plt.xscale('log')
        plt.yscale('log')

        plt.xlabel("Doubling time")
        plt.ylabel("Frequency")
        plt.legend(fontsize=5)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.savefig("./figures/Interdivision.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    import os
    import netCDF4 as nc

    if not os.path.exists("./figures/"):
        os.makedirs("./figures/")

    ncfile = nc.Dataset("./data/Interdivision.nc", "r")
    phis = ncfile.variables["phi"][:]
    doubling_times_list = ncfile.variables["doubling_times"][:,:]
    cell_types_list = ncfile.variables["cell_types"][:,:]
    ncfile.close()

    print("Data loaded successfully from Interdivision.nc")

    normals, m_dorms, r_dorms, mr_dorms = split_cell_types(doubling_times_list, cell_types_list)

    plot(phis, doubling_times_list, normals, m_dorms, r_dorms, mr_dorms)

    print("Plots saved successfully.")