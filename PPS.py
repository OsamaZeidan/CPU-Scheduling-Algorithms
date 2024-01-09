# Preemptive Priority Scheduling with Aging
import math
# imports
import tkinter as tk
import Process

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

# burst times
burst_times = {}
for process in waiting_queue:
    burst_times[process.id] = process.burst_time

# priority
priority = {}
for process in waiting_queue:
    priority[process.id] = process.priority

# scheduling and execution process
while time <= period:
    # sort waiting queue according to arrival time
    waiting_queue.sort(key=lambda x: x.arrival_time)

    # add processes to the ready queue
    processes_to_remove = []
    for p in waiting_queue:
        if p.arrival_time <= time:
            # add the process to the ready queue
            p.time_in_ready_queue = 0
            ready_queue.append(p)
            # mark for removal
            processes_to_remove.append(p)
    # remove marked processes from waiting queue
    for p in processes_to_remove:
        waiting_queue.remove(p)

    # if ready queue is empty
    if len(ready_queue) == 0:
        # increase time
        time += 1
        continue

    # sort ready queue according to priority and arrival time -> (same priority -> FCFS)
    ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))

    # pop ready queue
    process = ready_queue.pop(0)

    process.exe_time = time
    # execute process
    time += 1
    if(time > period):
        break
    process.burst_time -= 1
    process.completion_time = time

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
    # Aging
    for x in ready_queue:
        x.time_in_ready_queue += 1
        if x.time_in_ready_queue >= age:
            x.priority -= (x.time_in_ready_queue // age)
            if x.priority < 0:
                x.priority = 0
            x.time_in_ready_queue %= age


    # if process is finished
    if process.burst_time == 0:
        num_of_processes += 1
        process.burst_time = burst_times[process.id]
        process.priority = priority[process.id]
        # update TAT
        TAT += process.completion_time - process.arrival_time
        # update WT
        WT += process.completion_time - process.arrival_time - process.burst_time
        process.arrival_time = time + process.comes_back_after
        waiting_queue.append(process)
    else:
        process.time_in_ready_queue = 0
        ready_queue.append(process)

    continue

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
