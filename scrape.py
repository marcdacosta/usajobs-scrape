"""
example job listing:

    {
        'PositionID': 'JV-17-JEH-1938937',
        'ClockDisplay': '',
        'ShowMapIcon': True,
        'SalaryDisplay': 'Starting at $71,466 (VN 00)',
        'Title': 'Nurse Manager - Cardiology Service',
        'HiringPath': [{
            'IconClass': 'public',
            'Font': 'fa fa-users',
            'Tooltip': 'Jobs open to U.S. citizens, national or individuals who owe allegiance to the U.S.'
        }],
        'Agency': 'Veterans Affairs, Veterans Health Administration',
        'LocationLatitude': 33.7740173,
        'LocationLongitude': -84.29659,
        'WorkSchedule': 'Full Time',
        'Location': 'Decatur, Georgia',
        'Department': 'Department of Veterans Affairs',
        'WorkType': 'Agency Employees Only',
        'DocumentID': '467314300',
        'DateDisplay': 'Open 04/20/2017 to 05/16/2017'
    }
"""

import json
import requests
from time import sleep
from bs4 import BeautifulSoup

BASE_URL = 'https://www.usajobs.gov'
INTERVAL = 60 * 60 * 12


def scrape(query, page=1):
    print('scraping page: {}'.format(page))
    url = '{base}/Search/?k={query}&p={page}'.format(
        base=BASE_URL, query=query, page=page)
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    search_id = soup.find(attrs={'id' : 'UniqueSearchID'}).attrs['value']

    cookies = dict(resp.cookies)
    headers = {
        'Origin': BASE_URL,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': url,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    data = {
        'GradeBucket': [],
        'JobCategoryCode': [],
        'LocationName': [],
        'PostingChannel': [],
        'Department': [],
        'Agency': [],
        'PositionOfferingTypeCode': [],
        'TravelPercentage': [],
        'PositionScheduleTypeCode': [],
        'SecurityClearanceRequired': [],
        'ShowAllFilters': [],
        'HiringPath': [],
        'Keyword': query,
        'Page': page,
        'UniqueSearchID': search_id
    }

    resp = requests.post('{base}/Search/ExecuteSearch'.format(base=BASE_URL),
                         headers=headers, cookies=cookies, data=json.dumps(data))
    payload = json.loads(resp.text)
    results = payload['Jobs']
    if (payload['Pager']['CurrentPageIndex'] <= payload['Pager']['LastPageIndex']):
        next = payload['Pager']['NextPageIndex']
        fetched = False
        while not fetched:
            try:
                results.extend(scrape(query, page=next))
                fetched = True
            except requests.exceptions.ConnectionError:
                sleep(5)
    return results


def on_job(job):
    """called on a new job listing, e.g. post to twitter or sth"""
    print('{} ({})'.format(job['Title'], job['Location']))


if __name__ == '__main__':
    try:
        jobs = json.load(open('jobs.json', 'r'))
    except FileNotFoundError:
        jobs = {}

    while True:
        results = scrape('immigration')
        for job in results:
            id = job['PositionID'] # alternatively, 'DocumentID'
            if id not in jobs:
                jobs[id] = job
                on_job(job)

        with open('jobs.json', 'w') as f:
            json.dump(jobs, f)
        print('done')

        sleep(INTERVAL)
