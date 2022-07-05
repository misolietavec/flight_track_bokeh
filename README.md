# Flight tracking application with openskynet data and bokeh 

Inspired by [this blog post](https://www.geodose.com/2020/08/create-flight-tracking-apps-using-python-open-data.html)

There is standalone application flight_track and the "small" application
notebook flight_small using flight_utils. Both are prepared for further
development with interactive widgets from pyviz panel. They can be deployed
directly in Jupyter (Jupyterlab) notebook and also by 

``panel serve small_flight.py``

It is assumed that you have jupytext extension installed and configured for
paired notebooks. This is my configuration:

```python
# Always pair ipynb notebooks to py:percent files
formats = "ipynb,py:percent"
```

(see jupytext documentation). You can then open .py files as Jupyter
notebooks.



 
