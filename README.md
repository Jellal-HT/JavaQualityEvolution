# JavaQualityEvolution
A python script used to analyze architecture smells and design smell for Java programs. It uses [DesigniteJava Enterprise](http://www.designite-tools.com/designitejava) to analyze Java project and detect architecture and design smells. This script will create a csv file, which record the github repo name and the 
correspondidng amount of architecture and design smells.

## How to run
### Prerequisite and assumptions

1. download DesigniteJava Enterprise edition on your machine. You may download DesigniteJava Enterprise from [Designite website](http://www.designite-tools.com/designitejava). 

2. set up git and python in your environment

3. download pandas

4. download the dataset file(dataset.csv) from [RepoRepear](https://reporeapers.github.io/results/1.html)

5. Create a folder any convenient location in your machine and move the DesigniteJava jar file, dataset.csv and the script(main.py) to the newly created folder.

6. run the script using python command
