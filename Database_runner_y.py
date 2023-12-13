import subprocess
import sys
# initially set returncode to 0
returncode2 = 0

while returncode2 == 0:
    result = subprocess.run(['python', 'database_maker_y.py'], capture_output=True, text=True)
    print(result.stdout)
    
    # update returncode with the current script process return code
    returncode2 = result.returncode

# If the loop breaks, it means the returncode was not 0, print this message
print(f"The return code was: {returncode2}, hence the script stopped.")