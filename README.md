# RMIT-ABC-Fact-Checked-Data-Collection

Main task: Given a claim that has to be fact checked, identify the first tweet where that claim was made (i.e., **original tweet**)

.... Under construction ... 


## install dependencies:
pip3 install -r requirements.txt

pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git


## ABC Fact Check scraping code

### v1 notebooks
v1 notebooks ([ABC FactCheck Home page scraping](https://github.com/stevcabello/RMIT-ABC-Fact-Checked-Data-Collection/blob/main/notebooks/v1/ABC%20FactCheck%20Home%20page%20scraping.ipynb) and [ABC FactCheck archived page scraping](https://github.com/stevcabello/RMIT-ABC-Fact-Checked-Data-Collection/blob/main/notebooks/v1/ABC%20FactCheck%20archived%20page%20scraping.ipynb)) collect all the fact check articles url and inspect the <body> to identify tweet/twitter-related content. Results from v1 are stored as csv files in [resultsv1 folder](https://github.com/stevcabello/RMIT-ABC-Fact-Checked-Data-Collection/tree/main/resultsv1). v1's results have the article type, the article url, a flag True/False for twitter-related content, the part of the text in the <body> that matches with tweet/twitter content.
  
  
### v2 notebooks
v2 notebooks ([ABC FactCheck Home page scraping v2](https://github.com/stevcabello/RMIT-ABC-Fact-Checked-Data-Collection/blob/main/notebooks/v2/ABC%20FactCheck%20Home%20page%20scraping%20v2.ipynb) and [ABC FactCheck archived page scraping v2](https://github.com/stevcabello/RMIT-ABC-Fact-Checked-Data-Collection/blob/main/notebooks/v2/ABC%20FactCheck%20archived%20page%20scraping%20v2.ipynb)) collect all the fact check articles url and inspect "The Claim" section to identify tweet/twitter-related content. Besides, they extract all the quoted text in the "The Claim" section and use those claims to identify the original tweet. Results from v2 are stored as csv files in [resultsv2 folder](https://github.com/stevcabello/RMIT-ABC-Fact-Checked-Data-Collection/tree/main/resultsv2). v2's results have the article type, the article url, a flag True/False for twitter-related content, the part of the text in "The Claim" that matches with tweet/twitter content, the quoted claims, and the original tweet for each quoted claim.
  

