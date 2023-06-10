# CoAuthorViz_Dashboard
 Cluster Analysis Dashboard of CoAuthor keystroke data
 
# Co-Authorship Visualization with GPT-3

This repository contains the work done during my internship under Dr. Shibani Antonette at University of Technology Sydney. The project involves the analysis of co-authorship with GPT-3 and visualising the results.

## Project Overview

The project is divided into several parts:

1. **Research Paper Analysis**: Analysis of the research paper authored by my professor and other related papers.
2. **Python Notebooks**: Two Python Jupyter notebooks where I performed clustering and created various visualizations.
3. **Datasets**: Three datasets used in the analysis in the Jupyter notebooks.
4. **Python Script**: A Python script file which contains a dashboard for an educator.

## Repository Structure

The repository is organized as follows:

- `.ipynb`: These are the Jupyter notebooks for the project.
- `Dashboard.py`: This is the Python script for the educator dashboard.
- `.py`: These are the Python script for the project.
- `README.md`: This file.

## Getting Started

To get started with the project:

1. Clone the repository
2. Install the required dependencies
3. Run the Jupyter notebooks

## Dependencies

- Python 3.x
- Jupyter
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn

## Usage

To run the Dashboard, navigate to the `project` directory and start Terminal:

```bash
streamlit run Dashboard.py
```

Project Details
The first Python notebook imports one dataset named 'coauthorviz_metrics.csv' in the first part, which was already created by my supervisor. In the second part of the first Python notebook, I imported two files, namely 'CoAuthor_Metadata_creative.csv' and 'CoAuthor_Metadata_argumentative.csv', which are already present in the following folder path 'CoAuthorViz_Dashboard\CoAuthorViz\csv' and were present on the CoAuthor website (https://coauthor.stanford.edu/) as metadata.

In the second Python notebook, I'm reconstructing the data frame containing different metrics in a different way so that it also contains a column where the sequence followed by the writer for every sentence is saved as a dictionary. After the reconstruction process, I saved it in a CSV file named 'df_init.csv', which is present in the root project folder. This CSV file is imported and used for all the analysis further below in the notebook. If someone ever wishes to reconstruct this CSV file again, they just need to set 'execute_code = True', which is in the third code cell of the notebook.

Finally, to run the dashboard, one needs to install Streamlit into their system, right-click into the main project folder, and click 'Open in Terminal'. In that terminal, execute the command line 'streamlit run dashboard.py' to run the dashboard in your browser.

Use this code in both Python notebooks and the Python script to set the Project directory.

```python
# Set the working directory
os.chdir('C:/{Your_Path}/CoAuthorViz_Dashboard')
```

To save the process trees generated, two new blank folders were added in the main 'CoAuthorViz.zip' file/folder, namely, 'Process_Trees' and 'Alpha_Trees'.
