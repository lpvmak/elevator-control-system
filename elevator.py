from __future__ import annotations

import logging
import os
import random
import time
from enum import Enum
from typing import List, Set

import elevator_exceptions
from elevator_interface import IElevator, IPassenger, IElevatorObserver


class ElevatorDirection(Enum):
    """Enumeration for elevator direction"""
    DOWN = -1
    IDLE = 0
    UP = 1


class Elevator(IElevator):
    """Class representing an elevator."""

    def __init__(self, max_capacity: int = 8, floors_count: int = 10, observer: IElevatorObserver = None):
        """
        Initializes the Elevator object.

        :param max_capacity: Maximum capacity of the elevator (default: 8).
        :param floors_count: Total number of floors in the building (default: 10).
        """

        self._logger = logging.getLogger('Elevator')
        self._floors_count = floors_count
        self._current_floor = 1
        self._queue: List[int] = []  # Stores the floors requested by passengers
        self._direction = ElevatorDirection.IDLE  # Indicates the current direction of the elevator
        self._max_capacity = max_capacity
        self._passengers: Set[IPassenger] = set()  # Stores the passengers currently inside the elevator
        self._is_open = False  # Indicates whether the elevator doors are open
        self._is_moving = False  # Indicates whether the elevator is moving

        if observer is None:
            class DefaultObserver(IElevatorObserver):
                pass
            observer = DefaultObserver
        self._observer = observer

    # Methods for moving the elevator and updating its status
    def _move_up(self):
        """Move the elevator up one floor."""
        self._logger.debug('Elevator moving up')
        self._current_floor = min((self._current_floor + 1), self._floors_count)

    def _move_down(self):
        """Move the elevator down one floor."""
        self._logger.debug('Elevator moving down')
        self._current_floor = max(self._current_floor - 1, 1)

    def _update_direction(self):
        """
        Update the direction of the elevator based on the current floor and the destination floors in the queue.
        """
        if self._queue:
            direction = self._direction
            if self.current_floor < self._queue[0]:
                self._direction = ElevatorDirection.UP
            elif self.current_floor > self._queue[0]:
                self._direction = ElevatorDirection.DOWN
            if direction is not self._direction:
                self._logger.debug(f'Direction is changed. Moving {self._direction.name}')
        else:
            self._direction = ElevatorDirection.IDLE
            self._logger.debug('Elevator is IDLE')

    def _open_the_doors(self):
        """Open the elevator doors and pop the current floor from the queue as the elevator has arrived at the floor."""
        if self._is_moving:
            raise elevator_exceptions.ElevatorIsOpenedTheDoorsWhileMoving()
        self._logger.debug('Opening the doors')
        self._logger.info(f'Elevator arrived on {self._current_floor} floor')
        self._queue.remove(self._current_floor)
        self._is_open = True
        self._logger.debug('Doors are open')

        self._observer.on_open_doors(self)


    def _close_the_doors(self):
        """Close the elevator doors."""
        self._logger.debug('Closing the doors')
        self._is_open = False
        self._logger.debug('Doors are closed')

        self._observer.on_close_doors(self)

    def _stop_moving(self):
        """Stop the elevator."""
        self._logger.debug('Stopping Elevator')
        self._is_moving = False
        self._logger.debug('Elevator is stopped')

        self._observer.on_stop(self)

    def _start_moving(self):
        """Start the elevator."""
        if self._is_open:
            raise elevator_exceptions.ElevatorIsMoveWithOpenDoors()
        if not self._is_moving:
            self._logger.debug('Starting Elevator')
        self._is_moving = True
        self._logger.debug('Elevator is moving')

        self._observer.on_moving(self)

    def _sort_queue(self):
        """Sort the queue based on the current direction to handle requests efficiently."""

        def key_func(floor):
            """
            A custom key function to determine the sorting order of floors in the elevator's queue.
            The elevator's queue of floors needs to be sorted in a way that optimizes passengers' journey by not changing
            direction until the last requested floor in the current direction has been served. This function calculates a key
            value for each floor, which is then used for sorting.
            """
            if self._direction.value * (floor - self._current_floor) > 0:
                return self._direction.value * (floor - self._current_floor)
            else:
                return self._direction.value * (self._current_floor - floor) + self._floors_count

        self._queue.sort(key=key_func)

    def call_floor(self, floor: int):
        """
        Call the elevator to a specific floor.

        :param floor: The floor to which the elevator is called.
        """
        if floor < 1 or floor > self._floors_count:
            raise elevator_exceptions.ElevatorFloorOutOfTheRangeException()

        if floor not in self._queue and floor:
            self._queue.append(floor)
            self._sort_queue()

        if self._direction is ElevatorDirection.IDLE:
            self._update_direction()
            if self._current_floor == floor:
                self._open_the_doors()

    def move(self):
        """Move the elevator based on the current queue of floors to stop at and handle passenger requests."""
        if self.is_open:
            self._close_the_doors()

        self._update_direction()

        if self._direction is not ElevatorDirection.IDLE:
            self._start_moving()

            if self._direction == ElevatorDirection.UP:
                self._move_up()
            elif self._direction == ElevatorDirection.DOWN:
                self._move_down()

        if self._current_floor in self._queue:
            self._stop_moving()
            self._open_the_doors()
        self._logger.debug(f'Current floor is {self._current_floor}')

    @property
    def current_floor(self) -> int:
        """Get the current floor of the elevator."""
        return self._current_floor

    @property
    def floors_count(self) -> int:
        """Get the floors count."""
        return self._floors_count

    @property
    def is_full(self) -> bool:
        """Check if the elevator is full."""
        return len(self._passengers) == self._max_capacity

    @property
    def is_open(self) -> bool:
        """Check if the elevator doors are open."""
        return self._is_open

    @property
    def passengers(self) -> List[IPassenger]:
        """List of passengers in the elevator"""
        return list(self._passengers)

    def append_passenger(self, passenger: IPassenger):
        """
        Add a passenger to the elevator.

        :param passenger: The Passenger object to be added to the elevator.
        :raises elevator_exceptions.ElevatorIsFullException: If the elevator is already at full capacity.
        :raises elevator_exceptions.ElevatorDoorsClosed: If the elevator's doors are closed.
        :raises elevator_exceptions.ElevatorPassengerFloorsMismatch: If the elevator's current floor mismatch this passenger
        """
        if self.is_full:
            raise elevator_exceptions.ElevatorIsFullException()
        if not self.is_open:
            raise elevator_exceptions.ElevatorDoorsClosed()
        if self.current_floor != passenger.current_floor:
            raise elevator_exceptions.ElevatorPassengerFloorsMismatch()
        self._passengers.add(passenger)
        self._observer.on_passenger_enter(self, passenger)

    def remove_passenger(self, passenger: Passenger):
        """
        Remove a passenger from the elevator.

        :param passenger: The Passenger object to be removed from the elevator.
        :raises elevator_exceptions.PassengerNotFoundException: If the passenger is not found in the elevator.
        """
        if passenger not in self._passengers:
            raise elevator_exceptions.PassengerNotFoundException()
        self._passengers.remove(passenger)
        self._observer.on_passenger_exit(self, passenger)

    def set_observer(self, observer: IElevatorObserver):
        self._observer = observer


