# Placeholder for dashboard.py
# ui/dashboard.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time

class LiveDashboard:
    def __init__(self):
        self.risk_scores = []
        self.timestamps = []
        self.start_time = time.time()

        # Setup the figure
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Real-Time Collision Risk Monitor')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Risk Score')
        self.line, = self.ax.plot([], [], 'r-', linewidth=2)
        self.ax.set_ylim(0, 1.1)
        self.ax.grid(True)

    def update_plot(self, frame):
        # Dummy simulation: Append random risk values
        current_time = time.time() - self.start_time
        new_risk = random.uniform(0, 1)

        self.timestamps.append(current_time)
        self.risk_scores.append(new_risk)

        self.line.set_data(self.timestamps, self.risk_scores)
        self.ax.set_xlim(0, max(10, current_time + 5))
        return self.line,

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000)
        plt.show()
