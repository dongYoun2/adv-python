import math
from threading import Thread
from multiprocessing import Pool


def partial_integral(x, start, end, steps, result, idx):
    dt = (end - start) / steps
    t = start + dt
    s = 0.0

    for _ in range(steps):
        s += (t ** (x - 1)) * math.exp(-t) * dt
        t += dt

    result[idx] = s  # store result


def gamma_threading(x, bound_1, bound_2, total_steps, N=4):
    threads = []
    results = [0.0] * N

    chunk_size = (bound_2 - bound_1) / N
    steps_per_chunk = total_steps // N

    for i in range(N):
        start = bound_1 + i * chunk_size
        end = start + chunk_size

        t = Thread(target=partial_integral,
                   args=(x, start, end, steps_per_chunk, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)


def partial_integral_mp(args):
    x, start, end, steps = args
    
    dt = (end - start) / steps
    t = start + dt
    s = 0.0

    for _ in range(steps):
        s += (t ** (x - 1)) * math.exp(-t) * dt
        t += dt

    return s


def gamma_multiprocessing(x, bound_1, bound_2, total_steps, N=4):
    chunk_size = (bound_2 - bound_1) / N
    steps_per_chunk = total_steps // N

    args = []
    for i in range(N):
        start = bound_1 + i * chunk_size
        end = start + chunk_size
        args.append((x, start, end, steps_per_chunk))

    with Pool(N) as p:
        results = p.map(partial_integral_mp, args)

    return sum(results)