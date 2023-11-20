# Halftone-Visual-Cryptography
This Script creates 2-out-of-2 halftone visual cryptography shares and combines them using Pixel XOR and Transposition

Installation:
```shell
git clone https://github.com/Cavan-M/Halftone-Visual-Cryptography.git)https://github.com/Cavan-M/Halftone-Visual-Cryptography.git
```
```shell
cd PATH/TO/REPOSITORY/
```
```shell
python -m pip install -r requirements.txt
```

Usage:
```python
from halftoneGeneration import HalftoneImageEncryption

halftone_generator = HalftoneImageEncryption("images/source/lena.png", "lena_halftone")  # First param is input path, second param is output filename
halftone_generator.create_halftone()   # create halftone image from greyscale image
halftone_generator.convert_to_matrix()   # format halftone image for share generation
halftone_generator.create_shares()   # create encrypted shares
halftone_generator.combine_shares_XOR()   # Combine shares by XOR
halftone_generator.combine_shares_transpose()   # Combine shares by transposition
```
