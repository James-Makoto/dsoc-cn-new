#!/usr/bin/env python
from trans import Translation


for name in ('dsoc_event',):
    trans = Translation(f'{name}.json')
    trans.save(f'{name}.xlsx', index='Jpn')
