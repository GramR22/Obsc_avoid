import numpy as np
import car as obj
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

grid = np.zeros((30, 30), dtype=int)
grid[10, 5:25] = 1
grid[5:20, 15] = 1
grid[25:28, 25:28] = 1
car = obj.car(0,0)


def visualize(true_grid, mapped_grid, car_position=None):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Define custom colormap: -1 = black (unknown), 0 = white (empty), 1 = red (obstacle)
    cmap = ListedColormap(['black', 'white', 'red'])

    # Plot 1: True grid
    axes[0].imshow(true_grid, cmap=cmap, vmin=-1, vmax=1)
    axes[0].set_title("True Grid")
    if car_position:
        axes[0].scatter(car_position[0], car_position[1], color='green', s=50)

    # Plot 2: Mapped Grid (need to offset -1 → 0 for colormap indexing)
    mapped_display = mapped_grid + 1
    axes[1].imshow(mapped_display, cmap=cmap, vmin=0, vmax=2)
    axes[1].set_title("Mapped Grid")
    if car_position:
        axes[1].scatter(car_position[0], car_position[1], color='green', s=50)

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.show()

visualize(grid,car.mapped_Grid)