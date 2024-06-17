import random
import matplotlib.pyplot as plt

'''
class RandomWalk:
    def __init__(self, num_agents=3, num_points=5000, min_step=0.01, max_step=0.06, space=5, goal_x=4, goal_y=4, goal_radius=0.5):
        self.num_agents = num_agents
        self.num_points = num_points
        self.min_step = min_step
        self.max_step = max_step
        self.space = space

        self.goal_x = goal_x  # center x-coordinate of the goal region
        self.goal_y = goal_y  # center y-coordinate of the goal region
        self.goal_radius = goal_radius

        self.agents = {}
        for i in range(num_agents):
            self.agents[i] = {
                'x_values': [0],
                'y_values': [0],
            }

    def fill_walk(self):
        goal_reached = False
        while not goal_reached and any(len(agent['x_values']) < self.num_points for agent in self.agents.values()):
            for agent, data in self.agents.items():
                if len(data['x_values']) < self.num_points:
                    x_direction = random.choice([-1, 1])
                    x_distance = random.uniform(self.min_step, self.max_step) * x_direction
                    x_step = data['x_values'][-1] + x_distance

                    y_direction = random.choice([-1, 1])
                    y_distance = random.uniform(self.min_step, self.max_step) * y_direction
                    y_step = data['y_values'][-1] + y_distance

                    if abs(x_step) <= self.space and abs(y_step) <= self.space:
                        data['x_values'].append(x_step)
                        data['y_values'].append(y_step)

                        # Check if the goal is reached
                        if (x_step - self.goal_x)**2 + (y_step - self.goal_y)**2 <= self.goal_radius**2:
                            goal_reached = True
                            break  # Break out of the outer loop (agent reached goal)
    def plot_walk(self):
        plt.figure(figsize=(10, 6))
        plt.xlim(-self.space, self.space)  # Set x-axis limits
        plt.ylim(-self.space, self.space)  # Set y-axis limits

        # Plot the goal region
        goal_circle = plt.Circle((self.goal_x, self.goal_y), self.goal_radius, color='blue', alpha=0.5)
        plt.gca().add_patch(goal_circle) 

        # Plot full continuous space
        plt.axvline(x=0, color='black', linewidth=0.5)  # x-axis
        plt.axhline(y=0, color='black', linewidth=0.5)  # y-axis
        plt.fill_between([-self.space, self.space], -self.space, self.space, color='lightgray', alpha=0.5)

        for agent, data in self.agents.items():
            plt.plot(data['x_values'], data['y_values'], label=f'Agent {agent+1}')
            plt.scatter(data['x_values'][0], data['y_values'][0], c='green', s=100)  # start
            plt.scatter(data['x_values'][-1], data['y_values'][-1], c='red', s=100)    # end

        plt.title("Multiple Random Walks")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.legend()
        plt.grid(True)
        plt.show()

# Example Usage (3 agents)
rw = RandomWalk(num_agents=3)
rw.fill_walk()
rw.plot_walk()
#'''

import numpy as np
import matplotlib.pyplot as plt

class RandomWalk:
    def __init__(self, num_agents=3, num_points=5000, min_step=0.01, max_step=0.06, space=5, goal_x=4, goal_y=4, goal_radius=0.5):
        self.num_agents = num_agents
        self.num_points = num_points
        self.min_step = min_step
        self.max_step = max_step
        self.space = space

        self.goal_x = goal_x  # center x-coordinate of the goal region
        self.goal_y = goal_y  # center y-coordinate of the goal region
        self.goal_radius = goal_radius

        # Initialize the positions of agents as NumPy arrays
        self.agents_x = np.zeros((num_agents, num_points))
        self.agents_y = np.zeros((num_agents, num_points))
        # Boolean array to track if each agent has reached the goal
        self.goal_reached = np.zeros(num_agents, dtype=bool)

    def fill_walk(self):
        #  Loop through all points and fill the arrays
        for i in range(1, self.num_points):
            if np.all(self.goal_reached):
                break
            
            # Generate random steps and assign directions for all agents
            steps = np.random.uniform(self.min_step, self.max_step, (self.num_agents, 2))
            directions = np.random.choice([-1, 1], (self.num_agents, 2))
            steps *= directions

            # Calculate new positions
            new_x = self.agents_x[:, i-1] + steps[:, 0]
            new_y = self.agents_y[:, i-1] + steps[:, 1]

            # Check if new positions are within bounds and not yet reached the goal
            within_bounds = (np.abs(new_x) <= self.space) & (np.abs(new_y) <= self.space)
            self.agents_x[:, i] = np.where(within_bounds & ~self.goal_reached, new_x, self.agents_x[:, i-1])
            self.agents_y[:, i] = np.where(within_bounds & ~self.goal_reached, new_y, self.agents_y[:, i-1])

            # Compute distance to goal and update goal_reached status
            distance_to_goal = (self.agents_x[:, i] - self.goal_x)**2 + (self.agents_y[:, i] - self.goal_y)**2
            self.goal_reached = self.goal_reached | (distance_to_goal <= self.goal_radius**2)


    def plot_walk(self):
        plt.figure(figsize=(10, 6))
        plt.xlim(-self.space, self.space)  # Set x-axis limits
        plt.ylim(-self.space, self.space)  # Set y-axis limits

        # Plot the goal region
        goal_circle = plt.Circle((self.goal_x, self.goal_y), self.goal_radius, color='blue', alpha=0.5)
        plt.gca().add_patch(goal_circle) 

        # Plot full continuous space
        plt.axvline(x=0, color='black', linewidth=0.5)  # x-axis
        plt.axhline(y=0, color='black', linewidth=0.5)  # y-axis
        plt.fill_between([-self.space, self.space], -self.space, self.space, color='lightgray', alpha=0.5)

        for i in range(self.num_agents):
            plt.plot(self.agents_x[i], self.agents_y[i], label=f'Agent {i+1}')
            plt.scatter(self.agents_x[i, 0], self.agents_y[i, 0], c='green', s=100)  # start
            plt.scatter(self.agents_x[i, -1], self.agents_y[i, -1], c='red', s=100)    # end

        plt.title("Multiple Random Walks")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.legend()
        plt.grid(True)
        plt.show()

# Example Usage (3 agents)
rw = RandomWalk(num_agents=3)
rw.fill_walk()
rw.plot_walk()
