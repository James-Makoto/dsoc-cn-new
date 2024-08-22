#!/usr/bin/env python
from trans import Translation

for name in ('dsoc_event',):
    trans = Translation(f'{name}.xlsx')
    trans.save(f'{name}.json', index='Jpn')
