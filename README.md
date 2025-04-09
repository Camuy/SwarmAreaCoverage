# SwarmAreaCoverage
SwarmAreaCoverage is a simulation for agents to cover a certain area unlock the performance of the swarm to better perform this task.

# Introduction
## Get Start
The required dependences are listed below:
- [Mesa](https://mesa.readthedocs.io/latest/index.html) (Its dependencies are not listed fully!)
- [Solara](https://solara.dev)
- [Matplotlib](https://matplotlib.org)
- [Numpy](https://numpy.org)
- [Scipy](https://scipy.org)
First of all install all the dependency.
Mesa required all this library, if you install only Mesa you are not able to use it. Install also the other if not done yet.

## Install
This repository is basedo on python 3.12.9. It should work also with the version 3.11.0 and older.

First of all you must upgrade all packages, and if you don't have pip you must install it.
<pre><code class="language-bash">  pip install --upgrade pip
</code></pre>

Once you have installed all the dependencies, you can clone this repository and perform the simulation.

to clone the repository you must have git installed.

<pre><code class="language-bash">  pip install git
  git clone https://github.com/Camuy/SwarmAreaCoverage.git
</code></pre>

In a terminal you execute this commands to install all the dependency:
<pre><code class="language-bash">  pip install -r requirements.txt
</code></pre>

Now ypou should able to run the simulation

## Usage
The repo is divided in 3 important files:
- app.py
- model.py
- agent.py

is possible to have other files that changes informatiotion on these files, like the information of the gradient on the environment.

### app.py
It create the enviroment on top of whom the other codes are run. It gives you the information to access the [localhost at port 8765](http://localhost:8765) to get access to the simulation itself.

### model.py
It is a file responsable of creating the information on the simulation environment and mathematical model.

### agent.py
It create all the instruction each singlre agent has to follow. It besically dictate the role to be followed by the agent.

## Run
To run the code you simply have to run this code.
<pre><code class="language-bash">  solara run app.py</code></pre>
