# Makefile for C++ benchmarks

CXX = g++
CXXFLAGS = -O3 -std=c++17 -Wall

all: fibonacci factorial sum

fibonacci: fibonacci.cpp
	$(CXX) $(CXXFLAGS) -o fibonacci fibonacci.cpp

factorial: factorial.cpp
	$(CXX) $(CXXFLAGS) -o factorial factorial.cpp

sum: sum.cpp
	$(CXX) $(CXXFLAGS) -o sum sum.cpp

clean:
	rm -f fibonacci factorial sum

.PHONY: all clean

