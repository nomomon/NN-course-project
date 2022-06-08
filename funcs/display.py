from turtle import color
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

from .distance import *
from .convert import *

def str_int(n):
    return int(n) if int(n) == n else n

def display_molecule_video(row, angle=10, atom_index=False, bond_type=True, equal_aspect_ratio=False):
    fig = plt.figure()
    fig.set_size_inches(12, 8)

    ax = plt.axes(projection='3d')
    if equal_aspect_ratio:
        p = row.positions
        p_max = p.max()
        p_min = p.min()

        ax.set_xlim([p_min, p_max])
        ax.set_ylim([p_min, p_max])
        ax.set_zlim([p_min, p_max])
    # ax.grid(False)
    
    def init():
        p = row.positions
        s = row.symbols
        n = row.numbers
        
        x = p[:, 0]
        y = p[:, 1]
        z = p[:, 2]

        ax.scatter(x, y, z, 
            s = n*20,        # size
            c = n,           # color
            cmap = 'inferno'
        )

        dist_mat = get_distance_matrix(row)
        bond_matrix = get_bond_type_matrix(dist_mat, row.symbols)

        for i in range(len(p)):
            ax.text(x[i], y[i], z[i], f" {s[i]} {str(i) if atom_index else ''}")

        for i in range(len(p)):
            for j in range(i+1, len(p)):
                if bond_matrix[i][j] != 0:
                    lx = np.array([x[i], x[j]])
                    ly = np.array([y[i], y[j]])        
                    lz = np.array([z[i], z[j]])

                    ax.plot(lx, ly, lz, color='black')
                    if bond_type:
                        ax.text(lx.mean(), ly.mean(), lz.mean(), str_int(bond_matrix[i][j]))
        return fig,


    def animate(i):
        ax.view_init(elev=angle, azim=i)
        return fig,

    
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=360, interval=30, blit=True)
    
    plt.close()
    return HTML(anim.to_html5_video())

# %matplotlib notebook
def display_molecule(row, atom_index=False, bond_type=True, equal_aspect_ratio=False):
    p = row.positions
    s = row.symbols
    n = row.numbers

    ax = plt.axes(projection='3d')
    fig = plt.figure()
    fig.set_size_inches(12, 8)

    if equal_aspect_ratio:
        p_max = p.max()
        p_min = p.min()

        ax.set_xlim([p_min, p_max])
        ax.set_ylim([p_min, p_max])
        ax.set_zlim([p_min, p_max])
    
    x = p[:, 0]
    y = p[:, 1]
    z = p[:, 2]

    ax.scatter(x, y, z, 
        s = n*20,        # size
        c = n,           # color
        cmap = 'inferno'
    )

    dist_mat = get_distance_matrix(row)
    bond_matrix = get_bond_type_matrix(dist_mat, row.symbols)

    for i in range(len(p)):
        ax.text(x[i], y[i], z[i], f" {s[i]} {str(i) if atom_index else ''}")

    for i in range(len(p)):
        for j in range(i+1, len(p)):
            if bond_matrix[i][j] != 0:
                lx = np.array([x[i], x[j]])
                ly = np.array([y[i], y[j]])        
                lz = np.array([z[i], z[j]])

                ax.plot(lx, ly, lz, color='black')
                if bond_type:
                    ax.text(lx.mean(), ly.mean(), lz.mean(), str_int(bond_matrix[i][j]), color='r')
    return fig