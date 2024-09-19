#!/usr/bin/env python
from trans import Translation

for name in ('dsoc_event',):
    trans = Translation(f'{name}.json')
    trans.save(f'{name}.xlsx', index='Jpn')

for name in ('bible',):
    trans = Translation(f'{name}.json')
    trans.save(f'{name}.xlsx', index='Jpn')

for name in ('fusion',):
    trans = Translation(f'{name}.json')
    trans.save(f'{name}.xlsx', index='Jpn')

for name in ('code.bin',):
    trans = Translation(f'{name}.json')
    trans.save(f'{name}.xlsx', index='Jpn')

for name in ('ds_auction',):
    trans = Translation(f'{name}.json')
    trans.save(f'{name}.xlsx', index='Jpn')
