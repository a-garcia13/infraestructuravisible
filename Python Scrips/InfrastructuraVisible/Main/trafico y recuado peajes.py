import pandas as pd
import numpy as np
import csv
import json
from math import radians, cos, sin, asin, sqrt
import os

class Peaje:
    def __init__(self, name, code):
        self.code = code
        self.name = name
        self.trafico = {}
        self.recaudo = {}

print(os.path.dirname(__file__))
home = os.getcwd()
file = "trafico.csv"
result = os.path.join(home, file)
with open(result, 'r') as f:
    trafico_file = pd.read_csv(f, sep=",")

file = "recaudo.csv"
result = os.path.join(home, file)
with open(result, 'r') as f:
    recaudo_file = pd.read_csv(f, sep=",")

peajes = {}
años = ['2014','2015','2016','2017','2018']
meses = ['01','02','03','04','05','06','07','08','09','10','11','12']

for index, row in trafico_file.iterrows():
    name = "" + row['NombreEstacionPeaje']
    new_peaje = Peaje(row['NombreEstacionPeaje'], row['Codigo Invias'])
    for year in años:
        for month in meses:
            date = month+"/"+"01"+"/"+year
            value = row[date]
            new_peaje.trafico[date] = value
    peajes[name] = new_peaje

for index, row in recaudo_file.iterrows():
    name = "" + row['NombreEstacionPeaje']
    if name in peajes:
        old_peaje = peajes[name]
        for year in años:
            for month in meses:
                date = month + "/" + '01' + "/" + year
                value = row[date]
                old_peaje.recaudo[date] = value
    else:
        new_peaje = Peaje(row['NombreEstacionPeaje'], row['Codigo Invias'])
        for year in años:
            for month in meses:
                date = month + "/" + '01' + "/" + year
                value = row[date]
                new_peaje.trafico[date] = value
        peajes[name] = new_peaje

columns_names = ["Codigo Invias", "NombreEstacionPeaje", "Fecha", "Trafico", "Recaudo"]
df = pd.DataFrame(columns=columns_names)

count = 0
for key, value in peajes.items():
    for year in años:
        for month in meses:
            date = month + "/" + '01' + "/" + year
            recaudado = 0
            trafico = 0
            if date in value.recaudo:
                recaudado = value.recaudo[date]
            if date in value.trafico:
                trafico = value.trafico[date]
            df.loc[count] = [value.code, value.name, date, trafico, recaudado]
            count = count+1

df.to_csv("trafico y recaudo.csv", sep=",", encoding='utf-8-sig')