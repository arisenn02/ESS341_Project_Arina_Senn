# Spatial and Temporal Analysis of Urban Issue Reports in Zurich
This project analyzes the spatial distribution of service requests in the city of Zurich, which can be reported by citizens via the platform www.zueriwieneu.ch. 
The analysis focuses in particular on the service category "Abfall/Sammelstelle" and investigates its spatial distribution,processing times and temporal pattern.

## Data Sources
- Zurich Open Data Portal: https://data.stadt-zuerich.ch/dataset/geo_zueri_wie_neu
- Zurich Open Data Portal: https://data.stadt-zuerich.ch/dataset/geo_statistische_quartiere
- Zurich Open Data Portal: https://data.stadt-zuerich.ch/dataset/bev_bestand_jahr_statzone_od3241

The reports and statistical neighborhood dataset were downloaded on the 24.04.2026. \
The population dataset was downloaded on 11.05.2026

## Repository structure
data/raw/ -> raw datasets \
data/processed/ -> processed datasets \
notebooks/ -> Jupyter Notebook \
outputs/ -> exported figures and maps \
environment -> file with required python packages 

## Setup Instructions
This project requires Python 3.11.15.

Create the environment using the environment.yml file:

conda env create -f environment.yml
conda activate ess341_projekt

## Execution Order
1. Open zuerich_service_analysis.ipynb
2. Run all cells from top to bottom
