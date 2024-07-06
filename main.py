import simpy
import numpy as np
import matplotlib.pyplot as plt

class CoffeeShop:
    def __init__(self, env, num_baristas, cook, arrival_rate, order_time1, order_time2, coffee_time1, coffee_time2, food_time, queue_capacity, waiting_capacity, T_o, T_w):
        self.env = env
        self.num_baristas = num_baristas
        self.cook = cook
        self.arrival_rate = arrival_rate
        self.order_time1 = order_time1
        self.order_time2 = order_time2
        self.coffee_time1 = coffee_time1
        self.coffee_time2 = coffee_time2
        self.food_time = food_time
        self.queue_capacity = queue_capacity
        self.waiting_capacity = waiting_capacity
        self.T_o = T_o
        self.T_w = T_w
        self.queue = []
        self.waiting_area = []
        self.revenue = 0
        self.orders = 0
        self.queue_lengths = []
        self.waiting_lengths = []
        self.revenues = []
        
        self.barista_resource = simpy.Resource(env, capacity=num_baristas)
        self.cook_resource = simpy.Resource(env, capacity=cook)
        self.env.process(self.generate_customers())

    def generate_customers(self):
        while True:
            yield self.env.timeout(np.random.exponential(1/self.arrival_rate))
            if len(self.queue) < self.queue_capacity:
                self.env.process(self.handle_customer())

    def handle_customer(self):
        self.queue.append(self.env.now)
        with self.barista_resource.request() as request:
            yield request
            self.queue.pop(0)
            order_type = np.random.choice(['coffee', 'food', 'both'], p=[0.4, 0.3, 0.3])
            if self.env.now % 2 == 0:  # Alternate between baristas
                order_time = np.random.exponential(self.order_time1)
            else:
                order_time = np.random.exponential(self.order_time2)
            yield self.env.timeout(order_time)
            self.waiting_area.append(order_type)
            self.queue_lengths.append(len(self.queue))
            self.waiting_lengths.append(len(self.waiting_area))
            self.revenues.append(self.revenue)
            self.env.process(self.fulfill_order(order_type))

    def fulfill_order(self, order_type):
        if order_type == 'coffee':
            if self.env.now % 2 == 0:  # Alternate between baristas
                coffee_time = np.random.exponential(self.coffee_time1)
            else:
                coffee_time = np.random.exponential(self.coffee_time2)
            with self.barista_resource.request() as request:
                yield request
                yield self.env.timeout(coffee_time)
                self.waiting_area.pop(0)
                self.revenue += 5
        elif order_type == 'food':
            food_time = np.random.exponential(self.food_time)
            with self.cook_resource.request() as request:
                yield request
                yield self.env.timeout(food_time)
                self.waiting_area.pop(0)
                self.revenue += 10
        elif order_type == 'both':
            if self.env.now % 2 == 0:  # Alternate between baristas
                coffee_time = np.random.exponential(self.coffee_time1)
            else:
                coffee_time = np.random.exponential(self.coffee_time2)
            with self.barista_resource.request() as request:
                yield request
                yield self.env.timeout(coffee_time)
            food_time = np.random.exponential(self.food_time)
            with self.cook_resource.request() as request:
                yield request
                yield self.env.timeout(food_time)
            self.waiting_area.pop(0)
            self.revenue += 15
        self.orders += 1

def run_simulation(num_baristas, cook, arrival_rate, order_time1, order_time2, coffee_time1, coffee_time2, food_time, queue_capacity, waiting_capacity, T_o, T_w, run_time=240):
    env = simpy.Environment()
    coffee_shop = CoffeeShop(env, num_baristas, cook, arrival_rate, order_time1, order_time2, coffee_time1, coffee_time2, food_time, queue_capacity, waiting_capacity, T_o, T_w)
    env.run(until=run_time)
    return coffee_shop

def plot_results(coffee_shop, title):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Time (minutes)')
    ax1.set_ylabel('Queue Length', color=color)
    ax1.plot(range(len(coffee_shop.queue_lengths)), coffee_shop.queue_lengths, color=color, label='Queue Length')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.axhline(y=np.mean(coffee_shop.queue_lengths), color=color, linestyle='--', linewidth=1, label='Average Queue Length')

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Revenue ($)', color=color)
    ax2.plot(range(len(coffee_shop.revenues)), coffee_shop.revenues, color=color, label='Revenue')
    ax2.tick_params(axis='y', labelcolor=color)

    color = 'tab:red'
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))
    ax3.set_ylabel('Waiting Area Length', color=color)
    ax3.plot(range(len(coffee_shop.waiting_lengths)), coffee_shop.waiting_lengths, color=color, label='Waiting Area Length')
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.axhline(y=np.mean(coffee_shop.waiting_lengths), color=color, linestyle='--', linewidth=1, label='Average Waiting Area Length')

    fig.tight_layout()
    plt.title(title)
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    plt.show()

# Parameters
num_baristas = 2
cook = 1
arrival_rate = 1/2  # One customer every 2 minutes
order_time1 = 3
order_time2 = 4
coffee_time1 = 2
coffee_time2 = 3
food_time = 5
queue_capacity = 10
waiting_capacity = 20
run_time = 240  # Simulate for 240 minutes

# Calculate T_o and T_w based on key parameters
T_o = queue_capacity * (1/order_time1 + 1/order_time2) / (2 * arrival_rate)
T_w = waiting_capacity * (1/coffee_time1 + 1/coffee_time2) / (arrival_rate * (0.4 + 0.3))

# Run the simulation
coffee_shop = run_simulation(num_baristas, cook, arrival_rate, order_time1, order_time2, coffee_time1, coffee_time2, food_time, queue_capacity, waiting_capacity, T_o, T_w, run_time)
plot_results(coffee_shop, 'Coffee Shop Simulation')
