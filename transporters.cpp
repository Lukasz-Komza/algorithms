/*

Written by Lukasz Komza

transporters.cpp finds the minimum number of "transporters"
that need to be installed in a "space station" represented
by a graph, such that if any node in the graph was removed,
all nodes could still be connected to a transporter.

This problem is equivalent to finding the number of leafs
in the subgraph of biconnected components, which is the
implemented solution below.

int transporters(int n, VI& tubes){} returns the minimum number
of transporters required, where n is the number of nodes and
tubes[2*i] and tubes[2*i+1] indicates nodes forming an edge.

*/
using namespace std;
#include <vector>
#include <stack>
#include <utility>
typedef vector<int> VI;
VI pre_num;
VI low_num;
int transporters_num;
int ind;
vector<bool> art_pt;
int root_issue;

struct Graph{
    int n;
    vector<VI>adj_list;
    Graph(int n){
        this->n = n;
        for(int i=0; i<n; ++i)
            adj_list.push_back({});
    }
    void addEdge(int v, int w){
        adj_list[v].push_back(w);
        adj_list[w].push_back(v);
    }
    bool DFS(int v, int u){
        ind++;
        bool art_branch = true;
        bool art_root = false;
        pre_num[v] = ind;
        low_num[v] = ind;
        for(int i=0; i<adj_list[v].size(); ++i){
            int w = adj_list[v][i];
            if(pre_num[w]==0) {
                bool leaf = DFS(w, v);
                art_branch = art_branch&&leaf;
                low_num[v] = min(low_num[w],low_num[v]);
                art_pt[v] = art_pt[v] || low_num[w] >= pre_num[v];
                if(low_num[w]>=pre_num[v]&&leaf)
                    transporters_num++;
            }
            else if(pre_num[w]<pre_num[v]&&w!=u)
                low_num[v] = min(pre_num[w],low_num[v]);
            if(art_pt[v]&&low_num[w]==1)
                art_root = true;
        }
        if(art_pt[v]&&(low_num[v]==1||low_num[v]==2)){
            for(int i=0; i<adj_list[v].size(); ++i){
                int w = adj_list[v][i];
                if(low_num[w]==1){
                    art_root = true;
                    break;
                }
            }
        }
        if(art_root)
            root_issue++;
        art_branch = art_branch&&!art_pt[v];
        return art_branch;
    }
    void DFS(){
        pre_num[0] = 1;
        low_num[0] = 1;
        bool first_adj = false;
        int num_adj = 0;
        for(int i=0; i<adj_list[0].size(); ++i){
            int w = adj_list[0][i];
            if(pre_num[w]==0){
                num_adj++;
                if(num_adj==2){
                    root_issue++;
                    art_pt[0] = true;
                    if(first_adj)
                        transporters_num++;
                }
                bool leaf = DFS(w, 0);
                if(art_pt[0]&&leaf)
                    transporters_num++;
                if(num_adj==1)
                    first_adj = leaf;
            }
        }
    }
};
int transporters(int n, vector<int>& tubes) {
    pre_num = vector<int>(n);
    low_num = vector<int>(n);
    art_pt = vector<bool>(n, false);
    ind = 1;
    root_issue = 0;
    transporters_num = 0;

    Graph g(n);
    for(int i=0; i<tubes.size()/2; ++i)
        g.addEdge(tubes[2*i], tubes[2*i+1]);

    g.DFS();

    if(!root_issue)
        return 2;
    if(root_issue==1&&!art_pt[0])
        transporters_num++;
    return transporters_num;
}
