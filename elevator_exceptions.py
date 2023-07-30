class BaseElevatorException(Exception):
    """
    Base class for elevator-related exceptions.
    """
    pass


class ElevatorIsFullException(BaseElevatorException):
    """
    Exception raised when a passenger tries to enter the elevator, but it is already at its maximum capacity.
    """
    def __init__(self):
        super().__init__("Elevator is full.")


class ElevatorDoorsClosed(BaseElevatorException):
    """
    Exception raised when a passenger tries to enter the elevator, but the doors are closed.
    """
    def __init__(self):
        super().__init__("Elevator doors are closed. Cannot enter at the moment.")


class PassengerNotFoundException(BaseElevatorException):
    """
    Exception raised when a passenger is not found in the elevator.
    """
    def __init__(self):
        super().__init__("Passenger not found in the elevator.")


class ElevatorPassengerFloorsMismatch(BaseElevatorException):
    """
    Exception raised when the passenger is trying to get into the elevator, which is now on another floor.
    """
    def __init__(self):
        super().__init__("Elevator is on another floor. Cannot enter at the moment.")


class ElevatorFloorOutOfTheRangeException(BaseElevatorException):
    """
    Exception raised when the elevator is requested to move to a floor outside the building's floor range.
    """
    def __init__(self):
        super().__init__("Floor requested is outside the building's floor range.")


class ElevatorIsBrokenException(BaseElevatorException):
    """
    Base exception class for any issues related to the elevator's functionality.
    """
    pass


class ElevatorIsOpenedTheDoorsWhileMoving(ElevatorIsBrokenException):
    """
    Exception raised when the elevator tries to open its doors while still in motion.
    """
    def __init__(self):
        super().__init__("Elevator doors cannot be opened while it is in motion.")


class ElevatorIsMoveWithOpenDoors(ElevatorIsBrokenException):
    """
    Exception raised when the elevator attempts to move while its doors are open.
    """
    def __init__(self):
        super().__init__("Elevator cannot move while its doors are open.")
