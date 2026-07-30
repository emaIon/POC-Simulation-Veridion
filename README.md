# POC-Simulation-Veridion


The goal of this project was to find the best company match for every client input. In the dataset, every client company had several possible candidates. I had to compare these candidates and choose the one that was most likely correct.

First, I opened the dataset and checked the number of rows, the number of client companies and the number of candidates for every company. I also checked if there were missing values in important columns, such as the company name, country, city, postcode, street, website and Veridion ID.

After this, I cleaned the text because the same information could be written in different ways. I changed the text to lowercase, removed extra spaces and removed symbols such as dots, commas and hyphens. I also removed legal words from company names, such as Limited, Ltd, LLC, Inc, Corporation, GmbH and SRL. For example, “ABC Company Limited” and “ABC Company” became easier to compare.

Next, I compared the client company with every candidate. I checked the company name, country, city, postcode and street. I first checked if the company names were exactly the same. I also checked if the names became the same after removing legal words. In some cases, the names were not exactly the same, but one name was included in the other. For example, “Amazon Web Services” can be included in “Amazon Web Services EMEA”.

I created a simple score for every candidate. The company name received the highest number of points because it was the most important information. The candidate also received points when the country, city, postcode or street matched. After calculating the scores, I selected the candidate with the highest score for every client input.

Some results were not clear enough. I marked a result for manual review when two or more candidates had the same top score, when the score was low or when the company names were not related. These cases were saved in a separate Excel file so they could be checked again.

The script creates different Excel files. The most important file is “Final matches improved.xlsx”, which contains one selected candidate for every client input. The file “Manual review.xlsx” contains the results that are less certain and need more checking. The comparison files show how the candidates were compared.

This solution is based on simple rules. It does not use an API or internet search. Because of this, I cannot say that every selected match is 100% correct. Some companies can have different names, old addresses, branches or similar information. However, the solution helps select the most likely candidate and separates the uncertain results for manual review.
