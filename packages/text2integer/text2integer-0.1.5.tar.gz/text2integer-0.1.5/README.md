The package is used to convert texts to integers. You can use the below examples to get started

pip install text2integer

from text_2_integer.t2i import text_2_integer

ti = text_2_integer.text_2_int()

ti.text2int("five lakh",scales_use='hi')
#500000
ti.text2int("paanch lakh",scales_use='hi')
#500000

ti.text2int("nine point five lakh",scales_use='hi')
#950000

ti.text2int("paanch hazaar",scales_use='hi')
#5000


We support hindi/english languages and the work is in developmental phase

## License
MIT License
License: MIT + file text_2_integer.py