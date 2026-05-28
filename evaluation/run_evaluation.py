
import time
import requests
import json


TEST_PROMPTS = [

    "Build a CRM with login and analytics",

    "Build an e-commerce app with payments",

    "Build a hospital management system",

    "Build a food delivery app",

    "Build a school management portal",

    "Build a social media app",

    "Build a ride booking platform",

    "Build a fitness tracker app",

    "Build an inventory management system",

    "Build a banking dashboard"
]


API_URL = "http://127.0.0.1:8000/compile-app"


results = []


for prompt in TEST_PROMPTS:

    print("\n==============================")
    print("TEST:", prompt)

    start_time = time.time()

    try:

        response = requests.post(
            API_URL,
            json={
                "prompt": prompt
            }
        )

        latency = round(
            time.time() - start_time,
            2
        )

        data = response.json()

        success = (
            response.status_code == 200
        )

        repair_success = data.get(
            "repair_success",
            False
        )

        api_repair_success = data.get(
            "api_repair_success",
            False
        )

        results.append({
            "prompt": prompt,
            "success": success,
            "latency_seconds": latency,
            "repair_success": repair_success,
            "api_repair_success": api_repair_success
        })

        print("SUCCESS:", success)
        print("LATENCY:", latency, "sec")

    except Exception as e:

        results.append({
            "prompt": prompt,
            "success": False,
            "error": str(e)
        })

        print("FAILED:", e)


print("\n==============================")
print("FINAL RESULTS")
print("==============================\n")

successful_runs = sum(
    1
    for r in results
    if r["success"]
)

success_rate = (
    successful_runs / len(results)
) * 100


avg_latency = round(

    sum(
        r.get("latency_seconds", 0)
        for r in results
    ) / len(results),

    2
)


summary = {

    "total_tests": len(results),

    "successful_runs": successful_runs,

    "success_rate": success_rate,

    "average_latency": avg_latency,

    "results": results
}


print(
    json.dumps(
        summary,
        indent=2
    )
)


with open(
    "evaluation_results.json",
    "w"
) as f:

    json.dump(
        summary,
        f,
        indent=2
    )


print(
    "\nSaved results to evaluation_results.json"
)

