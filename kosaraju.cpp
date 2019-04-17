/*

Written by Lukasz Komza

kosaraju.cpp implements Kosaraju's Algorithm to find strong components in
a given digraph G, then outputs the component graph of G, i.e., the DAG
whose vertices are in a 1-1 correspondence with the strong components of G.

Input Format:
n e
i_0 j_0
…
i_e-1 j_e-1

Output Format:
nsc
n_0 i_00 i_01 … i_0,n_0
…
n_nsc-1 i_k0 … i_k,n_nsc-1 (where k = nsc-1)
ne
p_0 q_0
…
p_ne-1 q_ne-1

Where:
n = # of vertices in G
e = # of arcs in G
nsc = # of strong components in G
ne = # of arcs in the G’s component DAG
i_kj = index of vertex in the kth component of G
p_i and q_i define an arc in G’s component DAG

*/
using namespace std;
#include <iostream>
#include <vector>
#include <fstream>
#include <stack>
#include <set>

struct Graph {

	int n; // number of vertices
	vector<vector<int>>print;
	vector<vector<int>>a; // vector of adjacency lists
	vector<int>c; // vector for component labeling

	Graph(int m){ // make a graph of size m
        a = vector<vector<int>>(m);
        c = vector<int>(m);
        n = m;
	}
	void addEdge(int v1, int v2){ // add an edge to the graph
        a[v1].push_back(v2);
	}

	void order(int v, stack<int>&Stack, vector<bool>&seen){
        seen[v] = true; // current vertex is seen
        // recurse over adjacent vertices
        for(int i=0; i<a[v].size(); ++i){
            if(!seen[a[v][i]])
                order(a[v][i], Stack, seen);
        }
        Stack.push(v); // v is pushed after all neighbors are
	}

	void printDFS(int v, vector<bool>&seen, int numSC){ // print utility version of order()
        seen[v] = true;
        c[v]=numSC; // number the vertex by its SCC
        print[numSC].push_back(v);
        for(int i=0; i<a[v].size(); ++i){
            if(!seen[a[v][i]])
                printDFS(a[v][i], seen, numSC);
        }
    }

	Graph invertGraph(){ // returns the inverse of the graph
        Graph inverse(n);
        for (int i=0; i<n; ++i){
            for(int j=0; j<a[i].size(); ++j)
                inverse.addEdge(a[i][j], i); // adds the opposite edge to the new graph
        }
        return inverse;
	}

	void kosaraju(){ // implementation of kosaraju's algorithm
        stack<int>Stack;
        vector<bool>seen(n);
        for(int i=0; i<n; ++i)
            seen[i] = false; // all vertices initially unseen

        // add vertices to stack by post order (first DFS)
        for(int i=0; i<n; ++i)
            if(!seen[i])
                order(i, Stack, seen);

        Graph inverse = invertGraph();

        for(int i=0; i<n; ++i)
            seen[i]=false; // reset seen list

        // second DFS
        int numSC=0;


        while(!Stack.empty()){
            int v = Stack.top();
            Stack.pop();
            if (!seen[v]){
                inverse.print.push_back({});
                inverse.printDFS(v, seen, numSC); // print the SCC found through DFS
                numSC++; // increment the SCC counter
            }

        }
        set<pair<int,int>>edges;
        for(int i=0; i<n; ++i){
            for(int j=0; j<a[i].size(); ++j){
                if(inverse.c[i]!=inverse.c[a[i][j]]){
                    edges.insert(pair<int,int>(inverse.c[i],inverse.c[a[i][j]]));
                }
            }
        }
        cout<<inverse.print.size()<<"\n";
        for(int i=0; i<inverse.print.size(); ++i){
            cout<<inverse.print[i].size()<<" ";
            for(int j=0; j<inverse.print[i].size(); j++){
                cout<<inverse.print[i][j]<<" ";
            }
            cout<<"\n";
        }
        cout<<edges.size();
        for(auto i=edges.begin(); i!=edges.end(); ++i)
            cout<<"\n"<<(*i).first<<" "<<(*i).second;
	}
};

int main() {

    int n;
    int e;
	cin>>n>>e;
    Graph g(n);
	for (int i=0; i<e; ++i){
        int t1=0;
        int t2=0;
        cin>>t1>>t2;
        g.addEdge(t1,t2);
	}
    g.kosaraju();
}
