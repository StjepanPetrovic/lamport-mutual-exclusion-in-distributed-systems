import sys

from WorkerProcess import WorkerProcess


def read_input_arguments():
    times = []
    temp_array = []
    last_arg = None

    for arg in sys.argv[1:]:
        last_arg = arg

        if arg == '@':
            times.append(temp_array)
            temp_array = []
        else:
            temp_array.append(int(arg))

    if temp_array:
        times.append(temp_array)

    if last_arg == '@':
        times.append([])

    return times


def read_times_to_critical_section(input_times):
    output_times = []

    for j in range(1, len(input_times)):
        output_times.append(input_times[j])

    return output_times


if __name__ == "__main__":

    process_times = read_input_arguments()
    initial_clock_times = process_times[0]

    initial_clock_times[0] = 8

    times_to_critical_section = read_times_to_critical_section(process_times)

    processes = []

    for i, process_init_value in enumerate(initial_clock_times):

        processes.append(
            WorkerProcess(
                id_process=i + 1,
                clock=process_init_value,
                times_to_critical_section=times_to_critical_section[i],
                number_of_other_processes=len(initial_clock_times) - 1,
            )
        )

    for process in processes:
        process.join()
