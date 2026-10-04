#!/usr/bin/env python

import random
import string

print(''.join(random.choice(list(string.ascii_letters + string.digits))) for _ in range(16))
