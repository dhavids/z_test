import random
import matplotlib.pyplot as plt
import numpy as np


class RandomWalk:
    def __init__(self, num_agents=3, num_points=5000, min_step=0.01, max_step=0.06, space=5, goal_radius=0.5):
        self.num_agents = num_agents
        self.num_points = num_points
        self.min_step = min_step
        self.max_step = max_step
        self.space = space
        self.goal_radius = goal_radius
        self.goal_center = (random.uniform(-space, space), random.uniform(-space, space))  # Random goal location
        self.agents = {}
        for i in range(num_agents):
            self.agents[i] = {
                'x_values': [0],
                'y_values': [0],
            }

    def fill_walk(self):
        goal_reached = False
        while not goal_reached and any(len(agent['x_values']) < self.num_points for agent in self.agents.values()):
            for agent in self.agents.values():
                if len(agent['x_values']) < self.num_points:
                    while True:  # Loop until a valid step is found
                        x_direction = random.choice([-1, 1])
                        x_distance = random.uniform(self.min_step, self.max_step) * x_direction
                        x_step = agent['x_values'][-1] + x_distance

                        y_direction = random.choice([-1, 1])
                        y_distance = random.uniform(self.min_step, self.max_step) * y_direction
                        y_step = agent['y_values'][-1] + y_distance

                        if (
                            abs(x_step) <= self.space 
                            and abs(y_step) <= self.space
                            and not self.check_overlap(x_step, y_step, agent)  # Check for overlap
                            and not self.check_goal(x_step, y_step)           # Check for goal
                        ):
                            agent['x_values'].append(x_step)
                            agent['y_values'].append(y_step)
                            break  # Valid step found, exit loop

    def check_overlap(self, x, y, current_agent):
        for other_agent, data in self.agents.items():
            if other_agent != current_agent:  # Don't check against the agent itself
                if (x - data['x_values'][-1])**2 + (y - data['y_values'][-1])**2 <= 0.01**2:                    
                    return True  # Overlap found
        return False  # No overlap

    def check_goal(self, x, y):
        return (x - self.goal_center[0])**2 + (y - self.goal_center[1])**2 <= self.goal_radius**2

    def plot_walk(self):
        plt.figure(figsize=(10, 6))
        plt.xlim(-self.space, self.space)  # Set x-axis limits
        plt.ylim(-self.space, self.space)  # Set y-axis limits

        # Plot the goal region
        goal_circle = plt.Circle(self.goal_center, self.goal_radius, color='blue', alpha=0.5)
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