class Passenger(IPassenger):
    """Class representing a passenger."""

    _passenger_count = 0

    def __init__(self, current_floor: int, destination_floor: int):
        """
        Initializes the Passenger object.

        :param current_floor: The current floor where the passenger is located.
        :param destination_floor: The destination floor where the passenger wants to go.
        :param passenger_id: The unique ID of the passenger.
        """
        self._logger = logging.getLogger('Passenger')
        self._passenger_id = Passenger._passenger_count
        Passenger._passenger_count += 1
        self._current_floor = current_floor
        self._destination_floor = destination_floor

    def __str__(self):
        """Get a string representation of the passenger."""
        return f"Passenger#{self._passenger_id} ({self._current_floor}->{self._destination_floor})"

    def enter_elevator(self, elevator: IElevator):
        """
        Make the passenger enter the elevator.

        :param elevator: The Elevator object into which the passenger enters.
        """
        self._logger.info(f"{self} is entering the elevator")
        elevator.append_passenger(passenger=self)
        elevator.call_floor(self._destination_floor)

    def exit_elevator(self, elevator: IElevator):
        """
        Make the passenger to exit the elevator.

        :param elevator: The Elevator object from which the passenger exits.
        """
        self._logger.info(f"{self} is leaving the elevator")
        elevator.remove_passenger(self)

    def call_elevator(self, elevator: IElevator):
        """
        Call the elevator to the current floor of the passenger.

        :param elevator: The Elevator object to be called.
        """
        elevator.call_floor(self._current_floor)

    @property
    def current_floor(self):
        """
        Get the current floor where the passenger is located.
        """
        return self._current_floor

    @property
    def destination_floor(self):
        """
        Get the destination floor.
        """
        return self._destination_floor


