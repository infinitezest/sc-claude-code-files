The @EDA.ipynb contains exploratory data analysis on e-commerce data in @ecommerce_data, focusing on sales metrics for 2023. Keep the sam analysis and graphs, and improve the structure and documentation of the notebook.

Review the existing notebook and identify:
- What business metrics are currently calculated
- What visualizations are created
- What data transformations are performed
- Any code quality issues or inefficiences

**Refactoring Requirements**

1. Notebook Structure and Documentation
    - Add proper documentation and markdown cells with clear header and a brief explanation for the section
    - Organize into logical sections:
        - Introduction and Business Objectives
        - Data Loading and Configuration
        - Data Preparation and Transformation
        - Business Metrics Calculation (revenue, product, geographic, customer experience analysis)
        - Summary of Observations
    - Add table of contents at the beginning
    - Include data dictionary explaining key columns and business terms

2. Code Quality Improvements
    - Create reusable functions with docstrings
    - Implement consistent naming and formatting
    - Creating separate Python files:
        - business_metrics.py containing business metric calculations only
        - data_loader.py loading, processing and cleaning the data

3. Enhanced Visualizations
    - Improve all plots with:
        - Clear and descriptive titles
        - Proper axis labels with units
        - Legends where needed
        - Appropriate chart types for the data
        - Include date range in plot titles or captions
        - Use consistent color business-oriented color schemes

4. Configurable Analysis Framework
The notebook shows the computation of metrics for a specific data range (entire year of 2023 compared to 2022).
Refactor the code so that the data is first filtered according to configurable month and year and implement general-purpose metric calculations.

**Deliverables Expected**
- Refactored Jupyter notebook (EDA_Refactored.ipynb) with all improvements
- Business metrics module (business_metrics.py) with documented functions
- Requirements file (requirements.txt) listing all dependencies
- README section explaining how to use the refactored analysis

All the required data files are in ../ecommerce_data folder.
The EDA.ipynb is in the lesson7_files folder, which holds the ecommerce_data folder.
All the generated files (EDA_Refactored.ipynb, business_metrics.py, data_loader.py, dashboard.py, README.md, requirements.tx) should be created in the lesson7_files folder.

**Success Criteria**
- Easy to read code and notebook (do not use icons in the printing statements or markdown cells)
- Configurable analysis that works for any date range
- Reusable code that can be applied to future datasets
- Maintainable structure that other analysts can easily understand and extend
- Maintain all existing analyses while improving the quality, structure, and usability of the notebook.
- Do not assume any business thresholds.
