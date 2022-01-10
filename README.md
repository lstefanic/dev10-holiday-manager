# dev10-holiday-manager

Text-based application to track US holidays

### Functionality

Application begins by reading in all holidays from `holidays.json` and scraping all holidays from [https://www.timeanddate.com/holidays/us/](https://www.timeanddate.com/holidays/us/) that occur within 2 years of the present year. The user may then add and remove holidays, and view holidays for any given week.

### How to use

Download the files `holiday.py`, `holidays.json`, and `menu.txt`, and in a terminal, run `python holiday.py`. Before exiting, save your changes, and the holidays you have chosen to track will be written into a file called `output.json`

### Sample use

An example of a use of the application is in `holiday.ipynb`

### Technology used

Application uses Python 3.9.5 and includes the following `import` statements:

    import datetime
    import json
    from bs4 import BeautifulSoup
    import requests
    from dataclasses import dataclass