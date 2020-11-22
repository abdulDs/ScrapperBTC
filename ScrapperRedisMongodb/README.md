# Mongodb 

## This Proggram dose:
- [1] Scrapes BTC values data from (https://www.blockchain.com/btc/unconfirmed-transaction.);
- [2] Caches the data in redis memory for 60 sec
- [3] Output the top value from our cached data
- [4] Insert this observation into mongodb

This programm will execute every 1 minute


# How to use?
- [1] install python3 and it's needed library
- [2] install text editor to run the code
- [3] install and run Mongodb
- [4] install and run redis


# Our Goal
to Scrape (https://www.blockchain.com/btc/unconfirmed-transactions) websites every 1 minute and store the observation in as an object in mongodb collection.
