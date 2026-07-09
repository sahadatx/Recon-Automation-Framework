from modules.fuzzing.manager import run_fuzzing

results, overall, failed, elapsed = run_fuzzing([
    "https://httpbin.org"
])

print(results)
print(overall)