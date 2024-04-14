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
Describe the execution of tests and discuss the results. Include methodologies, test scenarios, and the outcomes.

## User Manual
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
[Spring Final Presentation Slides](https://docs.google.com/presentation/d/1co4_NATWwx58o8fNLTBt8JRdHQASSN4Hl-MjrWZ7DQw/edit#slide=id.g28fbe254194_0_80)

## Final Expo Poster
Expo poster can be found within the OneDrive link below:
[CEAS EXPO POSTER](https://1drv.ms/b/s!AtwtZBOB204QgQPADZKmDRHT8NDF?e=kjsBTq)

## Assessments
### Initial Self-Assessments
Summary of initial self-assessments conducted during the fall semester.

#### Jordan Shaheen:
The capstone project aims to demonstrate the comprehensive computer science skills acquired during college through the creation of a Bias News Detector, leveraging current software techniques. The choice of a challenging project over a simpler one reflects the team's ambition to maximize their capabilities. The project benefits from a strong foundation in teamwork, software application development, and machine learning from both academic courses and co-op experiences, particularly in web development with Django. The plan involves using Django for website structure and Natural Language Processing to detect biased phrases in news articles, potentially extending to news videos if time permits. The project's success will be measured by its functionality and user-friendly interface, with GitHub commits tracking the team's consistent efforts and progress.

### Final Self-Assessments
Summary of final self-assessments conducted during the spring semester. Exclude confidential team assessments.

#### Jordan Shaheen:
In my capstone project, I oversaw team progress and developed the front and back end of our website, integrating an SQL database and Docker. Drawing on my previous experience with Django and Docker, I built the website infrastructure efficiently. Our project involved creating a rule-based natural language processing (NLP) model, necessitating extensive research and team collaboration to ensure accuracy and efficiency.

We successfully implemented a pre-trained large language model, SpaCy, and enhanced its sentiment analysis through custom rules that adjusted polarity scores based on sentence embedding and dependency parsing. One major challenge was ensuring the model's reliability across various news articles. Despite some initial difficulties and my lack of experience in natural language processing, we overcame these challenges, significantly improving my skills in web development, NLP, and collaboration, contributing to the success of the project.

## Summary of Hours and Justification
Provide a detailed summary of hours worked by each team member, justifying the effort corresponding to at least 45 hours per member.

Jordan Shaheen:
13 hours on frontend devleopment
2 hours on Docker initalization
30 hours on SpaCy model/rule-based system development

Cole Hutchins
15 hours on researching and studying ideas and tools mentioned in academic papers
15 hours on trying to implement BOW, TF-IDF, and brainstorming and transistion to other ideas when we realized that idea was not sustainable
15 hours of general work on code review, presentation slide creation, project direction,    
5 hours on sentiment analysis on entities and subjects


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


