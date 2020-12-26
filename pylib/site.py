import dotenv
import os
import requests
from lxml import etree
from urllib import parse

class Website:
  
  BASE = 'https://adventofcode.com/'

  def __init__(self, year, day):
    self.year = str(year)
    self.day = str(int(day))

    if not os.getenv('session'):
      dotenv.load_dotenv()
    assert os.getenv('session')

    self.session = requests.Session()
    self.session.headers.update({'cookie': f'session={os.getenv("session")}'})
    self.assert_logged_in()

  def assert_logged_in(self):
    resp = self.session.get(self.BASE)
    resp.raise_for_status()
    assert '[Log Out]' in etree.HTML(resp.content).xpath('//a/text()')

  def get_input(self) -> str:
    u = parse.urljoin(self.BASE, f'{self.year}/day/{self.day}/input')
    resp = self.session.get(u)
    resp.raise_for_status()
    return resp.text

  def submit(self, answer) -> str:
    u = parse.urljoin(self.BASE, f'{self.year}/day/{self.day}')
    resp = self.session.get(u)
    resp.raise_for_status()
    et = etree.HTML(resp.content)
    level = et.xpath('//form/input[@name="level"]/@value')[0]
    resp = self.session.post(f'{u}/answer', data={'answer': answer, 'level': level})
    resp.raise_for_status()
    et = etree.HTML(resp.content)
    output = ''.join(et.xpath('//main/article//text()'))
    return output



