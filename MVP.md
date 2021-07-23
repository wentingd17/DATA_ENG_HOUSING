This project is trying to create a dashboard for property buyers, which enables them to check all closed listings in last 3 months that are closed the the property they're interested in. The app will also show them an estimated price range to help them decide their offer price.

I have two data pulls:
* closed_listings: this data is used for creating the app to show closed listings and creating a linear regression model.
* active_listing: this data will be used to create the app only.

My data were pulled from [US Real Estate API](https://rapidapi.com/datascraper/api/us-real-estate/), which include all closed listing in CA from Dec 2020 to Jul 2021.

I have all my data saved in Mongodb. And I'm doing data EAD via Pyspark and Pandas.

In last 8 months, LA, San Diego, San Jose and Sacramento have higher closed listing volume than other cities in CA.
<img src="closed_listing_by_cities.png" width=500>

The most expensive zipcode is 94027, which is Atherton in Palo Alto, CA.
<img src="median_price_by_zip.png" width=500>

<img src="median_sqrtprice_by_zip.png" width=500>

The map below is a screen shot of a plotly chart, which shows the median property price in the Bay Area. 
<img src="BayArea.png" width=500>


I'm training a linear regression model now to predict the percentage change of close price vs. listing price.
