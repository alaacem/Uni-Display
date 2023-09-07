
from lib.TableScraper import TableScraper
from lib.ConfigManager import ConfigManager

if __name__=='__main__':
    config=ConfigManager("config.json")
    config_date=config.load()
    scrapper_config=config_date['scrapper_config']
    url = scrapper_config.get('url')
    frame_id = scrapper_config.get('frame_id')
    if enable_scraping:=scrapper_config.get('enable_scraping'):
        scraper = TableScraper(url, frame_id)
        test_week=scraper.fetch_data_by_frame_id()
        config_date['times']=test_week
        config.save(config_date)