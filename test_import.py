import traceback
import sys
try:
    import main
    print("Success importing main")
except Exception as e:
    print("Error importing main")
    traceback.print_exc()
