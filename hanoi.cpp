/*

Written by Lukasz Komza

hanoi.cpp finds the best-known solutions to the Towers of Hanoi
problem for up to 10 towers. Up to 10000 disks can be handled.

Each move is given as a two-integer VI describing the move as
moving a disk from one tower to another.

hanoi_init() uses dynamic programming to initialize the vectors n_hanoi
and k_hanoi, where n_hanoi[twr][dsks] is the minimum number of moves to
solve the problem with the number of towers and disks being twr and dsks
respectively, and k_hanoi gives the corresponding number of disks k that
should be moved to a spare tower first, to achieve the value in n_hanoi.

*/
using namespace std;
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <climits>
typedef vector<int> VI;
typedef vector<long long> VL;
vector<VL> n_hanoi (11, VL(10001));
vector<VI> k_hanoi (11, VI(10001));

void hanoi_init(){
    //base cases
    n_hanoi[2][1]=1;
    for(int d=0; d<=63; d++){ //non overflowing cases
        n_hanoi[3][d]=pow(2,d)-1;
        k_hanoi[3][d]=d-1;
    }
    for(int d=64; d<10001; d++){ //overflowing cases
        n_hanoi[3][d]=LLONG_MAX;
    }
    for(int t=4; t<11; t++){
        n_hanoi[t][1]=1;
        for(int d=2; d<10001; d++){
            long long minimum=LLONG_MAX;
            int best_k=0;
            for(int k=1;k<d;++k){
                if(!(n_hanoi[t][k] > (LLONG_MAX-n_hanoi[t-1][d-k])/2)){
                    if(minimum>(2*n_hanoi[t][k] + n_hanoi[t-1][d-k])){
                        minimum=(2*n_hanoi[t][k] + n_hanoi[t-1][d-k]);
                        best_k = k; //minimizes n_hanoi with k
                    }
                    else if(best_k)
                        break;
                }
            }
            k_hanoi[t][d] = best_k;
            n_hanoi[t][d]= minimum;
        }
    }
}

void hanoi(vector<VI>& moves, int n_twrs, int n_dsks, VI&aux){
    //base cases
    if(!n_dsks)
		return;
	if (n_twrs==2){
		moves.push_back({aux[0], aux[1]});
		return;
	}
	int k = k_hanoi[n_twrs][n_dsks];
	swap(aux[1], aux[n_twrs-1]);
	hanoi(moves, n_twrs, k, aux); //moves top k to furthest spare
	swap(aux[1], aux[n_twrs-1]);
	hanoi(moves, n_twrs-1, n_dsks-k, aux); //moves remaining disks to goal
	swap(aux[0], aux[n_twrs-1]);
	hanoi(moves, n_twrs, k, aux); //moves k from furthest spare to goal
	swap(aux[0], aux[n_twrs-1]); //restores aux[]
}
