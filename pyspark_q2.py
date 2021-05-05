# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ErXM-YLM0KDi1DccudHCZPtveW821-kt
"""

import os
import sys
import pandas as pd
from pyspark.sql import *

NoCPU = int(sys.argv[1])
outfile = sys.argv[2]

if NoCPU == 0:
  print('No of CPU needs to be minimum 1')
else:
  spark  = SparkSession.builder.appName('Airport data Control').getOrCreate()
  df = spark.read.csv('/content/sample_data/airports.csv',header = True,inferSchema =True)
  os.environ["SPARK_WORKER_CORES"] = str(NoCPU)
  df.repartition(NoCPU)
  df2 = df.groupby("COUNTRY").count()
  df2 = df2.orderBy("count",ascending = False).select('COUNTRY').limit(1)
  df2 = df2.select('*').toPandas()
  df2.to_csv(outfile,index=False)