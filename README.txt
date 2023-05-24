GitHub Repository Link: https://github.com/vishalraj247/CoAuthorViz_Dashboard

Here, I'll demonstrate the project, until the part where one can run the final dashboard. First of all, make sure that you are in the main project folder, all the files are there, and you have all the required Python libraries installed. The first Python notebook imports one dataset named 'coauthorviz_metrics.csv' in the first part, which was already created by my supervisor. In the second part of the first Python notebook, I imported two files, namely 'CoAuthor_Metadata_creative.csv' and 'CoAuthor_Metadata_argumentative.csv', which are already present in the following folder path 'CoAuthorViz_Dashboard\CoAuthorViz\csv' and were present on the CoAuthor website (https://coauthor.stanford.edu/) as metadata.

In the second Python notebook, I'm reconstructing the data frame containing different metrics in a different way so that it also contains a column where the sequence followed by the writer for every sentence is saved as a dictionary. After the reconstruction process, I saved it in a CSV file named 'df_init.csv', which is present in the root project folder. This CSV file is imported and used for all the analysis further below in the notebook. If someone ever wishes to reconstruct this CSV file again, they just need to set 'execute_code = True', which is in the third code cell of the notebook.

Finally, to run the dashboard, one needs to install Streamlit into their system, right-click into the main project folder, and click 'Open in Terminal'. In that terminal, execute the command line 'streamlit run dashboard.py' to run the dashboard in your browser.

Use this code in both Python notebooks and the Python script to set the Project directory.
# Set the working directory
os.chdir('C:/{Your_Path}/CoAuthorViz_Dashboard')

To save the process trees generated, two new blank folders were added in the main 'CoAuthorViz.zip' file/folder, namely, 'Process_Trees' and 'Alpha_Trees'. Also, for the 2nd notebook, you will need to install the 'graphviz' library and put its directory into your local and system environment variable path.