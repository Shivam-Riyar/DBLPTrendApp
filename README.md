# DBLPTrendApp
A lightweight app that analyzes publication trends from the DBLP dataset:
---------------------------------------------------------------------------
To run this locally download app.py file and intall following dependencies : 
- pip install streamlit

Then run the app by using following command :
- streamlit run app.py

Download and extract the files from https://dblp.org/xml/
Upload the file and enter the keywords to get the results.

IMPORTANT : If the file size is bigger than the original specified limit you can increase the limit by using the following command while running - 
- streamlit run app.py --server.maxUploadSize=2048
where you can explicitly set the maxUploadSize.


