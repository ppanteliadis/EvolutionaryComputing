using System.IO;

namespace Practical2 {
    public class Graph {
        public Node[] Nodes;

        // Read a space delimited file with 2 columns. Assuming the first column is a vertex
        // and the second column, the vertex it connects to.
        public Graph(string path, int count) {
            Nodes = new Node[count];
            generateGraph(path);
        }

        private void generateGraph(string path) {
            for (int i = 0; i < Nodes.Length; i++) {
                Nodes[i] = new Node(i);
            }

            using (StreamReader sr = new StreamReader(path)) {
                while (!sr.EndOfStream) {
                    string[] line = sr.ReadLine().Split(' ');

                    int id1 = int.Parse(line[0].Trim()) - 1;
                    int id2 = int.Parse(line[1].Trim()) - 1;

                    Nodes[id1].Neighbours.Add(Nodes[id2]);
                    Nodes[id2].Neighbours.Add(Nodes[id1]);
                }
            }
        }

        public int GetSize() {
            return Nodes.Length;
        }
    }
}
