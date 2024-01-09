class Process:
    # Constructor #
    def __init__(
        self,
        id,
        arrival_time,
        burst_time,
        comes_back_after,
        priority,
        completion_time=0,
        exe_time=0,
        time_in_ready_queue=0,
        first_time = True
    ):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.comes_back_after = comes_back_after
        self.priority = priority
        self.completion_time = completion_time
        self.exe_time = exe_time
        self.time_in_ready_queue = time_in_ready_queue
        self.first_time = first_time

    def __str__(self):
        return (
            "Process: "
            + str(self.id)
            + " Arrival Time: "
            + str(self.arrival_time)
            + " Burst Time: "
            + str(self.burst_time)
            + " Comes Back After: "
            + str(self.comes_back_after)
            + " Priority: "
            + str(self.priority)
            + " Completion Time: "
            + str(self.completion_time)
            + " Execution Time: "
            + str(self.exe_time)
            + ""
        )
