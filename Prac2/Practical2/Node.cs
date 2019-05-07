using System.Collections.Generic;

namespace Practical2 {
    public class Node {
        // Private member-variables
        public int Id;
        public List<Node> Neighbours;

        public Node(int id) {
            Id = id;
            Neighbours = new List<Node>();
        }
    }
}
