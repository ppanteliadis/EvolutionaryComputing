using System.Collections.Generic;

namespace Practical2
{
    public class Assignment {
        public int[] Colors;
        public int Fitness;
        private int _colorCount;

        public Assignment(int count, int colorCount, List<int>[] subsets = null) {
            Colors = new int[count];
            _colorCount = colorCount;
            if(subsets == null)
            {
                return;
            }

            int k = 0;
            for(int i = 0; i < colorCount; i++)
            {
                foreach(int j in subsets[i])
                {
                    Colors[j] = i;
                    k++;
                }
            }
        }

        public int GetColor(Node node)
        {
            return Colors[node.Id];
        }

        public void SetColor(Node node, int color)
        {
            Colors[node.Id] = color;
        }

        public List<int>[] GetSubsets()
        {
            List<int>[] subsets = new List<int>[_colorCount];
            for(int i = 0; i < _colorCount; i++)
            {
                subsets[i] = new List<int>();
            }
            for(int i = 0; i < Colors.Length; i++)
            {
                subsets[Colors[i]].Add(i);
            }
            return subsets;
        }
    }
}
