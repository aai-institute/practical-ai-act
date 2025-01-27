# A demonstration of AI Act compliance with machine learning systems

This repository demonstrates how machine learning projects can achieve compliance with the EU AI Act.
The most important requirements and provisions of the AI Act are introduced, and linked with the steps taken to achieve compliance in a machine learning pipeline.
Importantly, we present a way of integrating these requirements into a professional machine learning lifecycle, introducing tools that help specifically to construct safe and robust AI systems.

## Case study: Using US Census data to predict income

The project presented here has the goal of predicting income for a person based on some aspects of their economic and social status.
For this, data collected by the Bureau of the Census for the Bureau of Labor Statistics is used, specifically the 2022 [Annual Social and Economic (ASEC)](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar22.pdf) Supplement to the Current Population Survey.

The data was sourced in [CSV format](https://www2.census.gov/programs-surveys/cps/datasets/2022/march/asecpub22csv.zip) from the official United States Census Bureau website.
It contains a large number of columns encoding information about households, families, and persons, with supplementary markers indicating if missing data has been imputed on a per-column basis.

Our goal is to create a machine learning system that predicts household income as a function of a curated set of input features from the ASEC data.
It is formulated as a regression problem, i.e., we want to obtain a system modelling the mathematical relationship between socio-economic data and the expected income of a person.
