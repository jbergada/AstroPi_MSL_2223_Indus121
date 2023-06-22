#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:20:23 2023

@author: linkat
"""

import folium
import pandas as pd

# Load CSV file
df = pd.read_csv('data.csv')

# Extract latitude, longitude and label columns
latitudes = df['Latitude']
longitudes = df['Longitude']
etiquetas = df['id']

# Create a map with Google Maps tile provider (satellite)
mapa = folium.Map(location=[latitudes[0], longitudes[0]], tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google')

# Add markers for each point with labels
for lat, lon, etiqueta in zip(latitudes, longitudes, etiquetas):
    folium.Marker(location=[lat, lon], popup=etiqueta).add_to(mapa)

# Display the map
mapa.save('mapa.html')  # Guardar el mapa en un archivo HTML
mapa