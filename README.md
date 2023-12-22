# The Road to Adminship: A Guide for Aspiring Wikipedia Administrators


## Abstract: 
Wikipedia relies on volunteer administrators for maintenance. Users seeking administrator status submit a Request for Adminship (RFA). The Wikipedia community then decides whether to accept or to reject a given candidate through public discussions involving comments and votes. 
Our project aims to provide individuals interested in the Wikipedia administrator role with a guide for a successful election. To achieve this, we analyze the [Wikipedia adminship election](http://snap.stanford.edu/data/wiki-RfA.html) data spanning from 2003 to 2013, with a specific focus on identifying patterns that impact election outcomes. We examine comments related to those elections to extract the conditions on which users base their votes. Furthermore, by analyzing the network voting graph, we check for user groups, who consistently support or oppose the same candidates or interact with similar Wikipedia content, to uncover their roles in shaping the community’s decisions. 
We combine all these insights to build a roadmap that assists potential candidates in navigating the path towards Adminship.


## Research Questions:

Our project aims to explore the following research questions:
-  How does a candidate's prior engagement in the election process affect their chance of success in his election?
-  Do voters leave comments consistent with their voting choices and which factors do they usually take into account when voting?
-  How does the large number of neutral votes impact the acceptance or rejection of a candidate?
-  Can users be grouped into communities that consistently vote similarly? How does that influence their voting behavior?


## Additional Datasets:

Since our objective is to analyze the factors behind people's voting choices, we need metrics to evaluate the productivity of users. For that, we use additional datasets containing statistics about Wikipedia users, precisely: 

-  The number of pages created per user: [List of users by pages created](https://en.wikipedia.org/wiki/User:Bryan/List_of_users_by_pages_created) <br>
-  The number of articles per user : [List of Wikipedians by article count](https://en.wikipedia.org/wiki/Wikipedia:List_of_Wikipedians_by_article_count) <br>
-  The number of edits per user: [List of Wikipedians by number of edits](https://en.wikipedia.org/wiki/Wikipedia:List_of_Wikipedians_by_number_of_edits) <br>
-  Monthly WikiMedia editor activity: [Montly WikiMedia Editor Activity](https://data.world/wikimedia/monthly-wikimedia-editor-activity) <br>

We also explore a dataset containing edits of discussion pages attached to each Wikipedia article: [Complete Wikipedia Edit History](https://snap.stanford.edu/data/wiki-meta.html) <br>


## Methods:
### Part 1 : Data Preprocessing:
#### Part 1.1 : Data Extraction:
We parse the data text file to extract information that must be included in our initial dataframe. We proceed then to formatting the columns and handling the missing data by exploring the reasons and correcting the inconsistent values.
And for better analysis, we create three dataframes: the first one contains information about candidates, the second one about the voters, and the third one repertories the different elections and their outcomes.

#### Part 1.2 : Text Processing
The voters’ comments are written in [WikiMarkup](https://en.wikipedia.org/wiki/Help:Wikitext), which is not optimal for the textual data analysis. Therefore, we remove the Wiki markup using regular expressions due to the limitations of Wikitext libraries to handle the removal as wished, like: ignoring the wikilinks, … .

#### Part 1.3 : Exploratory Data analysis
We start our data analysis by studying  the number variation of voters and candidates over years in order to have a better understanding of the dataset. Subsequently, we address the question regarding the voters’ engagement  in the voting process: do users who took part in an election in 2003 also engage in subsequent years like 2004, 2005, etc.? 


### Part 2 : Data Analysis :  
In our analysis, we explore various variables that could influence the acceptance or rejection of candidates in elections, aiming to uncover the factors leading to a successful outcome. We first study the voters' previous voting activity, quantified as the ratio of past votes to active years. Secondly, we examine candidates' prior involvement in the voting process before seeking adminship. To explore the correlation with the election outcome for these four variables, we employ visualizations and hypothesis tests, including t-tests and chi-test.
We finally use the additional datasets to investigate the correlation between the activities of voters and candidates (such as the number of pages created, written, or edited) and the outcome of the election in which they participate.

### Part 3 : Textual Data Analysis
#### Part 3.1 : Sentiment Analysis with [Vader](https://medium.com/@rslavanyageetha/vader-a-comprehensive-guide-to-sentiment-analysis-in-python-c4f1868b0d2e): 
We conduct a sentiment analysis using Vader on comments to check the consistency with their associated votes. For that, we rely on the compound score that merges negative, neutral and positive scores. 

#### Part 3.2 : Sentiment Analysis with [TextBlob](https://textblob.readthedocs.io/en/dev/):
The goal of this step is to have a polarity  value that would enable us to know which comment is more positive or negative, and on top of that to have the comment's subjectivity. Thanks to these two parameters, we can find out which comments are the most subjective, and thus have comments that provide more information for the next steps. Using the polarity value, we can then divide our data into two groups to better analyze comments.

#### Part 3.3 : Filtering :
We filter comments to keep only interesting ones, based on the two parameters provided by the sentiment analysis. By putting a threshold on the subjectivity and using the polarity, we keep the comments that are very positive or very negative. This filtering is necessary to get interesting topics for our next step.

#### Part 3.4 : Clustering Comments by Topic :
In this step, we use the [Latent Dirichlet Allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) method to get a list of the most representative words of each topic sorted by their weight. Therefore, we can determine which criteria is the most sought-after.

#### Part 3.5 : N-grams Analysis:
By examining noteworthy words, we analyze the occurrence of n-grams (with n ranging from 2 to 5). The objective is to identify meaningful sequences of words that provide valuable insights into the expectations associated with a new administrator.

### Part 4 : Network Analysis :
The goal behind the Network Analysis section is to understand how group behavior influences voting.
We build three graphs, a voting graph containing the votes cast during the different elections, an agreement graph that reflects how similar voting patterns are between pairs of users, a similarity graph taking into account the similarity between how users interact with Wikipedia content.
From the corresponding networks, we extract communities, using the [Louvain method](https://en.wikipedia.org/wiki/Louvain_method) and analyze how users behave with their own community as well as with other communities. This allows us to understand the role affinity and group-belonging influence the outcomes of elections.

### Part 5 : Answering the scientific questions :
Now that we have completed our data analysis, we can gather our results in a comprehensive guide and create a data story presenting the motivations behind positive, neutral and negative votes. Thanks to this, candidates will gain a better understanding of the factors contributing to a successful election, including the percentage of votes required for a positive outcome, the potential influencers among voters, and the candidate qualities that hold significant importance for adminship. 

## Proposed timeline
-  10/11/2023 - Part 1
-  17/11/2022 - Part 3.1 and 3.2, and beginning of part 2 and part 3.4 - Deliver Milestone 2
-  05/12/2022 - Beginning of Milestone 3: End of part 2 and 3.4 and beginning of part 4
-  09/12/2022 - Part 4: Networks construction and network statistics extraction and part 3: topic mining and comments' categorization.     
-  15/12/2022 - Part 4: Network extraction of communities, analysis of those communities and part 4: creation of datastory's website. 
-  19/12/2022 - Part 5: Data Story and Page Design
-  22/12/2022 - Deliver Milestone 3

## Organization within the team:

-  **Akram Elbouanani** : Data Processing, Network Graph Analysis, Organization of Deliverables, Data Story
-  **Christian Doimo** : NLP, Sentiment Analysis, Clustering Comments by Topic, Data Analysis of additional Datasets, Data Story
-  **Liandro Da Silva Monteiro** : NLP, Sentiment Analysis, Clustering Comments by Topic, Data Story
-  **Murielle Iradukunda** : Data Processing, Data Analysis, Statistical Tests, Matching, Documenting, Graphs Plotting
-  **Yasmine Sakas** : Data Processing, Sentiment Analysis, Data Story Webpage, Data Story, Graphs Plotting



