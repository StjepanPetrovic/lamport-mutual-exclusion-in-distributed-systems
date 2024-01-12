import sys

from WorkerProcess import WorkerProcess

if __name__ == "__main__":

    base_port = 8000

    numbers = []
    temp = []
    last_arg = None

    for arg in sys.argv[1:]:
        last_arg = arg

        if arg == '@':
            numbers.append(temp)
            temp = []
        else:
            temp.append(int(arg))

    if temp:
        numbers.append(temp)

    if last_arg == '@':
        numbers.append([])

    processes = []

    for i, process_init_value in enumerate(numbers[0]):
        processes.append(WorkerProcess(base_port + i, numbers[0][i], numbers[i + 1]))

    for process in processes:
        process.join()
