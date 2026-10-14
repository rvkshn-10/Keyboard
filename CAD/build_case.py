from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).parent/'slim-revision/build_slim.py'),run_name='__main__')
