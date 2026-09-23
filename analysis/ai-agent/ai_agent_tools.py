import subprocess
import analytics
import json

def run_external(script_path,arguments=None):
    try:        
        output = subprocess.run(['python', script_path, json.dumps(arguments)], #input=json.dumps(arguments), 
                                text=True, stderr=subprocess.STDOUT)
        return output
    except subprocess.CalledProcessError as e:
        print("Program failed with output:\n", e.output)
    except Exception as e:
        return str(e)

print("Running scripts!!!")
print("Start Date and Time", analytics.get_current_et_timestamp())
for module in analytics.chart_modules:
    if module[3]:
        print("*" * 90)
        print(f"Creating chart for {module[1]} using {module[2]}")
        print(run_external(module[2],module[4]))
        print("*" * 90)
print("End Date and Time", analytics.get_current_et_timestamp())