# Data Shaper

A config-first pipeline for bringing a dataset into the desired shape.

**Do we need this?**
Probably not, it's a toy project after all, but if you don't get your hands dirty, you're missing out on learning, so here we are.

## Main Ideas
✔ The user defines the configuration for processing a specific dataset, including :
    - extraction,
    - validation,
    - transformation,
    - exportation. 
✔ The pipeline provides an interface for dataset-agnostic data processing based on abstract objects.
✔ Concrete functions are defined for several types of input datasets : csv, xlsx, parquet, etc.
