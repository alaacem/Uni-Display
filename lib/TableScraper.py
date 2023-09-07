import requests
from bs4 import BeautifulSoup

class TableScraper:
    def __init__(self, scrapper_config):

        self.url = scrapper_config['url']
        self.frame_id = scrapper_config['frame_id']
        self.cached_results = {}

    def fetch_webpage(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to get the page: {response.status_code}")
            return None

    def extract_date_range(self, frame_div):
        date_range_text = frame_div.find(string=lambda s: 'Öffnungszeiten vom' in s)
        if date_range_text:
            date_range = date_range_text.replace('Öffnungszeiten vom', '').split('-')
            start_date, end_date = date_range[0].strip(), date_range[1].strip().split(':')[0]
            return start_date, end_date
        return None, None

    def extract_times(self, frame_div):
        schedule = {}
        table = frame_div.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    day_name = cols[0].text.strip()
                    time_intervals = cols[1].text.strip().split('&')
                    while len(time_intervals) < 2:  # Ensure there are two time slots
                        time_intervals.append('')
                    schedule[day_name] = [interval.strip() for interval in time_intervals]
            return schedule
        return None

    def parse_table(self, html_text, frame_id):
        soup = BeautifulSoup(html_text, 'html.parser')
        frame_div = soup.find('div', {'id': frame_id})
        if frame_div:
            start_date, end_date = self.extract_date_range(frame_div)
            schedule = self.extract_times(frame_div)
            return {
                'start_date': start_date,
                'end_date': end_date,
                'schedule': schedule
            }
        else:
            print(f"No frame found with id: {frame_id}")
            return None


    def update_cache(self, frame_id, schedule):
        old_data = self.cached_results.get(frame_id, {})
        if schedule != old_data:
            self.cached_results[frame_id] = schedule
            return schedule
        return False

    def fetch_data_by_frame_id(self):
        html_text = self.fetch_webpage()
        if html_text:
            schedule = self.parse_table(html_text, self.frame_id)
            if schedule:
                return self.update_cache(self.frame_id, schedule)
        return False

    def reload(self,):
        results = self.fetch_data_by_frame_id()
        if results:
            return results
        return False