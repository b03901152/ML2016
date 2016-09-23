#include <iostream>
#include <iomanip>
#include <algorithm>
#include <cstdio>
#include <ctype.h>
#include <cassert>
#include <cstring>
#include <vector>

#include <fstream>
#include <sstream>

using namespace std;

int main(int argc, char* argv[])
{
	stringstream stmp;
	stmp << argv[1];
	int index;
	stmp >> index;
	ifstream ifs;
	ifs.open(argv[2],ifstream::in);
	string s;
	double d;
	vector<double> r;
	while(getline(ifs,s))
	{
		stringstream ss;
		ss << s;
		int counter=0;
		while(ss.good())
		{
			ss >> d;
			if(counter==index)
				{
					r.push_back(d);
					break;
				}
			counter++;
		}
	}
	sort(r.begin(),r.end());

	ofstream ofs ("ans1.txt", ofstream::out);
	for(int i=0; i<r.size(); ++i)
		{
			ofs << r[i] << ',' ; 
		}

}



