from urllib.request import Request, urlopen, urlretrieve
from urllib.error import HTTPError
import time
import re
import json
import datetime
import os


def sorted_alphanumeric(data):
    """
    https://stackoverflow.com/a/48030307/2441026
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


def all_pages(region):
    url = f"https://{region}.tribunnews.com/epaper/"
    user_agent = "Googlebot-News"
    headers = {'User-Agent': user_agent}
    req = Request(url, headers=headers)
    with urlopen(req) as resp:
        regex = re.findall(rf"{region}\/\d+\.jpg", resp.read().decode("utf-8"))
    print('[VISIT] ' + url)
    data = sorted_alphanumeric(list(set(regex)))
    if region == "jabar":
        data = data[:16]
        pass
    return [f"https://epaper.tstatic.net/{page}" for page in data]



def download_epaper_per_page(url):
    # url: https://epaper.tstatic.net/jabar/1.jpg
    date = datetime.date.today()
    urlpath = url.split("/")[-2:]
    # urlpath: ['jabar', '1.jpg']
    dirpath = "tribun/{region}/{year}/{month}/{date}".format(
        region=urlpath[0],
        year=date.strftime('%Y'),
        month=date.strftime('%m'),
        date=date
    )
    # dirpath: tribun-jabar/2021/04/2021-04-23
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = "/".join([dirpath, os.path.basename(url)])
    # filepath: tribun-jabar/2021/04/2021-04-23/1.jpg
    try:
        urlretrieve(url, filepath)
    except HTTPError as e:
        # print(e.code)
        # print(e.read())
        pass

    print("[DOWNLOAD] " + url)




def main():
    ts = time.time()
    regions = ["surabaya", "jabar", "jogja", "jateng", "aceh", "palembang", "sumsel", "bangka", "belitung", "batam", "jambi", "lampung", "medan", "pekanbaru", "makassar", "manado", "kaltim", "banjarmasin", "pontianak", "kupang", "bali", "wartakota"]
    #regions = ["jabar"]
    for region in regions:
        res = all_pages(region)
        print(region, len(res), res)
        for i in res:
            download_epaper_per_page(i)
    print('took', time.time() - ts)

if __name__ == "__main__":
    main()


