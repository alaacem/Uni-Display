import time
from lib.TableScraper import TableScraper
from lib.ConfigManager import ConfigManager

if __name__=='__main__':
    config_manager = ConfigManager("config.json")

    while True:
        config_data = config_manager.load()
        scrapper_config = config_data['scrapper_config']
        enable_scraping = scrapper_config.get('enable_scraping')

        if enable_scraping:
            url = scrapper_config.get('url')
            frame_id = scrapper_config.get('frame_id')
            scraper = TableScraper(url, frame_id)

            test_week = scraper.fetch_data_by_frame_id()
            if test_week:
                config_data['times'] = test_week
                config_manager.save(config_data)

            refresh_time = int(scrapper_config.get('refresh_time'))  # Convert to integer
            time.sleep(refresh_time)  # Pause the execution for "refresh_time" seconds
        else:
            break
