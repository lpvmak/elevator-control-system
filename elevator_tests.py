# test_elevator.py
import pytest

import elevator_exceptions
from elevator import Elevator, ElevatorDirection, Passenger


def test_elevator_initialization():
    """
    Test the initialization of the Elevator class.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)

    assert elevator.current_floor == 1
    assert elevator.is_full is False
    assert elevator.is_open is False
    assert elevator._direction == ElevatorDirection.IDLE
    assert elevator._max_capacity == 6
    assert elevator._is_moving is False
    assert elevator._queue == []
    assert elevator._passengers == set()


def test_elevator_moving_up():
    """
    Test the elevator's movement in the upward direction.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)
    elevator._current_floor = 5
    elevator._queue = [7, 9, 11]

    elevator.move()

    assert elevator.current_floor == 6


def test_elevator_moving_down():
    """
    Test the elevator's movement in the downward direction.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)
    elevator._current_floor = 10
    elevator._queue = [7, 5, 3]

    elevator._move_down()

    assert elevator.current_floor == 9


def test_elevator_update_direction():
    """
    Test the update_direction method of the Elevator class.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)
    elevator._current_floor = 10
    elevator._queue = [15, 12, 17]

    elevator._update_direction()

    assert elevator._direction == ElevatorDirection.UP

    elevator._current_floor = 18
    elevator._queue = [15, 12, 9]

    elevator._update_direction()

    assert elevator._direction == ElevatorDirection.DOWN

    elevator._current_floor = 13
    elevator._queue = []

    elevator._update_direction()

    assert elevator._direction == ElevatorDirection.IDLE


def test_elevator_open_and_close_doors():
    """
    Test the open_the_doors and close_the_doors methods of the Elevator class.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)
    elevator._is_moving = True

    with pytest.raises(elevator_exceptions.ElevatorIsOpenedTheDoorsWhileMoving):
        elevator._open_the_doors()

    elevator._current_floor = 7
    elevator._is_moving = False
    elevator._is_open = False
    elevator._queue = [7, 5, 3]

    elevator._open_the_doors()

    assert elevator._is_open is True
    assert elevator._queue == [5, 3]


def test_elevator_start_and_stop_moving():
    """
    Test the _start_moving and _stop_moving methods of the Elevator class.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)
    elevator._is_open = True

    with pytest.raises(elevator_exceptions.ElevatorIsMoveWithOpenDoors):
        elevator._start_moving()

    elevator._is_open = False

    elevator._start_moving()

    assert elevator._is_moving is True

    elevator._stop_moving()

    assert elevator._is_moving is False


def test_elevator_sort_queue():
    """
    Test the _sort_queue method of the Elevator class.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)
    elevator._current_floor = 10
    elevator._direction = ElevatorDirection.UP
    elevator._queue = [15, 12, 17, 3, 8]

    elevator._sort_queue()

    assert elevator._queue == [12, 15, 17, 8, 3]


def test_elevator_call_floor():
    """
    Test the call_floor method of the Elevator class.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)

    with pytest.raises(elevator_exceptions.ElevatorFloorOutOfTheRangeException):
        elevator.call_floor(0)

    with pytest.raises(elevator_exceptions.ElevatorFloorOutOfTheRangeException):
        elevator.call_floor(25)

    elevator.call_floor(7)
    elevator.call_floor(5)
    elevator.call_floor(10)

    assert elevator._queue == [5, 7, 10]


def test_elevator_move():
    """
    Test the movement of the elevator based on the current queue.
    """
    elevator = Elevator(max_capacity=6, floors_count=20)
    elevator._is_open = False
    elevator._queue = [5, 7, 10]

    elevator.move()

    assert elevator.current_floor == 2
    assert elevator._direction == ElevatorDirection.UP
    assert elevator._is_moving is True
    assert elevator._is_open is False

    for i in range(3):
        elevator.move()

    assert elevator.current_floor == 5
    assert elevator._direction == ElevatorDirection.UP
    assert elevator._is_moving is False
    assert elevator._is_open is True

    elevator.move()

    assert elevator.current_floor == 6
    assert elevator._direction == ElevatorDirection.UP
    assert elevator._is_moving is True
    assert elevator._is_open is False

    elevator.move()

    assert elevator.current_floor == 7
    assert elevator._direction == ElevatorDirection.UP
    assert elevator._is_moving is False
    assert elevator._is_open is True

    for i in range(4):
        elevator.move()

    assert elevator.current_floor == 10
    assert elevator._direction == ElevatorDirection.IDLE


def test_passenger_initialization():
    """
    Test the initialization of the Passenger class.
    """
    passenger = Passenger(current_floor=3, destination_floor=7)
    assert passenger.current_floor == 3


def test_passenger_enter_and_exit_elevator():
    """
    Test the enter_elevator and exit_elevator methods of the Passenger class.
    """
    elevator = Elevator(max_capacity=2, floors_count=10)
    passenger1 = Passenger(current_floor=1, destination_floor=3)
    passenger2 = Passenger(current_floor=1, destination_floor=2)
    passenger3 = Passenger(current_floor=1, destination_floor=4)

    passenger1.call_elevator(elevator)
    passenger1.enter_elevator(elevator)
    assert len(elevator._passengers) == 1
    assert elevator._queue == [3]
    passenger2.enter_elevator(elevator)

    with pytest.raises(elevator_exceptions.ElevatorIsFullException):
        passenger3.enter_elevator(elevator)

    elevator.move()
    passenger2.exit_elevator(elevator)
    assert len(elevator._passengers) == 1
    assert elevator._queue == [3]

    elevator.move()
    passenger1.exit_elevator(elevator)
    assert len(elevator._passengers) == 0
    assert elevator._queue == []


def test_passenger_call_elevator():
    """
    Test the call_elevator method of the Passenger class.
    """
    elevator = Elevator(max_capacity=2, floors_count=10)
    passenger1 = Passenger(current_floor=2, destination_floor=6)
    passenger2 = Passenger(current_floor=3, destination_floor=7)

    passenger1.call_elevator(elevator)
    assert elevator._queue == [2]

    passenger2.call_elevator(elevator)
    assert elevator._queue == [2, 3]

    elevator.move()
    passenger1.enter_elevator(elevator)
    assert elevator._queue == [3, 6]

    elevator.move()
    passenger2.enter_elevator(elevator)
    assert elevator._queue == [6, 7]


def test_elevator_exceptions():
    """
    Test various exception scenarios in the Elevator and Passenger classes.
    """
    elevator = Elevator(max_capacity=2, floors_count=10)
    passenger1 = Passenger(current_floor=2, destination_floor=6)

    with pytest.raises(elevator_exceptions.PassengerNotFoundException):
        elevator.remove_passenger(passenger1)

    with pytest.raises(elevator_exceptions.ElevatorIsFullException):
        elevator._passengers.add(Passenger(1, 2))
        elevator._passengers.add(Passenger(1, 2))
        elevator.append_passenger(passenger1)

    elevator._passengers = set()

    with pytest.raises(elevator_exceptions.ElevatorIsMoveWithOpenDoors):
        elevator._is_open = True
        elevator._start_moving()

    with pytest.raises(elevator_exceptions.ElevatorIsOpenedTheDoorsWhileMoving):
        elevator._is_moving = True
        elevator._open_the_doors()

    with pytest.raises(elevator_exceptions.ElevatorDoorsClosed):
        elevator._is_open = False
        elevator.append_passenger(passenger1)


# Add more test cases as needed for more scenarios


if __name__ == '__main__':
    pytest.main()
