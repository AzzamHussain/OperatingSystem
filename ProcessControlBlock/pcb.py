import queue
from random import randint
from texttable import Texttable

# Define a class to represent a process in a CPU scheduling scenario.
class Process:
    def __init__(self, process_id, arrival_time, burst_time, execution_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.time_left = execution_time
        self.is_arrived = False
        self.is_ready = False
        self.completion_time = 0
        self.turn_arount_time = 0
        self.wait_time = 0
        self.response_time = 0

    def decrement_time_left(self):
        self.time_left -= 1

    def set_completion_time(self, time_passed):
        self.completion_time = time_passed

    def set_turn_around_time(self):
        self.turn_arount_time = self.completion_time - self.arrival_time

    def set_wait_time(self):
        self.wait_time = self.turn_arount_time - self.burst_time

    def set_response_time(self, time_passed):
        self.response_time = time_passed - self.arrival_time

# Function to get input values from the user.
def input_entity(entity: str, min: int, max: int):
    while True:
        number_of_entities = int(input(f'Enter the {entity} (min: {min}, max: {max}):- '))
        if min <= number_of_entities <= max:
            return number_of_entities

# Check if any process still has time left to execute.
def check_is_execution_completed(process_list):
    for process in process_list:
        if process.time_left > 0:
            return True
    return False

# Function to print the process details in a formatted table.
def print_process_table(process_list):
    table = Texttable()
    table_rows = [["process_id", "arrival_time", "burst_time", "completion_time", "turn_around_time", "wait_time", "response_time"]]
    for process in process_list:
        new_row = [process.process_id, process.arrival_time, process.burst_time, process.completion_time, process.turn_arount_time, process.wait_time, process.response_time]
        table_rows.append(new_row)
    table.add_rows(table_rows)
    table.set_max_width(200)
    print(table.draw())

# If the main block
if __name__ == "__main__":
    # Ask for the number of processes
    number_of_processes = input_entity("number of processes", 3, 5)

    # Create a list to hold all process objects
    processes = []
    for i in range(number_of_processes):
        process_id = i + 1
        arrival_time = input_entity(f'Arrival time of process {process_id}', 0, 10)
        execution_time = input_entity(f'Execution time of process {process_id}', 1, 10)
        processes.append(Process(process_id, arrival_time, execution_time, execution_time))

    # Input quantum size for round-robin scheduling
    quantum_size = input_entity("quantum size", 1, 3)

    ready_queue = []
    running_queue = []
    time_passed = 0

    def put_processes_in_ready_queue(processes):
        for process in processes:
            if process.arrival_time <= time_passed and not process.is_arrived:
                process.is_arrived = True
                ready_queue.append(process)

    # Initially put arrived processes in ready queue
    put_processes_in_ready_queue(processes)

    while check_is_execution_completed(processes):
        if len(ready_queue) > 0:
            ready_process = ready_queue.pop(0)
            if not ready_process.is_ready:
                ready_process.set_response_time(time_passed)
                ready_process.is_ready = True
            running_queue.append(ready_process)

            time_quanta = 0
            while time_quanta < quantum_size:
                time_passed += 1
                time_quanta += 1
                running_queue[0].decrement_time_left()
                if running_queue[0].time_left == 0:
                    break

            ran_process = running_queue.pop(0)
            print_process_table([ran_process])
            put_processes_in_ready_queue(processes)
            if ran_process.time_left > 0:
                ready_queue.append(ran_process)
            else:
                ran_process.set_completion_time(time_passed)
                ran_process.set_turn_around_time()
                ran_process.set_wait_time()
        else:
            time_passed += 1
            put_processes_in_ready_queue(processes)

    print("Final Process List")
    print_process_table(processes)
