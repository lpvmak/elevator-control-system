# Elevator Control System

This project is an implementation of an elevator control system in Python. The control system is capable of simulating elevator activity and handling passenger requests efficiently.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)

## Overview

The elevator control system consists of the following main components:

- **Elevator:** The `Elevator` class represents an elevator. It can move up and down between floors, handle passenger requests, and manage passengers inside the elevator. The elevator's movement and behavior are based on its current queue of floors to stop at and passenger requests.

- **Passenger:** The `Passenger` class represents a passenger waiting for the elevator and intending to travel from one floor to another. Passengers can call the elevator to their current floor, enter the elevator, and exit the elevator at their destination floor.

- **Elevator Observer:** The `IElevatorObserver` interface defines methods that represent events that can be observed in an elevator. Classes implementing this interface can subscribe to an elevator's events to receive notifications about changes in the elevator's state and passenger interactions.

## Features

- Efficient handling of passenger requests: The elevator's queue of floors is sorted based on the current direction to optimize passengers' journeys by not changing direction until the last requested floor in the current direction has been served.

- Capacity management: The elevator has a maximum capacity, and it won't allow more passengers to enter if it reaches its limit.

- Door control: The elevator can open and close its doors at each floor when passengers enter or exit.

- Movement control: The elevator can move up or down between floors based on its current direction and queue of floors to stop at.

- Logging: The system is equipped with logging capabilities to record elevator activity and passenger interactions.

## Requirements

The following are the requirements to run the elevator control system:

- Python 3.x

## Installation

1. Clone the repository:

```bash
git clone https://github.com/lpvmak/elevator-control-system.git
cd elevator-control-system
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To simulate elevator activity over a day, run the `simulate_elevator_activity` function with an instance of the `Elevator` class as an argument:

```python
from elevator import Elevator, simulate_elevator_activity

# Create an instance of the Elevator class
elevator = Elevator(max_capacity=8)

# Simulate elevator activity over a day
simulate_elevator_activity(elevator, probability=0.01, total_simulation_time=24 * 60)
```

The `simulate_elevator_activity` function will generate random passenger requests at a given probability (adjust as needed) and simulate elevator movement and passenger interactions.

## Testing

To run the unit tests, execute the following command:

```bash
pytest elevator_tests.py
```

The unit tests cover various scenarios to ensure the correct functioning of the Elevator and Passenger classes.