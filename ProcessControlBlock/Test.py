from texttable import Texttable


class Process:
    def __init__(self, process_id, arrival_time, burst_time, execution_time, resources_needed):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.time_left = execution_time
        self.resources_needed = resources_needed  
        self.resources_allocated = None  
        self.is_arrived = False
        self.is_ready = False
        self.completion_time = 0
        self.turn_around_time = 0
        self.wait_time = 0
        self.response_time = 0
        self.state = "new"  
        self.PSW = {"instruction_pointer": 0, "flags": {}}  

        
        self.IR = None  
        self.PC = 0 

    
    def allocate_resources(self, resources_available):
        """Allocate resources to the process if available."""
        if self.resources_needed <= resources_available:
            self.resources_allocated = self.resources_needed
            return True
        return False

    
    def release_resources(self):
        """Release the resources when the process completes."""
        resources_released = self.resources_allocated
        self.resources_allocated = None
        return resources_released

    
    def decrement_time_left(self):
        self.time_left -= 1
        
        self.PC = self.PSW["instruction_pointer"]
        self.IR = f"Executing instruction at {self.PC}" 
        self.PSW["instruction_pointer"] += 1  

    
    def set_completion_time(self, time_passed):
        self.completion_time = time_passed

    def set_turn_around_time(self):
        self.turn_around_time = self.completion_time - self.arrival_time

    def set_wait_time(self):
        self.wait_time = self.turn_around_time - self.burst_time

    def set_response_time(self, time_passed):
        self.response_time = time_passed - self.arrival_time


def input_entity(entity: str, min: int, max: int):
    while True:
        number_of_entities = int(input(f'Enter the {entity} (min: {min}, max: {max}):- '))
        if min <= number_of_entities <= max:
            return number_of_entities

def check_is_execution_completed(process_list):
    for process in process_list:
        if process.time_left > 0:
            return True
    return False

def print_process_table(process_list):
    table = Texttable()
    
    table_rows = [["process_id", "arrival_time", "burst_time", "completion_time", "turn_around_time", "wait_time", "response_time", "PSW", "State", "IR", "PC"]]
    for process in process_list:
        new_row = [
            process.process_id, process.arrival_time, process.burst_time, process.completion_time, 
            process.turn_around_time, process.wait_time, process.response_time, 
            process.PSW["instruction_pointer"], process.state, process.IR, process.PC
        ]
        table_rows.append(new_row)
    table.add_rows(table_rows)
    table.set_max_width(200)
    print(table.draw())

resources_available = 10 

def allocate_resources_to_ready_processes(ready_queue):
    """Allocate resources to processes in the ready queue if resources are available."""
    global resources_available
    for process in ready_queue:
        if not process.resources_allocated:
            if process.allocate_resources(resources_available):
                resources_available -= process.resources_needed  
                process.state = "ready"  

def release_resources_from_completed_process(process):
    """Release resources when the process is completed."""
    global resources_available
    resources_available += process.release_resources() 
    process.state = "terminated"

if __name__ == "__main__":
    
    number_of_processes = input_entity("number of processes", 3, 5)

    processes = []
    for i in range(number_of_processes):
        process_id = i + 1
        arrival_time = input_entity(f'Arrival time of process {process_id}', 0, 10)
        execution_time = input_entity(f'Execution time of process {process_id}', 1, 10)
        resources_needed = input_entity(f'Resources needed for process {process_id}', 1, 5) 
        processes.append(Process(process_id, arrival_time, execution_time, execution_time, resources_needed))

   
    quantum_size = input_entity("quantum size", 1, 3)

    ready_queue = []
    running_queue = []
    time_passed = 0

    def put_processes_in_ready_queue(processes):
        for process in processes:
            if process.arrival_time <= time_passed and not process.is_arrived:
                process.is_arrived = True
                ready_queue.append(process)

    put_processes_in_ready_queue(processes)

    while check_is_execution_completed(processes):
        if len(ready_queue) > 0:
            allocate_resources_to_ready_processes(ready_queue)  

            if len(ready_queue) > 0 and ready_queue[0].resources_allocated:
                ready_process = ready_queue.pop(0)
                if not ready_process.is_ready:
                    ready_process.set_response_time(time_passed)
                    ready_process.is_ready = True
                running_queue.append(ready_process)
                ready_process.state = "running"  


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
                    ran_process.state = "waiting"  
                else:
                    ran_process.set_completion_time(time_passed)
                    ran_process.set_turn_around_time()
                    ran_process.set_wait_time()
                    release_resources_from_completed_process(ran_process)  

            else:
                time_passed += 1 
                put_processes_in_ready_queue(processes)

        else:
            time_passed += 1  
            put_processes_in_ready_queue(processes)

    print("Final Process List")
    print_process_table(processes)
