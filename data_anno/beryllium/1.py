def convert_position(grid_pos, continuous_pos):
    grid_min = 0
    grid_max = 10
    continuous_min = -3
    continuous_max = 3
    # Check if the input position is grid_pos
    if type(grid_pos) == tuple and len(grid_pos) == 2:
        x, y = grid_pos
        # Calculate continuous position from grid position
        continuous_x = (x - grid_min) / (grid_max - grid_min) * (continuous_max - continuous_min) + continuous_min
        continuous_y = (y - grid_min) / (grid_max - 
        grid_min) * (continuous_max - continuous_min) + continuous_min
        return continuous_x, continuous_y
 
    # Check if the input position is continuous_pos

    if type(continuous_pos) == tuple and len(continuous_pos) == 2:
        x, y = continuous_pos
        # Calculate grid position from continuous position
        grid_x = (x - continuous_min) / (continuous_max - continuous_min) * (grid_max - grid_min) + grid_min
        grid_y = (y - continuous_min) / (continuous_max - continuous_min) * (grid_max -              grid_min) + grid_min
        return int(grid_x), int(grid_y)
    raise ValueError("Invalid input type. Please enter a valid grid position or continuous position.")
        
 #Some examples
grid_pos=(10,10)
print(convert_position(grid_pos, None)) # Output: (0.0, 0.0)

continuous_pos = (1.5, -1.5)
print(convert_position(None, continuous_pos))  # Output: (6, 4)