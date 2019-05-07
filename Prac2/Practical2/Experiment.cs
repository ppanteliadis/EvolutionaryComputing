using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace Practical2 {
    public class Experiment {
        private int _k, _n, _bestFitness;
        private Graph _graph;
        private Assignment[] _population;
        Random rnd = new Random();

        public Experiment() {
            
        }

        public Experiment(int colors, int populationSize, string path, int count) {
            _k = colors;
            _n = populationSize;
            _graph = new Graph(path, count);
            GenerateStartingPopulation(count);
            _bestFitness = int.MaxValue;
        }

        private void GenerateStartingPopulation(int count) {
            _population = new Assignment[_n];
            // Initialize the population
            for (int i = 0; i < _n; ++i) {
                _population[i] = new Assignment(count, _k);
            }

            // Since every assignment is independent, generate them in parallel
            foreach(Assignment assignment in _population)
            {
                for (int i = 0; i < count; i++)
                {
                    assignment.Colors[i] = rnd.Next(0, _k);
                }
                VDLS(assignment);
            }
        }

        // Implementation of the Local Search for GraphColoring as per slide 10/46 Metaheuristic.pdf
        // Vertex Descent Local Search for Graph Coloring
        public void VDLS(Assignment assignment) {
            bool improved;
            do {
                improved = false;
                // Randomly iterate over the vertices
                foreach (int i in Enumerable.Range(0, _graph.GetSize()).OrderBy(x => rnd.Next())) {
                    Node node = _graph.Nodes[i];

                    // Initialize the current color
                    int minConflicts = 0;
                    int minColor = assignment.GetColor(node);
                    foreach (Node neighbour in node.Neighbours) {
                        if (assignment.GetColor(neighbour) == minColor) {
                            minConflicts++;
                        }
                    }

                    if (minConflicts == 0) {
                        continue;
                    }

                    // Randomly iterate over the colors
                    foreach (int k in Enumerable.Range(0, _k).OrderBy(x => rnd.Next())) {
                        if (assignment.GetColor(node) == k) {
                            continue;
                        }

                        // Count the amount of conflicts of the new color and compare
                        int conflicts = 0;
                        foreach (Node neighbour in node.Neighbours) {
                            if (assignment.GetColor(neighbour) == k) {
                                conflicts++;
                            }
                        }

                        if (conflicts < minConflicts) {
                            minConflicts = conflicts;
                            minColor = k;
                            if (conflicts == 0) {
                                break;
                            }
                        }
                    }

                    // If there is a better color, an improvement was found
                    if (assignment.GetColor(node) != minColor) {
                        improved = true;
                        assignment.SetColor(node, minColor);
                    }
                }
            } while (improved);

            // Log the amount of conflicts
            int totalConflicts = (from node in _graph.Nodes
                from neighbour in node.Neighbours
                where assignment.GetColor(node) == assignment.GetColor(neighbour)
                select node).Count();
            assignment.Fitness = totalConflicts / 2;
            //Console.WriteLine(totalConflicts / 2 + " conflicts");
        }

        public bool Run(StreamWriter writer)
        {
            Console.WriteLine("=====================");
            writer.WriteLine("=====================");
            Console.WriteLine("K = " + _k);
            writer.WriteLine("K = " + _k);
            //Console.WriteLine("BestFitness\tSeconds\tGenerations");
            writer.WriteLine("BestFitness\tSeconds\tGenerations");
            _bestFitness = _population.Min(a => a.Fitness);
            int generation = 0;
            Stopwatch stopwatch = Stopwatch.StartNew();
            while (_bestFitness != 0 && generation < 1000)
            {
                Recombination();
                _bestFitness = _population.Min(a => a.Fitness);
                //Console.WriteLine(_bestFitness + "\t" + (stopwatch.ElapsedMilliseconds / 1000 + 1));
                writer.WriteLine(_bestFitness + "\t" + (stopwatch.ElapsedMilliseconds / 1000 + 1) + "\t" + generation);
                generation++;
            }

            stopwatch.Stop();
            Console.WriteLine(_bestFitness + " fitness, " + (stopwatch.ElapsedMilliseconds / 1000 + 1) + " seconds, " + generation + " generations");
            writer.WriteLine(_bestFitness + " fitness, " + (stopwatch.ElapsedMilliseconds / 1000 + 1) + " seconds, " + generation + " generations");
            //Console.WriteLine("=====================");
            writer.WriteLine("=====================");
            return _bestFitness == 0;
        }

        public void Recombination()
        {
            _population = _population.OrderBy(x => rnd.Next()).ToArray();
            for (int i = 0; i < _n; i += 2)
            {
                Assignment p1 = _population[i];
                Assignment p2 = _population[i + 1];
                GPX(p1, p2, out Assignment child);
                VDLS(child);
                if (p1.Fitness > p2.Fitness)
                {
                    if(child.Fitness <= p1.Fitness)
                    {
                        _population[i] = child;
                    }
                }
                else
                {
                    if (child.Fitness <= p2.Fitness)
                    {
                        _population[i + 1] = child;
                    }
                }
            }
        }

        public void GPX(Assignment p1, Assignment p2, out Assignment child)
        {
            List<int>[] subsets1 = p1.GetSubsets();
            List<int>[] subsets2 = p2.GetSubsets();
            List<int>[] childSubsets = new List<int>[_k];

            for (int l = 0; l < _k; l++)
            {
                List<int>[] subsets = l % 2 == 0 ? subsets1 : subsets2;

                List<int> maxSubset = new List<int>(subsets[0]);
                foreach (List<int> subset in subsets)
                {
                    if(subset.Count > maxSubset.Count)
                    {
                        maxSubset = new List<int>(subset);
                    }
                }
                // TODO: Randomly break ties
                childSubsets[l] = new List<int>(maxSubset);
                foreach (List<int> subset in subsets1)
                {
                    subset.RemoveAll(c => maxSubset.Contains(c));
                }
                foreach (List<int> subset in subsets2)
                {
                    subset.RemoveAll(c => maxSubset.Contains(c));
                }
            }

            foreach (List<int> subset in subsets1)
            {
                foreach (int i in subset)
                {
                    childSubsets[rnd.Next(_k)].Add(i);
                }
            }

            child = new Assignment(_graph.GetSize(), _k, childSubsets);
        }
    }
}
