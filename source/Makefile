CXX = g++

SRC = main.cpp
SRC += Random.cpp

CXXFLAGS = -std=c++11

INC = -I/usr/include/python3.8/
INC += -I/home/triston/.local/lib/python3.8/site-packages/numpy/core/include/
INC += -lpython3.8

TARG = randomplot

randomplot:
	$(CXX) $(SRC) $(CXXFLAGS) $(INC) -o $(TARG)

clean:
	rm -f *.o randomplot data.txt
