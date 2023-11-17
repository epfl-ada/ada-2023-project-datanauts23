# The Road to Adminship: A Guide for Aspiring Wikipedia Administrators


## Abstract: 
Wikipedia relies on volunteer administrators for maintenance. Users seeking administrator status submit a Request for Adminship (RFA). The Wikipedia community then decides whether to accept or to reject a given candidate through public discussions involving comments and votes. 
Our project aims to provide individuals interested in the Wikipedia administrator role with a guide for a successful election. To achieve this, we analyze the Wikipedia adminship election data spanning from 2003 to 2013, with a specific focus on identifying patterns that impact election outcomes. We examine comments related to those elections to extract the conditions on which users base their votes. Furthermore, by analyzing the network voting graph, we check for user groups, who consistently support or oppose the same candidates or engage in mutual support, to uncover their roles in shaping the community’s decisions. 
We combine all these insights to build a roadmap that assists potential candidates in navigating the path towards Adminship.


## Research Questions:

Our project aims to explore the following research questions:
-  How does affinity influence election outcomes, and are there certain votes that carry more weight than others?
-  How does a candidate's prior engagement in the election process affect their chance of success in his election?
-  Do voters leave comments consistent with their voting choices and which factors do they usually take into account when voting?
-  To what extent does the involvement of active members in a specific election contribute to the success of a candidate?
-  How does the large number of neutral votes impact the acceptance or rejection of a candidate?


## Additional Datasets:

Since our objective is to analyze the factors behind people's voting choices, we need metrics to evaluate the productivity of users. For that, we use additional datasets containing statistics about Wikipedia users, precisely: 

-  The number of pages created per user: [List_of_users_by_pages_created](https://en.wikipedia.org/wiki/User:Bryan/List_of_users_by_pages_created) <br>
-  The number of articles per user : [List_of_Wikipedians_by_article_count](https://en.wikipedia.org/wiki/Wikipedia:List_of_Wikipedians_by_article_count) <br>
-  The number of edits per user: [List_of_Wikipedians_by_number_of_edits](https://en.wikipedia.org/wiki/Wikipedia:List_of_Wikipedians_by_number_of_edits) <br>


## Methods:
### Data preprocessing :
#### Step 1 : Data extraction :
We parse the data text file to extract information that must be included in our initial dataframe. We proceed then to formatting the columns and handling the missing data by exploring the reasons and correcting the inconsistent values.
And for better analysis, we create three dataframes: the first one contains information about candidates, the second one about the voters, and the third one repertories the different elections and their outcomes.

#### Step 2 : Text processing
The voters’ comments are written in [WikiMarkup](https://en.wikipedia.org/wiki/Help:Wikitext), which is not optimal for the textual data analysis. Therefore, we remove the Wiki markup using regular expressions due to the limitations of Wikitext libraries to handle the removal as wished, like: ignoring the wikilinks, … .

#### Step 3 : Exploratory data analysis
We start our data analysis by studying  the number variation of voters and candidates over years in order to have a better understanding of the dataset. Subsequently, we address the question regarding the voters’ engagement  in the voting process: do users who took part in an election in 2003 also engage in subsequent years like 2004, 2005, etc.? 


### Step 4 : data analysis :  
In our analysis, we explore various variables that could influence the acceptance or rejection of candidates in elections, aiming to uncover the factors leading to a successful outcome. We first study the voters' previous voting activity, quantified as the ratio of past votes to active years. Secondly, we examine candidates' prior involvement in the voting process before seeking adminship. To explore the correlation with the election outcome for these four variables, we employ visualizations and hypothesis tests, including t-tests and chi-test.
We finally use the additional datasets to investigate the correlation between the activities of voters and candidates (such as the number of pages created, written, or edited) and the outcome of the election in which they participate.
