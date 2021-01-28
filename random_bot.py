import numpy as np
from vxa_generator import vxa_from_array
from scipy.ndimage.measurements import label


WORKSPACE_LENGTH = 6


def make_one_shape_only(output_state):
    """Find the largest continuous arrangement of True elements after applying boolean mask.
    
    Avoids multiple disconnected softbots in simulation counted as a single individual.
    
    Parameters
    ----------
    output_state : numpy.ndarray
        Network output
        
    Returns
    -------
    part_of_ind : bool
        True if component of individual
    """
    if np.sum(output_state) == 0:
        return output_state
        
    # find coordinates
    array = output_state > 0
    labeled, ncomponents = label(array)
    
    largest_count = 0
    largest_label = 0
    for n in range(ncomponents+1):
        this_count = np.sum(labeled == n)
        vox_count = np.sum(array[labeled == n])
        if (this_count > largest_count) and (vox_count > 0):
            largest_label = n
            largest_count = this_count
            
    return labeled == largest_label


random_noise = np.random.randint(2, size=(WORKSPACE_LENGTH,)*3)
mask = make_one_shape_only(random_noise)
body = np.zeros_like(random_noise)
body[mask] = 1
vxa_from_array(body, save_filename='random_bot.vxa')
