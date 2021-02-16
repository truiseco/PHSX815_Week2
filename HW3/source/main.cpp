/*************************************************************
* @author   Triston Ruiseco
* @file     main.cpp
* @date     02/08/2021
* @brief    Program to randomly generate and plot a set of numbers.
*************************************************************/

#include <fstream>
#include "Random.h"
#include "matplotlibcpp.h"


namespace plt = matplotlibcpp;

int main(int argc, char* argv[]){
  bool printhelp = 0;
  long seed = 133742069;

  int Ncat = 6;

  int Nselect = 1;

  int Nexp = 1;

  bool doOutputFile = false;
  std::string OutputFileName;

  // parse user's command line args
  for(int i = 0; i < argc; i++){
    if(strncmp(argv[i],"--help", 6) == 0){
      printhelp = true;
    }
    if(strncmp(argv[i],"-h", 2) == 0){
      printhelp = true;
    }
    if(strncmp(argv[i],"-seed", 5) == 0){
      i++;
      seed = std::stol(argv[i]);
    }
    if(strncmp(argv[i], "-Ncat", 5) == 0){
      i++;
      int cat = std::stoi(argv[i]);
      if(cat > 2){
        Ncat = cat;
      }
    }
    if(strncmp(argv[i], "-Nselect", 8) ==0){
      i++;
      int select = std::stoi(argv[i]);
      if(select > 0){
        Nselect = select;
      }
    }
    if(strncmp(argv[i], "-Nexp", 5) == 0){
      i++;
      int Ne = std::stoi(argv[i]);
      if(Ne > 0){
	       Nexp = Ne;
      }
    }
    if(strncmp(argv[i],"-output", 7) == 0){
      i++;
      OutputFileName = std::string(argv[i]);
      doOutputFile = true;
    }
  }

  // print flags if requested
  if(printhelp){
    std::cout << "Usage: " << argv[0] << " [options]" << "\n";
    std::cout << "  options:" << "\n";
    std::cout << "   --help(-h)          print options" << "\n";
    std::cout << "   -seed [number]      random seed to use" << "\n";
    std::cout << "   -Ncat [number]      number of categories" << "\n";
    std::cout << "   -Nselect [number]   number of category selections per experiment" << "\n";
    std::cout << "   -Nexp [number]      number of experiments" << "\n";
    std::cout << "   -output [filename]  name of ouptut file" << "\n";

    return 0;
  }

  // declare an instance of our Random class
  Random  random(seed);

  int temp = 0;
  std::vector<double> data;

  /* record exeperiment data into vector and output space-delimited data and
     line-delimited experiments data file or stdout */
  if(doOutputFile){
    std::ofstream outFile;
    outFile.open(OutputFileName);
    for(int e = 0; e < Nexp; e++){
      for(int s = 0; s < Nselect; s++){
        data.push_back(random.Categorical(Ncat));
        outFile << data.back() << " ";
      }
      outFile << "\n";
    }
    outFile.close();
  } else{
    for(int e = 0; e < Nexp; e++){
      for(int s = 0; s < Nselect; s++){
        data.push_back(random.Categorical(Ncat));
        std::cout << data.back() << " ";
      }
      std::cout << "\n";
    }
  }

  // configure and display figure, results of all experiments displayed together
  plt::hist(data, Ncat, "b");
  plt::title("Uniform Categorical Distribution");
  plt::xlabel("Category");
  plt::ylabel("Counts");

  plt::show();
  plt::savefig("HW3Plot.png");

  return 0;
}
