import subprocess

result = subprocess.run(
    [
        r"C:\Users\apkoval\AppData\Local\Programs\Ollama\ollama.exe",
        "run",
        "qwen3:4b",
        "Привет"
    ],
    capture_output=True,
    text=True,
    timeout=120,
)

print("RETURN CODE:", result.returncode)
print()
print("STDOUT:")
print(result.stdout)
print()
print("STDERR:")
print(result.stderr)