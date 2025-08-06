import time

class DepthFirstSearch:
    def __init__(self, problem, limit):
        self.problem = problem
        self.best_solution = []
        self.best_fitness = 0
        self.limit = limit
        self.start_time = None
        self.subsets_indices = None

    def dfs(self, start=0, current_solution=[]):
        exec_time = time.time() - self.start_time
        if exec_time >= self.limit:
            return
        
        if len(current_solution) == self.problem.k:
            selected_subsets = [self.problem.subsets[i] for i in current_solution]
            covered_elements = set().union(*selected_subsets)
            fitness = len(covered_elements)
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_solution = current_solution
            return
        
        for i in range(start, len(self.subsets_indices)):
            self.dfs(i + 1, current_solution + [self.subsets_indices[i]])
    
    def run(self):
        self.start_time = time.time()
        self.subsets_indices = list(range(self.problem.m))
        self.dfs()
        exec_time = round(time.time() - self.start_time, 2)
        
        return self.best_solution, self.best_fitness, exec_time
