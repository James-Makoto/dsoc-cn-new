#!/usr/bin/env python
from trans import Translation

for name in ('dsoc_event',):
    trans = Translation(f'{name}.xlsx')
    trans.save(f'{name}.json', index='Tag')

for name in ('bible',):
    trans = Translation(f'{name}.xlsx')
    trans.save(f'{name}.json', index='Tag')

for name in ('fusion',):
    trans = Translation(f'{name}.xlsx')
    trans.save(f'{name}.json', index='Tag')

for name in ('code.bin',):
    trans = Translation(f'{name}.xlsx')
    trans.save(f'{name}.json', index='Tag')
