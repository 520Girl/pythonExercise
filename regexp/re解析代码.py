import re

s = """<div class="jay"><span id="1">测试</span></div>
<div class="jaz"><span id="2">测试2</span></div>
<div class="jolin"><span id="3">测试3</span></div>
<div class="tory"><span id="4">测试4</span></div>
"""
regex = re.compile(r'<div class=".*?"><span id="(?P<id>\d+)">.*?</span></div>', re.S)
re_list = regex.match(s)

print(re_list.group())