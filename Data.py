from datetime import datetime
from typing import List, Optional, Dict

class ServerRespond:
    def __init__(self, top_ask: Dict[str, float], top_bid: Dict[str, float], timestamp: datetime):
        self.top_ask = top_ask
        self.top_bid = top_bid
        self.timestamp = timestamp

class Row:
    def __init__(self, price_abc: float, price_def: float, ratio: float, 
                 timestamp: datetime, upper_bound: float, lower_bound: float, 
                 trigger_alert: Optional[float]):
        self.price_abc = price_abc
        self.price_def = price_def
        self.ratio = ratio
        self.timestamp = timestamp
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.trigger_alert = trigger_alert

class DataManipulator:
    @staticmethod
    def generate_row(server_respond: List[ServerRespond]) -> Row:
        price_abc = (server_respond[0].top_ask['price'] + server_respond[0].top_bid['price']) / 2
        price_def = (server_respond[1].top_ask['price'] + server_respond[1].top_bid['price']) / 2
        ratio = price_abc / price_def
        upper_bound = 1 + 0.05
        lower_bound = 1 - 0.05
        timestamp = max(server_respond[0].timestamp, server_respond[1].timestamp)
        trigger_alert = ratio if (ratio > upper_bound or ratio < lower_bound) else None

        return Row(price_abc, price_def, ratio, timestamp, upper_bound, lower_bound, trigger_alert)

import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.data = []
        
    def load_data(self, row: Row):
        self.data.append(row)
        
    def plot(self):
        timestamps = [row.timestamp for row in self.data]
        ratios = [row.ratio for row in self.data]
        
        plt.plot(timestamps, ratios, label='Ratio')
        plt.axhline(y=1.05, color='r', linestyle='--', label='Upper Bound')
        plt.axhline(y=0.95, color='g', linestyle='--', label='Lower Bound')
        
        plt.xlabel('Timestamp')
        plt.ylabel('Ratio')
        plt.title('Price Ratio Over Time')
        plt.legend()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Example data
    server_responses = [
        ServerRespond(top_ask={'price': 100.0}, top_bid={'price': 98.0}, timestamp=datetime.now()),
        ServerRespond(top_ask={'price': 105.0}, top_bid={'price': 103.0}, timestamp=datetime.now())
    ]

    # Generate a row
    row = DataManipulator.generate_row(server_responses)

    # Create and plot graph
    graph = Graph()
    graph.load_data(row)
    graph.plot()
