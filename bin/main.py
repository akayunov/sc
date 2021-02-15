import sys
from pathlib import Path

sys.path.append(Path(Path(__file__).parent, 'lib', 'sc'))

from sc import main

main.run()
