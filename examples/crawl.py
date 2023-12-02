import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from src.crawl import Crawler

if __name__ == "__main__":
    crawler = Crawler(api_key=os.getenv('API_KEY')) # Put your API key in .env file

    ######################################################################################
    ########################### Get all categories and metrics ###########################
    ######################################################################################

    all_categories_and_metrics = crawler.get_all_metrics()
    categories = list(all_categories_and_metrics.keys())
    print("There are %d categories in total" % len(categories))

    print(categories)
    for category in categories:
        for sub_category in all_categories_and_metrics[category]:
            for sub_sub_category in all_categories_and_metrics[category][sub_category]:
                print("There are %d metric(s) in subcategory %s of %s category" % (len(
                    all_categories_and_metrics[category][sub_category][sub_sub_category]), sub_category, category))
    
    ######################################################################################
    #################################### Download data ###################################
    ######################################################################################

    crawler.download_historical_data(metric_id="usd_price", resolution="1d", symbol="BTC", location='./data')
    print("Lastest data: ", crawler.get_lastest_data(metric_id="usd_price", resolution="1h", symbol="BTC"))