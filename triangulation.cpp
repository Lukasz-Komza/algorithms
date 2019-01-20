/*

Written by Lukasz Komza

triangulation.cpp finds the optimal triangulation of a convex polygon
with n sides where the cost of such a triangulation is the sum of the
Euclidean lengths of the diagonals.

An O(n^3) solution is implemented through dynamic programming.

Input File Format:
n
x_1 y_1
…
x_n y_n

Output File Format:
cost
i_1 j_1
…
i_(n-3) j_(n-3)

*/
#include <vector>
#include <fstream>
#include <cmath>
using namespace std;

struct Point{
    double x, y;
};
double dist(const vector<Point>points, int i, int j) {
	return sqrt(pow((points[i].x - points[j].x),2)+pow((points[i].y - points[j].y),2));
} //distance between points

void triangulate(const vector<Point>points, int n){
    vector<vector<vector<Point>>>d; //diagonal storage
	vector<vector<double>>c; //cost storage corresponding to diagonals by index
	for (int i=0; i<n-2; ++i) {
		d.push_back(vector<vector<Point>>(n-i-2));
        c.push_back(vector<double>(n-i-2));
	} //storing information
	for (int i=1; i<n-2; ++i) {
		for (int j=0; j<n-i-2; ++j) { //iterate over vertices
			int ind = -1;
			double m = c[i-1][j+1]+dist(points, j+1, i+j+2); //base
			for (int k=0; k<i-1; ++k) { //find optimal k
				double t = c[k][j]+dist(points, j+k+2, i+j+2) + c[i-k-2][j+k+2]+dist(points, j, j+k+2);
				//divide into a triangle and two convex polygons
				if (t<m) { //find min cost
					ind = k; //keep track of index
					m = t;
				}
			}
			double t = c[i-1][j]+dist(points, j, i+j+1);
            if(ind==-1){ //nothing yet
                d[i][j].push_back(Point{j+1, i+j+2});
				d[i][j].insert(d[i][j].end(), d[i-1][j+1].begin(), d[i-1][j+1].end());}
            else if (t<m) { //copy existing diagonal
				d[i][j].insert(d[i][j].end(), d[i-1][j].begin(), d[i-1][j].end());
				m = t;} //adjust min
			else { //draw two diagonals
				d[i][j].insert(d[i][j].end(), d[ind][j].begin(), d[ind][j].end());
				d[i][j].push_back(Point{j, ind+j+2}); //first vert
				d[i][j].push_back(Point{ind+j+2, i+j+2}); //second vert
				d[i][j].insert(d[i][j].end(), d[i-ind-2][ind+j+2].begin(), d[i-ind-2][ind+j+2].end());}
            c[i][j]=m; //set the cost to min found
		}
	}
    ofstream out; //output
	out.open("out.txt");
    out.precision(7); //7 sigfigs
	out<<c[n-3][0]<<"\n"; //optimal cost
	for (int i=0; i<n-3; ++i) //diagonals w/ cost
		out<<d[n-3][0][i].x<<" "<<d[n-3][0][i].y<<"\n";
	out.close();
}
int main() {
	ifstream in("in.txt"); //input
    int n;
	in>>n; //size
	vector<Point>points(n);
	for (int i=0; i<n; ++i)
		in>>points[i].x>>points[i].y;
    //file input
    triangulate(points, n);
}
