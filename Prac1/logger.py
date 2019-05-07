import csv

graphs = []
tables = {}
two_point_single = []
uniform_single = []

def send(fitness, crossover, size, successes, avg_generations, avg_evaluations, avg_time):
    # Record the sent data for the graphs and tables
    graphs.append((fitness, crossover, size, successes))
    # After a success, a higher size will never be tried, so when an experiment is successful, it is always the lowest size yet
    if successes >= 24:
        tables[fitness + crossover] = (fitness, crossover, size, avg_generations, avg_evaluations, avg_time)

def send_single(crossover, data):
    # Record the sent data for the single experiments
    if crossover == "2-Point":
        global two_point_single
        two_point_single = data
    elif crossover == "Uniform":
        global uniform_single
        uniform_single = data

def write(dir):
    # Insert the headers and write the data for the graphs, tables and singles to CSV files

    with open(dir + "/graphs.csv", "w", newline = "") as graphs_file:
        writer = csv.writer(graphs_file, delimiter = ";")
        writer.writerow(("Fitness Function", "Crossover Function", "Population Size", "Successes"))
        for row in graphs:
            writer.writerow(row)
    with open(dir + "/tables.csv", "w", newline = "") as tables_file:
        writer = csv.writer(tables_file, delimiter = ";")
        writer.writerow(("Fitness Function", "Crossover Function", "Population Size", "Average Generations", "Average Evaluations", "Average Time"))
        for row in tables.values():
            writer.writerow(row)
    graphs.insert(0, ("Fitness Function", "Crossover Function", "Population Size", "Successes"))
    with open("Data/2-point_single.csv", "w", newline = "") as single_file:
        writer = csv.writer(single_file, delimiter = ";")
        writer.writerow(("Proportion Ones", "Fitness Mean", "Fitness Standard Deviation", "Selection Error"))
        for row in two_point_single:
            writer.writerow(row)
    graphs.insert(0, ("Fitness Function", "Crossover Function", "Population Size", "Successes"))
    with open(dir + "/uniform_single.csv", "w", newline = "") as single_file:
        writer = csv.writer(single_file, delimiter = ";")
        writer.writerow(("Ones Proportion", "Fitness Mean", "Fitness Standard Deviation", "Selection Error"))
        for row in uniform_single:
            writer.writerow(row)
