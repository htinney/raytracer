import ray
ray.init()

def add1(a, b):
    return a + b

@ray.remote
def add2(a, b):
    return a + b

def test_add():
    print(ray.get([add2.remote(x, x+1) for x in range(10)]))

@ray.remote
def sub_experiment(i, j):
    # Run the jth sub-experiment for the ith experiment
    return i + j

@ray.remote
def run_experiment(i):
    sub_results = []
    # Launch tasks to perform 10 sub-experiments in parallel.
    for j in range(10):
        sub_results.append(sub_experiment.remote(i, j))
    return sum(ray.get(sub_results))

def test_run_experiment():
    results = [run_experiment.remote(i) for i in range(5)]
    print(ray.get(results))
