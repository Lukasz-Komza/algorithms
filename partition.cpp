/*

Written by Lukasz Komza

partition.cpp consists of several functions involving integer partitions.

part_q(n) finds how many unrestricted partitions of n exist.
part_k(n, k) finds the kth partition of n
part_i(p) finds the index of a partition p

This code can handle n values up to but not including 417

*/
using namespace std;
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
typedef unsigned long long ULL;
typedef vector<int> VI;
vector<vector<ULL>>h(417, vector<ULL>(417)); //global variable keeping track of part_q values

ULL part_q(int n, int k){ //helper of part_q, can take in k
    if(k>n)
        return 0;
    if(k==1)
        return 1; //base cases
    if(h[n][k]) //checks if call has been made before
        return h[n][k]; //returns known value
    h[n][k] = part_q(n-k, k)+part_q(n-1, k-1); //fills in h
    return h[n][k];
}
ULL part_q(int n){ //how many unrestricted partitions of n exist?
    ULL s = 0;
    for(int k = 1; k != n+1; ++k)
        s += part_q(n, k); //unrestricted partitions are a sum of restricted partitions
    return s;
}
VI part_k(int n, ULL k){ //what is the kth partition of n?
	ULL s = -1; //counting starts at 0
	VI p;
	int t=n;
	int l=n;
	while(t){ //while unaccounted part of the sum exists
		for(int i=l; i>0; --i){ //search
			ULL j = part_q(t, i);
			if(j+s>=k){
				p.push_back(i); //adds integer to the partition
				t-=i; //accounts for k in t
				l=min(i, t);
				break; //go back to while, start search over
			}
			s+=j; //increment by num of parts
		}
	}
	return p;
}
ULL part_i(const VI &p){ //what is the index of partition p of n?
    ULL s = 0;
	int t = accumulate(p.begin(), p.end(), 0); //finds number n, sets to t and l
	int l = t;
	for(int i=0; i<p.size(); ++i){ //for each part:
        for(int k=l; k!=p[i]; --k)
            s+=part_q(t, k); //increment sum by partitions before it
        t-=p[i]; //accounts for parts in t
        l=min(p[i], t);
	}
	return s;
}
