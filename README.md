# paper-Glerum-ASPECT-fields-vs-particles

The python plottings scripts were created with python 3.9.7
and the specific environment specified in the file requirements.txt
or environment.yml.

We advise to install the same python libraries through pip with

    pip3.9 install -r ../requirements.txt 

or when the installation process suggests it

    pip3.9 install -r ../requirements.txt  --user

The file requirements.txt was created in anaconda with

    pip list --format=freeze > requirements.txt

In anaconda,

    conda env create -f environment.yml

can be used to create an new environment
with the required packages installed. 

Then plots can be created with, e.g.

    python3.9 stress_plots.py 
