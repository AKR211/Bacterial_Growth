from Cell import Cell
from tqdm import tqdm

# Update the cell's content, type and time step based on the given parameters and divide the cell if appropriate
def division(params, c):

    out = []
    type = c.get_type()

    while True:
        c.update_type()
        dt = c.update(params)
        out.append(c.get_content()+[dt])
        type = c.get_type()

        if c.split(params):
            c_new = c.divide()
            break

    return out, type, c_new


# Simulate the cell division process using Lineage Growth for N iterations and return the results and types of cells
def simulate(params, N):
    c_old = Cell(10, 10, 10, 10)

    out = []
    types = []

    for i in tqdm(range(N), desc="Simulation", total=N):
        out_div, type, c_new = division(params, c_old)
        if i>1000:
            out.append(out_div)
            types.append(type)
        c_old = c_new

    return out, types