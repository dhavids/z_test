class IndexSlicableList(list):
    """List subclass that supports slicing with a list of indices."""

    def __getitem__(self, index):
        """Custom indexing behavior for the list."""

        # If index is a list of integers, treat it as a list of indices to slice.
        if isinstance(index, list) and all(isinstance(i, int) for i in index):
            return IndexSlicableList([self[i] for i in index])
        
        # If index is an integer, use the default list behavior.
        elif isinstance(index, int):
            return super().__getitem__(index)

        # Handle slice objects as normal list slicing.
        elif isinstance(index, slice):
            return super().__getitem__(index)

        else:
            raise TypeError("Index must be int, slice, or list of ints")


my_list = IndexSlicableList([10, 20, 30, 40, 50])

# Slicing with a list of indices
result = my_list[[1, -1, 4]]  
print(result)  # Output: [20, 40, 50] (New IndexSlicableList)

# Standard indexing
result = my_list[2]  
print(result)  # Output: 30

# Normal slicing
result = my_list[1:4]  
print(result)  # Output: [20, 30, 40] (New IndexSlicableList)

import numpy as np  # For handling indices in a numpy-like way

class SliceableList(list):
    def __getitem__(self, index):
        if isinstance(index, list):
            # Handle slicing with a list of indices
            indices = np.array(index)  # Convert to NumPy array for flexibility
            valid_indices = indices[(indices >= 0) & (indices < len(self))]  # Filter valid indices
            return [super().__getitem__(i) for i in valid_indices] 
        else:
            # Handle standard slicing and indexing
            return super().__getitem__(index)

    def __setitem__(self, index, value):
        if isinstance(index, list):
            indices = np.array(index)
            valid_indices = indices[(indices >= 0) & (indices < len(self))]
            if len(valid_indices) != len(value):
                raise ValueError("Number of indices and values must match.")

            for i, v in zip(valid_indices, value):
                super().__setitem__(i, v)
        else:
            super().__setitem__(index, value)

my_list = SliceableList([10, 20, 30, 40, 50])

# Slicing with a list of indices
print(my_list[[1, 3, 0]])  # Output: [20, 40, 10]

# Setting values with a list of indices
my_list[[2, 4]] = [99, 88]
print(my_list)  # Output: [10, 20, 99, 40, 88]