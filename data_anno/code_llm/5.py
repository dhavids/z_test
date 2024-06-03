import random
import matplotlib.pyplot as plt

class RandomWalk:
    """A class to generate random walks."""

    def __init__(self, num_points=5000, step=0.01, space=5):
        """Initialize attributes of a walk."""
        self.num_points = num_points
        self.step = step
        self.space = space
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        """Calculate all the points in the walk."""
        while len(self.x_values) < self.num_points:
            x_direction = random.choice([-self.step, self.step])
            x_distance = x_direction  # Simplified as step size is fixed
            x_step = self.x_values[-1] + x_distance

            y_direction = random.choice([-self.step, self.step])
            y_distance = y_direction  # Simplified as step size is fixed
            y_step = self.y_values[-1] + y_distance

            # Check if the step is within the allowed space
            if abs(x_step) <= self.space and abs(y_step) <= self.space:
                self.x_values.append(x_step)
                self.y_values.append(y_step)
            else:  # if step takes agent out of bounds, do not add to list. 
                pass

    def plot_walk(self):
        """Plot the points in the walk."""
        plt.figure(figsize=(10, 6))  
        plt.plot(self.x_values, self.y_values, linewidth=1)  
        plt.scatter(0, 0, c='green', s=100)  # starting point
        plt.scatter(self.x_values[-1], self.y_values[-1], c='red', s=100)  # ending point

        plt.title("Random Walk")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.grid(True)
        plt.show()


# Example Usage
rw = RandomWalk()  # Create a RandomWalk instance
rw.fill_walk()  # Calculate the walk
rw.plot_walk()  # Plot the walk