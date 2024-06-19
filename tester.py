import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

class Plotter:

    def __init__(self, x_min=0, y_min=0, x_max=1920, y_max=1080, num_agents=3, log_path=None, verbose=False,
                 env_dict=None) -> None:

        self.num_agents = num_agents
        self.agents = [id for id in range(num_agents)]
        self.verbose = verbose
        self.all_x = {id: [] for id in self.agents}
        self.all_y = {id: [] for id in self.agents}
        self.curr_id = None
        self.mouse_pressed = False
        self.key = None
        self.colors = ['r', 'g', 'b', 'c', 'y']
        self.log_path = log_path
        self.env_dict = env_dict
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_aspect('equal')
        self.x_min = x_min
        self.y_min = y_min
        self.width = x_max - x_min
        self.height = y_max - y_min
        self.lines = [self.ax.plot([], [], '-', c=self.colors[i])[0] for i in self.agents]
        
        self.prep_fig_from_env()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.init_text()
    
    def prep_fig_from_env(self):
        if self.env_dict is not None:
            soft_bound = self.env_dict.get('env_bound')
            landmarks = self.env_dict.get('landmarks')
            landmark_size = self.env_dict.get('landmark_size')
            if isinstance(soft_bound, list):
                x_lim, y_lim = soft_bound[0]
                width = soft_bound[1][0] - x_lim
                height = soft_bound[1][1] - y_lim
                rect = Rectangle((x_lim, y_lim), width, height, fill=False, ls='--', lw=0.2, 
                                 color='0', alpha=0.5)
                self.ax.add_patch(rect)
            else:
                print("Invalid env boundary data")

            if isinstance(landmarks, list) and isinstance(landmark_size, float):
                for pos in landmarks:
                    circle = Circle(pos, radius=landmark_size, color='m', alpha=0.2)
                    self.ax.add_patch(circle)
            else:
                print("Invalid landmark data")
    
        else:
            print("No env dict found")


    def connect(self):
        """Connect to all the events we need."""
        self.cidpress = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_move)
        self.cidkr = self.fig.canvas.mpl_connect(
            'key_release_event', self.on_key_released)
    
    def on_press(self, event):
        self.mouse_pressed = True
        self.info = True
        if self.verbose: print("Mouse pressed")

    def on_release(self, event):
        self.mouse_pressed = False
        if self.verbose: print("Mouse released")
        
        if self.curr_id is not None:
            self.update_text(f"Not Tracking...")

    def on_move(self, event):

        if self.mouse_pressed and self.curr_id is not None:
            # append event's data to agent lists
            self.all_x[self.curr_id].append(event.xdata)
            self.all_y[self.curr_id].append(event.ydata)
            self.update_fig()
            self.update_text(f"Tracking...")
        
        elif self.mouse_pressed:
            if self.info:
                print(f"Enter an agent ID between 0 and {self.num_agents-1} to Start")
                self.update_text(f"Error: No agent selected")
                self.info = False
    
    def on_key_released(self, event):
        self.key = event.key

        if self.key in ['m', 'M']:
            self.log_points()
            return
        
        if self.key in ['b', 'B','c', 'C']:
            clear_all = None if self.key in ['b', 'B'] else True
            self.clear_points(clear_all)
            return

        try:
            self.key = int(self.key)
            if self.key in self.agents:
                self.curr_id = self.key
                print("Current agent is:", self.curr_id)
                self.update_text()
            
            else:
                print(f"Please enter an agent ID between 0 and {self.num_agents-1}")
                self.curr_id = None
                self.update_text(f"Error: Not between 0 and {self.num_agents-1}")

        except Exception as e:
            print(f"Please enter an integer")
            self.curr_id = None
            self.update_text(f"Error: Not an INT!")
    
    def update_fig(self):
        # restore background
        self.fig.canvas.restore_region(self.background)
        # update plot's data  
        for id in self.agents:
            self.lines[id].set_data(self.all_x[id], self.all_y[id])
            # redraw just the points
            self.ax.draw_artist(self.lines[id])
        # fill in the axes rectangle
        self.fig.canvas.blit(self.ax.bbox)
        plt.draw()
    
    def init_text(self):
        """
        TODO: Usage instruction and key mapping information
        """
        x_pos = 0.8 * self.width + self.x_min
        y_pos = 1.02 * self.height + self.y_min
        self.id_text = self.ax.text(x_pos, y_pos, f"Curr ID: {self.curr_id}", c='0', fontsize=12)
        x_pos = 0 * self.width + self.x_min
        self.message = self.ax.text(x_pos, y_pos, f"", c='r', fontsize=10)

    def update_text(self, message=None):
        self.id_text.set_text(f"Curr ID: {self.curr_id}")
        color = '0' if self.curr_id is None else self.colors[self.curr_id]
        self.id_text.set_color(color)
        if message:
            self.message.set_text(f"{message}")
        else:
            self.message.set_text(f"")
        plt.draw()
    
    def log_points(self):
        all_pos = []
        max_step = max([len(points) for points in self.all_x.values()])

        padding = [-self.width, -self.height]
        for i in range(max_step):
            #temp = [val if j < len(x_p) else (-self.width, -self.height) for ]
            step_pos = []
            for id in self.agents:
                if i < len(self.all_x[id]):
                    temp = [self.all_x[id][i], self.all_y[id][i]]
                
                elif len(self.all_x[id]) > 0:
                    temp = [self.all_x[id][-1], self.all_y[id][-1]]
                
                else:
                    temp = padding 

                step_pos.append(temp)
            all_pos.append(step_pos)

        import csv
        path = self.log_path if self.log_path else "all_pos.csv"

        with open(path, 'w') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([f"Agent {id}" for id in self.agents])
            csvwriter.writerows(all_pos)
        
        print("Positions logged")
        self.update_text(f"Positions logged")

    def clear_points(self, clear_all=False):
        if self.curr_id is not None:
            if clear_all:
                self.all_x[self.curr_id] = []
                self.all_y[self.curr_id] = []
            
            else:
                if len(self.all_x[self.curr_id]) > 0:
                    del self.all_x[self.curr_id][-1]
                    del self.all_y[self.curr_id][-1]
            
            self.update_fig()
        
        else:
            print("No agent selected")
            self.update_text(f"Error: No agent selected")



env_dict = {
    "env_bound": [(-2,-2), (2,2)],
    "landmarks": [[-1.6,1.6],[0,0.2],[1.6,-1.5]],
    "landmark_size": 0.2
}

plots = Plotter(-3, -3, 3, 3, env_dict=env_dict)
plots.connect()
plt.show()