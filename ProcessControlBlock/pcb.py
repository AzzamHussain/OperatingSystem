import queue
from random import randint
from texttable import Texttable

# Define a class to represent a process in a CPU scheduling scenario.
class Process:
    # Constructor to initialize process attributes.
    def __init__(self, process_id, arrival_time, burst_time, execution_time):
        self.process_id = process_id  # Unique ID of the process
        self.arrival_time = arrival_time  # Time at which the process arrives in the queue
        self.burst_time = burst_time  # Original burst time (execution time)
        self.time_left = execution_time  # Time left for the process to execute
        self.is_arrived = False  # Flag to check if process has arrived in the queue
        self.is_ready = False  # Flag to check if process is ready for execution
        self.completion_time = 0  # Time at which process completes execution
        self.turn_arount_time = 0  # Time from arrival to completion
        self.wait_time = 0  # Time spent waiting in the queue
        self.response_time = 0  # First response time after execution starts

    # Decrease the remaining execution time of the process.
    def decrement_time_left(self):
        self.time_left -= 1

    # Set the time when the process finishes execution.
    def set_completion_time(self, time_passed):
        self.completion_time = time_passed

    # Calculate and set the turnaround time (completion time - arrival time).
    def set_turn_around_time(self):
        self.turn_arount_time = self.completion_time - self.arrival_time

    # Calculate and set the wait time (turnaround time - burst time).
    def set_wait_time(self):
        self.wait_time = self.turn_arount_time - self.burst_time

    # Set the response time (when the process first gets the CPU).
    def set_response_time(self, time_passed):
        self.response_time = time_passed - self.arrival_time

# Function to get input values from the user.
def input_entity(entity: str, min: int, max: int):
    number_of_entities = None
    while True:
        # Take input from the user within a specific range.
        number_of_entities = int(input(f'Enter the {entity} (min: {min}, max: {max}):- '))
        # Ensure the input is within the given range.
        if number_of_entities >= min and number_of_entities <= max:
            break
    return number_of_entities

# Function to check if any process still has time left to execute.
def check_should_execution_proceed(process_list):
    should_execution_proceed = False
    for process in process_list:
        if process.time_left > 0:
            should_execution_proceed = True
            break
    return should_execution_proceed

# Function to print the list of process details.
def print_process_list(process_list):
    for process in process_list:
        print(vars(process))  # Print attributes of each process.
    print()

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

# Function to check if all processes have completed execution.
def check_is_execution_completed(process_list):
    is_execution_completed = False
    for process in process_list:
        if process.time_left > 0:
            is_execution_completed = True
            break
    return is_execution_completed

if __name__ == "__main__":
    # Take input for the number of processes.
    number_of_processes = input_entity("number of processes", 3, 5)

    # Create a list to hold all the process objects.
    processes = []
    for i in range(number_of_processes):
        process_id = i + 1  # Unique process ID
        arrival_time = input_entity(f'arrival time of process {process_id}', 0, 10)  # Arrival time
        execution_time = input_entity(f'execution time of process {process_id}', 1, 10)  # Execution time
        processes.append(Process(process_id, arrival_time, execution_time, execution_time))  # Add process to the list

    # Input quantum size for round-robin scheduling.
    quantum_size = input_entity("quantum size", 1, 3)
    quantum_size = 2  # Set quantum size to 2
    print({"quantum_size": quantum_size}, '\n')

    ready_queue = []  # Queue to hold ready processes
    running_queue = []  # Queue to hold currently running process
    time_passed = 0  # Track the total time passed

    # Function to move processes to the ready queue if they have arrived.
    def put_processes_in_ready_queue(processes):
        for i in range(len(processes)):
            process = processes[i]
            if process.arrival_time <= time_passed and not process.is_arrived:
                process.is_arrived = True  # Mark process as arrived
                ready_queue.append(process)  # Add process to the ready queue

    # Initially, put arrived processes in the ready queue.
    put_processes_in_ready_queue(processes)

    # Loop until all processes are completed.
    while check_is_execution_completed(processes):
        if len(ready_queue) > 0:
            # Check if the first process in the ready queue can be executed.
            if time_passed >= ready_queue[0].arrival_time:
                ready_process = ready_queue.pop(0)  # Get the process from the ready queue
                if not ready_process.is_ready:
                    ready_process.set_response_time(time_passed)  # Set the response time for the process
                    ready_process.is_ready = True  # Mark process as ready
                running_queue.append(ready_process)  # Add process to the running queue

            # If there is a process in the running queue, execute it.
            if len(running_queue) > 0:
                time_quanta = 0
                while time_quanta < quantum_size:
                    time_passed += 1  # Increment time passed
                    time_quanta += 1  # Increment time quanta
                    running_queue[0].decrement_time_left()  # Reduce the remaining time of the process
                    if running_queue[0].time_left == 0:
                        break
                ran_process = running_queue.pop(0)  # Remove the executed process
                print_process_table([ran_process])  # Print the process details
                put_processes_in_ready_queue(processes)  # Check for more processes to add to the ready queue
                if ran_process.time_left > 0:
                    ready_queue.append(ran_process)  # Re-add the process if not finished
                else:
                    # Set process completion time and calculate times
                    ran_process.set_completion_time(time_passed)
                    ran_process.set_turn_around_time()
                    ran_process.set_wait_time()
            else:
                time_passed += 1  # If no process in the running queue, increment time
                put_processes_in_ready_queue(processes)
        else:
            time_passed += 1  # If no process in the ready queue, increment time
            put_processes_in_ready_queue(processes)

    # Final output of all processes after execution.
    print("Final Process List")
    print_process_table(processes)
