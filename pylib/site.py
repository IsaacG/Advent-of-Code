import apsw
import dotenv
import os
import re
import requests
import subprocess
from urllib import parse
from lxml import etree


class Website:

  BASE = 'https://adventofcode.com/'

  def __init__(self, year, day):
    self.year = str(year)
    self.day = str(int(day))
    conn = apsw.Connection(os.getenv('SQL_DB')
    query = 'SELECT value FROM cookies WHERE key = ?'
    cookie = next(conn.cursor().execute(query, ('aoc',)))[0]

    self.session = requests.Session()
    self.session.headers.update({'cookie': f'session={cookie}'})
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

  def _no_lxml_submit(self, answer) -> str:
    u = parse.urljoin(self.BASE, f'{self.year}/day/{self.day}')
    resp = self.session.get(u)
    resp.raise_for_status()
    m = re.search(r'name="level" value="(.*)"', resp.text)
    assert m, 'Cannot find the submit level'
    level = m.group(1)
    resp = self.session.post(f'{u}/answer', data={'answer': answer, 'level': level})
    resp.raise_for_status()
    cmd = ['pandoc', '--from=html', '--to=markdown']
    p = subprocess.run(cmd, text=True, capture_output=True, input=resp.text)
    return p.stdout

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