def setup_logging():
    """Set up logging for the elevator control system."""
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler to log messages to a file
    os.makedirs('logs', exist_ok=True)
    file_handler = logging.FileHandler('logs/elevator_system.log')
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler to log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set the formatter for the handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def simulate_elevator_activity(elevator: Elevator, probability=0.01, total_simulation_time: int = 24 * 60):
    """Simulate elevator activity over a day."""
    logger = logging.getLogger('Simulation')

    def generate_random_floor():
        """Generate a random floor number between 1 and the total number of floors."""
        return random.randint(1, elevator.floors_count)

    def generate_random_destination(current_floor: int):
        """Generate a random destination floor different from the current floor."""
        destination = generate_random_floor()
        while destination == current_floor:
            destination = generate_random_floor()
        return destination

    def generate_random_passenger_request():
        """Generate a random passenger request with current and destination floors."""
        current_floor = generate_random_floor()
        destination_floor = generate_random_destination(current_floor)
        return current_floor, destination_floor

    passengers_waiting = []
    passengers_skipped_elevator = []

    class PassengersElevatorObserver(IElevatorObserver):
        def on_passenger_enter(self, _elevator: IElevator, _passenger: IPassenger):
            for p in _elevator.passengers:
                if p is not _passenger:
                    print(f"{p} meets {_passenger} in elevator")

        def on_open_doors(self, _elevator: IElevator):
            passengers_to_exit = [p for p in elevator.passengers if
                                  p.destination_floor == elevator.current_floor]
            for p in passengers_to_exit:
                p.exit_elevator(_elevator)

            # Simulate passengers entering the elevator if it's on their current floor and it's not full
            passengers_to_enter = [p for p in passengers_waiting if
                                   p.current_floor == elevator.current_floor]
            for p in passengers_to_enter:
                try:
                    p.enter_elevator(_elevator)
                    passengers_waiting.remove(p)
                except Exception as e:
                    passengers_skipped_elevator.append(p)
                    logger.warning(f"Failed to let {p} enter the elevator: {e}")

    elevator.set_observer(PassengersElevatorObserver())

    for minute in range(total_simulation_time):
        # Simulate passengers arriving and pressing the elevator button
        if random.random() < probability:  # Probability of a passenger request in each minute (adjust as needed)
            current_floor, destination_floor = generate_random_passenger_request()
            logger.info(f"Passenger requested elevator: Current Floor {current_floor}, Destination Floor {destination_floor}")
            passenger = Passenger(current_floor, destination_floor)
            passenger.call_elevator(elevator)
            passengers_waiting.append(passenger)

        # Simulate elevator movement
        elevator.move()

        for passenger in passengers_skipped_elevator:
            passenger.call_elevator(elevator)
            passengers_waiting.append(passenger)

        passengers_skipped_elevator = []

        time.sleep(1)


if __name__ == '__main__':
    setup_logging()
    simulate_elevator_activity(Elevator(max_capacity=8), 60)