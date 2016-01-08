Readme
=============
Follow instructions at [Instructions](https://linkurio.us/linkedin-inmaps-discontinued-visualize-network-now/) and [More](http://allthingsgraphed.com/2014/10/16/your-linkedin-network/)

You can skip steps 1-3 if you already have a LinkedIn application with OAuth credentials setup.

## 1. Install Software prerequisites
Install this python packages

	pip install oauth2 simplejson unidecode


## 2. Create new LinkedIn application
Look at instructions at [Instructions](https://linkurio.us/linkedin-inmaps-discontinued-visualize-network-now/) and [More](http://allthingsgraphed.com/2014/10/16/your-linkedin-network/)


## 3. Get OAuth authentications credentials
In order to renew the OAuth authentication details follow these steps

Run a local HTTP web server

	python -m HTTPServer 8001

Generate the OAuth credentials

	python lioauth.py

Notes:
1. **consumer_key** is what LinkedIn calls **Api Key**
2. **consumer_secret** is what LinkedIn calls **Secret Key**
3. **OAUTH_TOKEN** is what LinkedIn calls **OAuth User Token**
4. **OAUTH_TOKEN_SECRET** is what LinkedIn calls **OAuth User Secret**


## 4. Query LinkedIn
Using the OAuth you have in LinkedIn application or the ones you generated at step 3 query LinkedIn running the script

	python liquery.py

This will generate two files:

1. **li-rels.csv** containing all the edges
2. **li-nodes.csv** containing all the nodes


## 5. Clean results
Run the script

	python liclean.py

6. In order to remove lines with "..., private private" run this replace (all occurrance) in sublime with Regex enabled "^.*,private private$\n"
7. Remove quotes from nodes and rels