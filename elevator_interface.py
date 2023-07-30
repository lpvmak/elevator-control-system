from __future__ import annotations

from _ast import List
from abc import ABC, abstractmethod


class IPassenger(ABC):
    """Abstract class representing a passenger."""

    @abstractmethod
    def enter_elevator(self, elevator: IElevator):
        """
        Method to allow the passenger to enter the elevator.

        :param elevator: The Elevator object that the passenger wants to enter.
        :raises elevator_exceptions.ElevatorIsFullException: If the elevator is already at full capacity.
        """
        pass

    @abstractmethod
    def exit_elevator(self, elevator: IElevator):
        """
        Method to allow the passenger to exit the elevator.

        :param elevator: The Elevator object that the passenger wants to exit.
        """
        pass

    @abstractmethod
    def call_elevator(self, elevator: IElevator):
        """
        Method for the passenger to call the elevator to their current floor.

        :param elevator: The Elevator object that the passenger wants to call.
        """
        pass

    @property
    @abstractmethod
    def current_floor(self):
        """
        Get the current floor where the passenger is located.
        """
        pass
    
    @property
    @abstractmethod
    def destination_floor(self):
        """
        Get the destination floor.
        """
        pass


class IElevator(ABC):
    """Abstract class representing an elevator."""

    @abstractmethod
    def move(self):
        """Move the elevator based on the current queue of floors to stop at and handle passenger requests."""
        pass

    @abstractmethod
    def call_floor(self, floor: int):
        """
        Call the elevator to a specific floor.

        :param floor: The floor to which the elevator is called.
        """
        pass

    @property
    @abstractmethod
    def current_floor(self) -> int:
        """Get the current floor of the elevator."""
        pass
    
    @property
    @abstractmethod
    def floors_count(self) -> int:
        """Get the floors count."""
        return self._floors_count

    @property
    @abstractmethod
    def is_full(self) -> bool:
        """Check if the elevator is full."""
        pass

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Check if the elevator doors are open."""
        pass

    @property
    @abstractmethod
    def passengers(self) -> List[IPassenger]:
        """List of passengers in the elevator"""
        pass

    @abstractmethod
    def append_passenger(self, passenger: IPassenger):
        """
        Add a passenger to the elevator.

        :param passenger: The Passenger object to be added to the elevator.
        :raises elevator_exceptions.ElevatorIsFullException: If the elevator is already at full capacity.
        """
        pass

    @abstractmethod
    def remove_passenger(self, passenger: IPassenger):
        """
        Remove a passenger from the elevator.

        :param passenger: The Passenger object to be removed from the elevator.
        :raises elevator_exceptions.PassengerNotFoundException: If the passenger is not found in the elevator.
        """
        pass


class IElevatorObserver:
    """
    Interface for an elevator observer.

    This interface defines methods that represent events that can be observed in an elevator.
    Classes implementing this interface can subscribe to an elevator's events to receive notifications
    about changes in the elevator's state and passenger interactions.
    """

    def on_open_doors(self, elevator: IElevator):
        """
        Event triggered when the elevator's doors are opened.

        :param elevator: The elevator instance whose doors were opened.
        """
        pass

    def on_close_doors(self, elevator: IElevator):
        """
        Event triggered when the elevator's doors are closed.

        :param elevator: The elevator instance whose doors were closed.
        """
        pass

    def on_moving(self, elevator: IElevator):
        """
        Event triggered when the elevator starts moving.

        :param elevator: The elevator instance that started moving.
        """
        pass

    def on_stop(self, elevator: IElevator):
        """
        Event triggered when the elevator stops at a floor.

        :param elevator: The elevator instance that has stopped.
        """
        pass

    def on_passenger_enter(self, elevator: IElevator, passenger: IPassenger):
        """
        Event triggered when a passenger enters the elevator.

        :param elevator: The elevator instance where the passenger entered.
        :param passenger: The passenger who entered the elevator.
        """
        pass

    def on_passenger_exit(self, elevator: IElevator, passenger: IPassenger):
        """
        Event triggered when a passenger exits the elevator.

        :param elevator: The elevator instance where the passenger exited.
        :param passenger: The passenger who exited the elevator.
        """
        pass




