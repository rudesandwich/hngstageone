from flask import Flask, request, Response
import requests
import json  # Import the json module

app = Flask(__name__)

# Helper Functions (keep these the same as before)
def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is perfect."""
    if n < 2:
        return False
    divisors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.extend([i, n // i])
    return sum(divisors) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d ** length for d in digits) == n

def get_fun_fact(n):
    """Fetch a fun fact about the number from numbersapi.com."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        return response.text if response.status_code == 200 else "No fun fact available."
    except requests.RequestException:
        return "No fun fact available."

# API Endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Extract the number parameter
    number = request.args.get('number')

    # Validate the input
    try:
        # Convert the input to a float (to handle both integers and decimals)
        number = float(number)
    except (ValueError, TypeError):
        # Return 400 with the specified error format
        error_response = {"number": str(number), "error": True}
        return Response(
            json.dumps(error_response, indent=4),  # Pretty-print JSON
            status=400,
            mimetype='application/json',  # Explicitly set the Content-Type header
            headers={'Content-Type': 'application/json'}  # Ensure the header is set
        )

    # Determine properties (only for integers)
    properties = []
    if number == int(number):  # Check if the number is an integer
        number = int(number)  # Convert to integer for property checks
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 else "even")
    else:
        # For floating-point numbers, skip Armstrong and odd/even checks
        properties.append("floating-point")

    # Build response
    response = {
        "number": number,
        "is_prime": is_prime(int(number)) if number == int(number) else False,  # Prime only for integers
        "is_perfect": is_perfect(int(number)) if number == int(number) else False,  # Perfect only for integers
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(int(number)))) if number == int(number) else None,  # Digit sum only for integers
        "fun_fact": get_fun_fact(int(number)) if number == int(number) else "No fun fact available for floating-point numbers."
    }

    # Return pretty-printed JSON response
    return Response(
        json.dumps(response, indent=4),  # Pretty-print JSON
        status=200,
        mimetype='application/json',  # Explicitly set the Content-Type header
        headers={'Content-Type': 'application/json'}  # Ensure the header is set
    )

# Health Check Endpoint (optional but recommended)
@app.route('/health', methods=['GET'])
def health_check():
    health_response = {"status": "healthy"}
    return Response(
        json.dumps(health_response, indent=4),  # Pretty-print JSON
        status=200,
        mimetype='application/json',  # Explicitly set the Content-Type header
        headers={'Content-Type': 'application/json'}  # Ensure the header is set
    )

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

