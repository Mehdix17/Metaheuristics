from modelisation.parser import parse_all_benchmarks

# Paths
EXPERIMENTATION_PATH = "results/experimentations/"
HISTORY_PATH = "results/history/"
BENCHMARKS_PATH = "benchmarks/"

ALGOS = ["Genetique", "DFS"]


# liste contenant les 25 benchmarks sous forme de tuple (subsets, m, n, k)
BENCHMARKS = parse_all_benchmarks(BENCHMARKS_PATH)
