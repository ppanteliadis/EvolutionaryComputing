import algorithm
import fitnesses
import crossovers
import threading
import logging
import logger
import sys

datadir = sys.argv[1]

length = 100

def run_experiment(fitness, crossover):
	logging.debug("Start " + fitness[1] + " " + crossover[1])
	size = 10
	# Keep doubling size until successful
	while True:
		if size > 1280:
			logging.debug("Abort")
			return
		logging.debug("Run " + str(size))
		successes, avg_generations, avg_evaluations, avg_time = algorithm.execute(fitness[0], crossover[0], size, length)
		logger.send(fitness[1], crossover[1], size, successes, avg_generations, avg_evaluations, avg_time)
		if successes >= 24:
			break
		else:
			size *= 2
	# Keep track of the low and high bound of the lowest reliable size and perform the bisection search
	low = int(size / 2)
	high = size
	while True:
		size = int((low + high) / 2)
		if size - low < 10:
			logging.debug("Done " + str(high))
			return
		logging.debug("Run " + str(size))
		successes, avg_generations, avg_evaluations, avg_time = algorithm.execute(fitness[0], crossover[0], size, length)
		logger.send(fitness[1], crossover[1], size, successes, avg_generations, avg_evaluations, avg_time)
		if successes >= 24:
			high = size
		else:
			low = size

logging.basicConfig(level = logging.DEBUG, format = "[%(levelname)s] (%(threadName)-10s) %(message)s", filename = datadir + "/run.log")
fitnesses.set_perm(length)

# Create and start the threads
threads = []
for fitness in fitnesses.get_all():
	for crossover in crossovers.get_all():
		thread = threading.Thread(target = run_experiment, args = (fitness, crossover))
		thread.start()
		threads.append(thread)

# Wait for all threads to finish
for thread in threads:
	thread.join()

# Run 2 experiments for the single data, one for each crossover function
data = algorithm.execute_single(fitnesses.counting, crossovers.two_point, 250, length)
logger.send_single("2-Point", data)
data = algorithm.execute_single(fitnesses.counting, crossovers.uniform, 250, length)
logger.send_single("Uniform", data)

logger.write(datadir)
