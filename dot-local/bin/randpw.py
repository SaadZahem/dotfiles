#!/usr/bin/env python

import random
import string

length = 16
values = list(string.ascii_letters + string.digits + "!$#%")
print(''.join(random.choice(values) for _ in range(length)))
