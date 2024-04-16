# Final Design Report - Bias News Detector 1.0

## Table of Contents
1. [Project Description](#project-description)
2. [User Interface Specification](#user-interface-specification)
3. [Test Plan and Results](#test-plan-and-results)
4. [User Manual](#user-manual)
5. [Spring Final PPT Presentation](#spring-final-ppt-presentation)
6. [Final Expo Poster](#final-expo-poster)
7. [Assessments](#assessments)
   - [Initial Self-Assessments](#initial-self-assessments)
   - [Final Self-Assessments](#final-self-assessments)
8. [Summary of Hours and Justification](#summary-of-hours-and-justification)
9. [Summary of Expenses](#summary-of-expenses)
10. [Appendix](#appendix)

## Project Description
Our Bias News Detector integrates SpaCy's LLM with custom rule-based algorithms to assess news content for bias. 
It evaluates sentence polarity and highlights biased statements, enabling users to discern media impartiality effectively. 
This innovative approach enhances critical reading by pinpointing bias in journalistic writing

Abstract: Modern readers of online political content are often just looking for the facts so that they can form their own opinions. Unfortunately, many news sources and articles are biased to one side or the other in their reporting, which can make up readers’ minds for them. For readers who don’t have the time to investigate every author, source, and claim, our tool will provide a simple bias score for any online news article. Readers will then be able to make informed decisions about which articles they choose to read and check other sources if they wish.

## User Interface Specification
The user interface is created using HTML templates and CSS Styling.  The webpages consist of:
- Homepage with project description and outline
  [JTCX HOMEPAGE](https://1drv.ms/i/s!AtwtZBOB204QgQfvwp2lWzZkyXjW?e=DIBxkv)
- Submission Page for user to submit a news article URL to be parsed
  [GET USER ARTICLE](https://1drv.ms/i/s!AtwtZBOB204QgQhHj3tCeiUrlXJS?e=ebb6cy)
- Output Page where our algorithm outputs the Bias within the news article, also has feedback page within it for user to give feedback on our accuracy
  [OUTPUT PAGE](https://1drv.ms/i/s!AtwtZBOB204QgQkO62uOPlyLXRCp?e=oihBRd)
  [OUTPUT PAGE (USER FEEDBACK)](https://1drv.ms/i/s!AtwtZBOB204QgQrsNi27n-QLIKde?e=FWjtvQ)
- Feddback submission page where the user is prompted wether the feedback was valid for our database or not.
  [FEEDBACK SUBMISSION](https://1drv.ms/i/s!AtwtZBOB204QgQtXei2oIxZi0sgi?e=PIMraX)
## Test Plan and Results

Our initial plan was to use a repository of hundreds of thousands of sentences to serve as training data for biased language. We were going to use a bag of words model, TF-IDF model, and at least another model to give us a process that could confidently predict bias for text. On top of this we were going to have an entity sentiment analysis model, and subject analysis model. As we were crafting a test plan for this idea, we started to realize that training a model for this data and then testing the model would be too time consuming for the resources we had. We shifted to a new strategy to accomplish our goal. The plan was now to combine a spacy sentiment analysis model, a model that ran sentiment analysis on named entities, a lexicon to detect biased words in context, a list of authors with biases and a list of authors with biases. In order to test our model/system, we needed to define "bias". Since defining what is biased is inherently biased, we decided to use only reasoning that could be backed up with numbers and data for our system. Our sentiment analysis model we chose was not trained on any specific context, and outputted a value for the sentiment it detected on the input. Our named entity model also gave a value for the sentiment detected. Our article and author bias list came from AllSides, which is a company that panels experts and regular consumers of media across both sides of the political spectrum to understand author and media company bias, and quantifies their responses. We now had quantifiable data for sentences, entities, authors, and publishers. To test our model, we did a pre-scan of any article we gave it, and highlighted sentences that we thought were biased and which side it would fall on. We understood that humans are often better at detecting bias then machines due to the context, intricacies of current events, and nuances that exist in the type of language we were analyzing. We also understood that we are not able to dictate bias. This was a tricky conundrum, but ultimately we decided to label the bias ourselves, especially since many of our test articles came from very inflammatory sites, and the bias was not super difficult to detect. We also ran some of the sentences through other bias detection models that we found online to confirm our labels. After deciding upon a baseline set of labels for an article, we ran our model on the article. We counted both false positives and false negatives as incorrect, but weighed false positives more heavily. We aimed for at least 80% of our selected biased phrases to be picked up, and for 1:10 ratio of false positives to true positives. ___needs more___



## User Manual
### How to Self-Host the Web Tool
You must have Docker installed on your device in order to host the web server. Run `docker compose up` to setup the environment and run the web server on your device. The server will run at http://localhost:8000.

### How to Use the Web Tool
1. User submits a news article URL to the submission box.
2. the Bias News Detector outputs the sentiment of each sentence within the submitted article.
3. At the bottom of the output page, the user can submit feedback where they believe that the bias detector went wrong by pasting the sentence, its outputted bias, and the correct bias.
4. User will then be prompted if the feedback was deemed valid or invalid
5. User can interact with the navigation bar within the header of each webpage to traverse to new article submission, homepage, About JTCX Page, or Meet the Developers Page
   

### Frequently Asked Questions (FAQ)
How can the user tell how bias the output was?

Can you submit any type of url to the webpage?

How can you account for all the different types of bias?

What are the next steps for this project?


## Spring Final PPT Presentation
[Spring Final Presentation Slides]  https://docs.google.com/presentation/d/1iVXy7lLQVvcYawKSG1_Hxu-TaMDuq9k1X4xTHf6QOpo/edit?usp=sharing

## Final Expo Poster
Expo poster can be found within the OneDrive link below:
[CEAS EXPO POSTER](https://1drv.ms/b/s!AtwtZBOB204QgQPADZKmDRHT8NDF?e=kjsBTq)

## Assessments
### Initial Self-Assessments
Summary of initial self-assessments conducted during the fall semester.

#### Cole Hutchins

This project will allow me to gain new skills and grow many of the ones I already have. I anticipate this project involving a lot of collaboration, which will allow me to grow my team working and interpersonal skills. From a strictly technical viewpoint, this project is going to require me to become familiar with a lot of new tools and subject matters. Our team is going to need to find a way to fairly define bias and then devise a method to consistently and accurately capture and label the bias. These challenges are difficult and will require a lot of research so that we can confidently create a model/system to solve our chosen problem.

#### Jordan Shaheen:
The capstone project aims to demonstrate the comprehensive computer science skills acquired during college through the creation of a Bias News Detector, leveraging current software techniques. The choice of a challenging project over a simpler one reflects the team's ambition to maximize their capabilities. The project benefits from a strong foundation in teamwork, software application development, and machine learning from both academic courses and co-op experiences, particularly in web development with Django. The plan involves using Django for website structure and Natural Language Processing to detect biased phrases in news articles, potentially extending to news videos if time permits. The project's success will be measured by its functionality and user-friendly interface, with GitHub commits tracking the team's consistent efforts and progress.

#### Tobias Knueven:
This project will give me a chance to explore the increasingly relevant field of AI technology and challenge myself to think creatively about solving a difficult problem like detecting and measuring political bias in media. I hope to learn more about existing natural language processing and data analysis techniques, and how they can be combined with a user-friendly interface to create a both sophisticated and approachable tool. I'm looking forward to collaborating with our team to develop a software solution to the problem of rampant media bias and spark interest in improving media literacy.

### Final Self-Assessments
Summary of final self-assessments conducted during the spring semester. Exclude confidential team assessments.

#### Cole Hutchins

For our capstone project, I worked to decide on a problem to address, how to solve it, and how to implement our solution. I read academic papers relating to bias detection models, sentiment analysis tools, discussions of bias in media, and others' thoughts on capturing biased language. I wrote a bag of words and TF-IDF model using a collection of hundreds of thousands of data points that we found. Once it became apparent that this was no longer suitable due to time and resource constraints, I worked on helping our team switch to finding a more suitable route to solving our problem. I wrote code to detect sentiment surrounding named entities, oversaw the progress of our model development, and helped make sure our ideas could work by researching into others' solutions.

#### Jordan Shaheen:
In my capstone project, I oversaw team progress and developed the front and back end of our website, integrating an SQL database and Docker. Drawing on my previous experience with Django and Docker, I built the website infrastructure efficiently. Our project involved creating a rule-based natural language processing (NLP) model, necessitating extensive research and team collaboration to ensure accuracy and efficiency.

We successfully implemented a pre-trained large language model, SpaCy, and enhanced its sentiment analysis through custom rules that adjusted polarity scores based on sentence embedding and dependency parsing. One major challenge was ensuring the model's reliability across various news articles. Despite some initial difficulties and my lack of experience in natural language processing, we overcame these challenges, significantly improving my skills in web development, NLP, and collaboration, contributing to the success of the project.

#### Tobias Knueven:
In our capstone project, I contributed in three main ways. Towards the beginning, I took a deep dive dive into exploring the doc2vec algorithm and evaluating whether or not it could capture political bias in news articles. Later, I assisted in experimentation with filtering the sentiment output from SpaCy to better capture bias when we decided on that as our main tool. Finally, I developed some UI features to improve the usability of our tool, like a pop-up tooltip explaining the analysis when hovering over highlighted text in our analysis output.

From this experience I gained exposure to a variety of NLP tools and techniques, like SpaCy, gensim, and the doc2vec text encoding algorithm. I think I succeeded in working collaboratively for the good of the team, which challenged me by forcing me to sacrifice some of my more ambitious goals for the project in favor of a simpler, smaller product.

## Summary of Hours and Justification
Provide a detailed summary of hours worked by each team member, justifying the effort corresponding to at least 45 hours per member.

Jordan Shaheen:
13 hours on frontend devleopment
2 hours on Docker initalization
+30 hours on SpaCy model/rule-based system development
(refrence of work can be found within the link of my contributions that the GitHub repository tracked from commits).
[Jordan Shaheen's Contribution](https://1drv.ms/i/s!AtwtZBOB204QgQzux6nj-V1dPXhw?e=4te9eZ)

Cole Hutchins:
15 hours on researching and studying ideas and tools mentioned in academic papers
15 hours on trying to implement BOW, TF-IDF, and brainstorming and transistion to other ideas when we realized that idea was not sustainable
15 hours of general work on code review, presentation slide creation, project direction,    
5 hours on sentiment analysis on entities and subjects

Tobias Knueven:
15 hours on researching existing AI techniques and toolsets
15 hours experimenting with developing a doc2vec pipeline for news article training data and developing preliminary metrics, eventually discarded in favor of SpaCy
15 hours helping refine rule-based techniques using SpaCy and improve frontend UI
5 hours assisting with project documentation

## Summary of Expenses
There was $0 spent in the creation of this project.

## Appendix
Include references, citations, links to code repositories, meeting notes, and any other pertinent information that supports the project documentation.
https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1224/reports/custom_116661041.pdf
https://realpython.com/sentiment-analysis-python/
https://pypi.org/project/spacytextblob/
https://www.djangoproject.com/
https://spacy.io/
https://github.com/HLTCHKUST/framing-bias-metric/tree/main/data/lexicons


