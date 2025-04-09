import concurrent.futures
import subprocess
import time


def run_script(script_path, delay=0):
    # Delay execution if specified
    if delay > 0:
        time.sleep(delay)
    result = subprocess.run(['python3', script_path],
                            capture_output=True, text=True)
    return result.stdout, result.stderr


if __name__ == '__main__':
    scripts = [
        ('Android/Android.py', 60),  # Delay of 60 seconds
        ('iOS/iOS.py', 0)           # No delay
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(run_script, script, delay): script
            for script, delay in scripts
        }

        for future in concurrent.futures.as_completed(futures):
            script = futures[future]
            try:
                stdout, stderr = future.result()
                print(f'Output from {script}:\n{stdout}')
                if stderr:
                    print(f'Error from {script}:\n{stderr}')
            except Exception as exc:
                print(f'{script} generated an exception: {exc}')
