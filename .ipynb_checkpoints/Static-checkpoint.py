{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d5b04df8-1e34-4144-aca3-36dc38a04467",
   "metadata": {},
   "outputs": [],
   "source": [
    "# static.py\n",
    "from model import WECSTATIC\n",
    "from mesa.visualization import SolaraViz, make_space_component, make_plot_component\n",
    "\n",
    "model = WECSTATIC()\n",
    "\n",
    "page = SolaraViz(\n",
    "    model,\n",
    "    components=[\n",
    "        make_space_component(agent_portrayal=wec_draw, backend=\"matplotlib\"),\n",
    "        make_plot_component(measure=\"avg_battery\"),\n",
    "        make_plot_component(measure=\"connections\"),\n",
    "        make_plot_component(measure=\"total_load\"),\n",
    "    ],\n",
    "    model_params=model_params,\n",
    "    name=\"Static WECs\",\n",
    ")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
