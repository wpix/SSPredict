# SSPredict: Solid-Solution Strengthening Prediction

A command line tool to plot solid solution strengthening stresses of a complex concentrated alloys (CCAs). The goal is to accelerate the discovery of high strength CCAs based on solid solution strengthening. It is designed to help visualize the solid solution strengthening stress regarding the combination of components and the vast composition space of CCAs. The formulations are based on an elasticity-based model for random solid solution alloys [ref.1].

## Getting Started
The tool is currently working with python3
Clone the tool to where you want to start the project:
```  
$ git clone https://github.com/DS-Wen/SSPredict.git .
```
#### Packages:
* matplotlib, coding version 1.13.3
* numpy, coding version 2.1.0
* pandas, coding version 0.23.4

## Using the tool

### Setup input file
[Here to see the input file setup and examples](/examples/input_guide.md)
### Command Lines
#### Predict the strengths
Under sspredict/ 
```
$ cd /path/to/sspredict/
```
Use predictss.py to predict data from an inputfile
```
$ python3 predictss.py -f inputfile -o outputfile_for_plot  
```
Where outputfile_for_plot is a .txt file including input information and data generated.  

Details of the generated data are described in the [data_description.pdf](examples/output_description.pdf)
#### Plot the strengths with the outputfile_for_plot
```
$ python3 predictss.py -f outputfile_for_plot
```
or to save the .png directly:
```
$ python3 predictss.py -f outputfile_for_plot -s xxx
```
## Examples
![](examples/MnFe-CoNi-Al/MnFe-CoNi-Al_plot.png)
![](examples/Mn-FeCoNi-AlCu/Mn-FeCoNi-AlCu_plot.png)
![](examples/MnFe-CoNi-AlCu/MnFe-CoNi-AlCu_plot.png)

     
