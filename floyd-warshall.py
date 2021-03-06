import numpy as np
from math import sqrt
import time
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image



GRID_LENGTH = 20
EXTENT_THRESHOLD = 20

start_time = time.time()
np.random.seed(123)

# Create grids.
source_grid = np.full([GRID_LENGTH+2,GRID_LENGTH+2], np.inf)
source_grid[1,1:1+GRID_LENGTH] = [1]*GRID_LENGTH
source_grid[20,1:1+GRID_LENGTH] = [1]*GRID_LENGTH
# source_grid[1:1+GRID_LENGTH,1:1+GRID_LENGTH] = np.random.randint(low=0, high=2, size=(GRID_LENGTH,GRID_LENGTH))
# source_grid[1:1+GRID_LENGTH,1:1+GRID_LENGTH] = np.array([[1,1,1,1,1,1,1,1,1,1],[0,1,0,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])

cost_grid = np.full([GRID_LENGTH+2,GRID_LENGTH+2], np.inf)
cost_grid[1:1+GRID_LENGTH,1:1+GRID_LENGTH] = np.random.randint(low=1, high=8, size=(GRID_LENGTH,GRID_LENGTH))
cost_grid[7:14,7:14] = np.full([7,7], 7)
# img = Image.open('N04E006_FABDEM_V1-0.tif')
# cost_grid = np.array(img)
# cost_grid[100:100+GRID_LENGTH, 100:100+GRID_LENGTH]

costdist_grid = np.full([GRID_LENGTH+2,GRID_LENGTH+2], np.inf)
costdist_grid[source_grid==1] = 0


def calc_neighbor(cost1, cost2):
    return 0.5*cost1 + 0.5*cost2

def calc_neighbor_diagonal(cost1,cost2):
    return 0.5*sqrt(2)*cost1 + 0.5*sqrt(2)*cost2

def body(cost_grid, costdist_grid, row_i, col_i):
    l = []
    current_costdist = costdist_grid[row_i, col_i]
    current_cost = cost_grid[row_i, col_i]
    new_costdist = np.full([GRID_LENGTH+2,GRID_LENGTH+2],np.inf)
    
    if current_cost == 0:
        pass
    
    costdist_surrounding = []
    # if current_costdist == np.inf:
    for row_offset in [-1,0,+1]:
        for col_offset in [-1,0,+1]:
            costdist = costdist_grid[row_i+row_offset, col_i+col_offset]
            costdist_surrounding.append(costdist)
            cost = cost_grid[row_i+row_offset, col_i+col_offset]
            if costdist != np.inf:
                if row_offset != 0 and col_offset != 0:
                    l.append(min(costdist_surrounding)+ calc_neighbor_diagonal(current_cost, cost))
                else:
                    l.append(min(costdist_surrounding) + calc_neighbor(current_cost, cost))
        
    l.append(current_costdist)
    new_costdist[row_i, col_i] = np.round(np.nanmin(l),1)
    return new_costdist

def plot_progress(source_grid, cost_grid, costdist_grid, title="test.png"):
    source_grid = source_grid[1:GRID_LENGTH+1,1:GRID_LENGTH+1]
    cost_grid = cost_grid[1:GRID_LENGTH+1,1:GRID_LENGTH+1]
    costdist_grid = costdist_grid[1:GRID_LENGTH+1,1:GRID_LENGTH+1]
    
    fig1, (ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=3, sharex = True, sharey = True, figsize=(20,20))
    cm = LinearSegmentedColormap.from_list("sources", [(255,255,100),(0,102,255)], N=2) 
    # ax1.imshow(source_grid, aspect='equal', cmap=cm)
    im2 = ax2.imshow(cost_grid, aspect='equal', cmap="Reds")
    im3 = ax3.imshow(costdist_grid, aspect='equal', cmap="Blues")
    extend_grid = np.ones((GRID_LENGTH,GRID_LENGTH))
    extend_grid[costdist_grid>EXTENT_THRESHOLD] = 0
    ax4.imshow(extend_grid, aspect='equal', cmap="Blues")
    
    # for (j,i),label in np.ndenumerate(cost_grid):
    #     ax2.text(i,j,label,ha='center',va='center', fontsize=4)
    # for (j,i),label in np.ndenumerate(costdist_grid):
    #     ax3.text(i,j,label,ha='center',va='center', fontsize=4)
    
    # fig1.colorbar(im2, ax=ax2, orientation="horizontal")
    # fig1.colorbar(im3, ax=ax3, orientation="horizontal")
    
    plt.subplots_adjust(wspace=0.2)

    # ax1.set_title("Sources")
    ax2.set_title("Costs")
    ax3.set_title("Cost distances")
    ax4.set_title("Flood extend")
        
    for ax in [ax2,ax3,ax4]:
        ax.axis('off')
        
    plt.savefig(f"images/{title}.png", dpi=300, bbox_inches="tight")
    
# Calculate the algorithm
for i in range(GRID_LENGTH*GRID_LENGTH):
    print(i)
    new_values = [costdist_grid]

    # calc cost dist for each pixel
    for row_i in np.arange(1,GRID_LENGTH+1,1):
        for col_i in np.arange(1,GRID_LENGTH+1,1):
            new_values.append(body(cost_grid, costdist_grid, row_i, col_i))
    
    # merge new cost distances to one array
    costdist_grid = np.amin(np.array(new_values), axis=0)

    # Plot single steps of path finding.
    plot_progress(source_grid, cost_grid, costdist_grid, f"{str(i+1).zfill(3)}") 

print("run time: ", np.round(time.time()-start_time,2), "sec")