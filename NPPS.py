# Non-preemptive Priority Scheduling with Aging

# imports
import tkinter as tk
import Process
import math

# num of processes
num_of_processes = 0

# Aging
age = 5

# period of time
period = 200

# current time
time = 0

# Turn Around Time
TAT = 0

# Waiting Avg Time
WT = 0

# gantt chart
gantt_chart = []

# initiate processes
waiting_queue = []

waiting_queue.append(Process.Process(1, 0, 10, 2, 3))
waiting_queue.append(Process.Process(2, 1, 8, 4, 2))
waiting_queue.append(Process.Process(3, 3, 14, 6, 3))
waiting_queue.append(Process.Process(4, 4, 7, 8, 1))
waiting_queue.append(Process.Process(5, 6, 5, 3, 0))
waiting_queue.append(Process.Process(6, 7, 4, 6, 1))
waiting_queue.append(Process.Process(7, 8, 6, 9, 2))

# ready queue
ready_queue = []

process = None
current_process_burst_time = 0
# priority dict
priority_dict = {}
for p in waiting_queue:
    priority_dict[p.id] = p.priority
# scheduling and execution process
while time <= period:
    # sort waiting queue according to arrival time
    # waiting_queue.sort(key=lambda p: p.arrival_time)

    # add processes to the ready queue
    processes_to_remove = []
    for p in waiting_queue:
        if p.arrival_time <= time:
            p.time_in_ready_queue = 0
            p.first_time = True
            # add the process to the ready queue
            ready_queue.append(p)
            # mark for removal
            processes_to_remove.append(p)

    # remove marked processes from waiting queue
    for p in processes_to_remove:
        waiting_queue.remove(p)

    # Aging
    for x in ready_queue:
        x.time_in_ready_queue += current_process_burst_time
        if x.first_time and abs(x.time_in_ready_queue - x.arrival_time) >= age:

            x.priority = x.priority - abs(x.time_in_ready_queue - x.arrival_time) // age
            x.time_in_ready_queue = abs(x.time_in_ready_queue - x.arrival_time) % age
            x.first_time = False
        elif not x.first_time:
            x.priority -= x.time_in_ready_queue // age
            x.time_in_ready_queue = x.time_in_ready_queue % age
        if x.priority < 0:
            x.priority = 0

    # if ready queue is empty
    if len(ready_queue) == 0:
        # increase time
        continue

    # sort ready queue according to priority and arrival time -> (same priority -> FCFS)
    ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
    # pop ready queue
    process = ready_queue.pop(0)
    # update exe time
    process.exe_time = time
    # execute process
    time += process.burst_time
    # check time
    if(time > 200):
        break
    num_of_processes += 1
    current_process_burst_time = process.burst_time
    # update completion time
    process.completion_time = time
    # time in waiting
    process.time_in_ready_queue = 0

    # update TAT & WT
    TAT += process.completion_time - process.arrival_time
    WT += process.completion_time - process.arrival_time - process.burst_time
    # gantt chart
    gantt_chart.append(
        Process.Process(
            process.id,
            process.arrival_time,
            process.burst_time,
            process.comes_back_after,
            process.priority,
            process.completion_time,
            process.exe_time,
        )
    )
    # add the process to the waiting queue, after execution
    # update the arrival time of the process
    process.arrival_time = time + process.comes_back_after
    # priority
    process.priority = priority_dict[process.id]
    waiting_queue.append(process)

# WT, TAT
WT /= num_of_processes
TAT /= num_of_processes
print(
    f"Avg. Turn Around Time = {TAT} (Time Unit)\nAvg. Waiting Time = {WT} (Time Unit)"
)
print("Num. of Finished Processes:", num_of_processes)
for p in gantt_chart:
    print(f"P_{p.id}_CT_{p.completion_time}")


# gantt chart
def create_rectangles():
    rectangle_width = 180
    rectangle_height = 150
    color = "white"
    i = 0
    for p in gantt_chart:
        text = f"PID: {p.id}\nTime: {p.completion_time}\n"

        # Calculate rectangle coordinates
        x1 = i * (rectangle_width + 10) + 50
        y1 = 50
        x2 = x1 + rectangle_width
        y2 = y1 + rectangle_height

        # Draw the rectangle
        canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Display the associated text
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, fill="black")
        i += 1


# Create the main window
root = tk.Tk()
root.title("Gantt Chart")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack()


# Function to scroll left
def scroll_left(event):
    canvas.xview_scroll(-1, "units")


# Function to scroll right
def scroll_right(event):
    canvas.xview_scroll(1, "units")


# Bind the arrow keys
root.bind("<Left>", scroll_left)
root.bind("<Right>", scroll_right)

# Create the rectangles
create_rectangles()

# Start the main events loop
root.mainloop()
