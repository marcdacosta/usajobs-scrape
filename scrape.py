import urllib2
from bs4 import BeautifulSoup
import requests
import json

def getData(query, pagenumber):
    print "in get data " + query + " " + str(pagenumber)

    url = "https://www.usajobs.gov/Search/?k=" + query + "&p=" + str(pagenumber)
    r  = requests.get(url)

    html = r.text

    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    UniqueSearchID = soup.find(attrs={"id" : "UniqueSearchID"}).attrs['value']
    #print "unique id " + UniqueSearchID

    #print dict(r.cookies)
    cookies = dict(r.cookies)
    # cookies = {
    #     'usaj-f': '%5B%7B%22Name%22%3A%22Demographics%22%2C%22Enabled%22%3Atrue%2C%22Variant%22%3A%22c%22%2C%22LastModified%22%3A%22%2FDate(1494022086847)%2F%22%7D%5D',
    #     'akavpau_usajobs': '1494027362~id=754a8d2cf4eb14006fbbaa965bf5ece2',
    #     'fsr.s': '%7B%22v2%22%3A-2%2C%22v1%22%3A1%2C%22cp%22%3A%7B%22cxreplayaws%22%3A%22true%22%2C%22Basic_Search_Results%22%3A%22Y%22%2C%22Adv_Search_Results%22%3A%22N%22%2C%22My_Account_Home%22%3A%22N%22%2C%22Application_Status%22%3A%22N%22%2C%22Any_JOA%22%3A%22N%22%2C%22Application_Start%22%3A%22N%22%2C%22complete_app%22%3A%22N%22%2C%22view_deails%22%3A%22Y%22%2C%22Apply_Start%22%3A%22N%22%2C%22controlnum%22%3A%22467764200%22%2C%22announcementnum%22%3A%22BPA%2017-7%22%7D%2C%22rid%22%3A%22de358f9-93124767-034e-b0fc-d98bb%22%2C%22to%22%3A4%2C%22c%22%3A%22https%3A%2F%2Fwww.usajobs.gov%2FGetJob%2FViewDetails%2F467764200%22%2C%22pv%22%3A11%2C%22lc%22%3A%7B%22d3%22%3A%7B%22v%22%3A6%2C%22s%22%3Atrue%7D%2C%22d2%22%3A%7B%22v%22%3A5%2C%22s%22%3Atrue%7D%7D%2C%22cd%22%3A2%2C%22sd%22%3A2%2C%22f%22%3A1494027133351%2C%22pn%22%3A2%7D',
    # }

    headers = {
        'Origin': 'https://www.usajobs.gov',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.usajobs.gov/Search/?k=' + query + '&p=' + pagenumber,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = '{"GradeBucket":[],"JobCategoryCode":[],"LocationName":[],"PostingChannel":[],"Department":[],"Agency":[],"PositionOfferingTypeCode":[],"TravelPercentage":[],"PositionScheduleTypeCode":[],"SecurityClearanceRequired":[],"ShowAllFilters":[],"HiringPath":[],"Keyword":"' + query + '","Page":"' + str(pagenumber) + '","UniqueSearchID":"' + UniqueSearchID +'"}'

    r = requests.post('https://www.usajobs.gov/Search/ExecuteSearch', headers=headers, cookies=cookies, data=data)
    payload = json.loads(r.text)

    for job in payload['Jobs']:
    	print str(job) + "\n\n"
    	#example listing: {u'PositionID': u'JV-17-JEH-1938937', u'ClockDisplay': u'', u'ShowMapIcon': True, u'SalaryDisplay': u'Starting at $71,466 (VN 00)', u'Title': u'Nurse Manager - Cardiology Service', u'HiringPath': [{u'IconClass': u'public', u'Font': u'fa fa-users', u'Tooltip': u'Jobs open to U.S. citizens, national or individuals who owe allegiance to the U.S.'}], u'Agency': u'Veterans Affairs, Veterans Health Administration', u'LocationLatitude': 33.7740173, u'LocationLongitude': -84.29659, u'WorkSchedule': u'Full Time', u'Location': u'Decatur, Georgia', u'Department': u'Department of Veterans Affairs', u'WorkType': u'Agency Employees Only', u'DocumentID': u'467314300', u'DateDisplay': u'Open 04/20/2017 to 05/16/2017'}

    if (payload['Pager']['CurrentPageIndex'] <= payload['Pager']['LastPageIndex']):
    	print "getting page " + str(payload['Pager']['NextPageIndex'])
    	getData(query, str(payload['Pager']['NextPageIndex']))
    else:
    	print "Finished processing " + str(payload['Pager']['NumberOfItems']) + " jobs across " + str(payload['Pager']['LastPageIndex']) + " pages"

getData("immigration", "1")