# Data Shaper
![Static Badge](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)

A config-first pipeline for bringing a dataset into the desired shape.

**Do we need this?**

Probably not, it's a toy project after all, but if you don't get your hands dirty, you're missing out on learning, so here we are.

**Who is this for then? And what problems does it solve?**

1. Small projects/datasets can benefit from this config-first approach to reduce time to clean data
2. People who are tired of writing the same data cleaning functions all over again
3. People who like the idea of working primarily with a config file

**How do I know this is not for me?**

You should probably look elsewhere if :
1. you find yourself writing custom functions more often than not,
2. your dataset consists of numerous columns,
3. you don't want clean data

## Main Ideas

✔ The user defines the configuration for processing a specific dataset, consisting of : _extraction_, _transformation_, and _exportation_ steps. 
    
✔ The pipeline provides an interface for dataset-agnostic data processing based on abstract objects.

✔ Concrete functions are defined for several types of input datasets : _csv_, _xlsx_, _parquet_, etc.

