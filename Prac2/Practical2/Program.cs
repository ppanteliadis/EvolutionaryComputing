using System;
using System.IO;

namespace Practical2 {
    class Program {
        static void Main(string[] args) {
<<<<<<< Updated upstream
            for (int i = 0; i < 5; i++) {
                StreamWriter writer = new StreamWriter("results/le450_15c.col_" + i + ".log");
                for (int K = 18; K > 14; K--)
                {
                    Experiment experiment = new Experiment(K, 100, "data/le450_15c.col2", 450);
                    bool result = experiment.Run(writer);
                    if (!result)
                    {
                        break;
                    }
=======
            /*
            for (int K = 18; K > 0; K--){
                Experiment experiment = new Experiment(K, 100, "data/le450_15c.col2", 450);
                experiment.Run();
            }*/

            StreamWriter writer = new StreamWriter("results/log.log");
            for (int K = 30; K > 0; K--)
            {
                Experiment experiment = new Experiment(K, 100, "data/dsjc250.5.col2", 250);
                bool result = experiment.Run(writer);
                if (!result) {
                    break;
>>>>>>> Stashed changes
                }
                writer.Close();
            }
            Console.ReadKey();
        }
    }
}
