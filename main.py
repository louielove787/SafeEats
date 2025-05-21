from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simple ingredient categories for demo purposes
SAFE_INGREDIENTS = {
    'water', 'rice', 'oats', 'apple', 'banana', 'carrot', 'chicken'
}

CAUTION_INGREDIENTS = {
    'sugar', 'salt', 'milk', 'wheat', 'almonds', 'peanuts', 'honey'
}

AVOID_INGREDIENTS = {
    'high fructose corn syrup', 'monosodium glutamate', 'aspartame',
    'trans fat', 'artificial colors'
}

ALLERGENS = {'milk', 'almonds', 'peanuts', 'wheat'}

def analyze_ingredients(text: str):
    words = [w.strip().lower() for w in text.split(',') if w.strip()]
    safe = []
    caution = []
    avoid = []
    disclaimers = []

    for w in words:
        if w in AVOID_INGREDIENTS:
            avoid.append(w)
        elif w in CAUTION_INGREDIENTS:
            caution.append(w)
        elif w in SAFE_INGREDIENTS:
            safe.append(w)
        else:
            caution.append(w)  # default to caution for unknown

    if any(w in {'sugar', 'high fructose corn syrup'} for w in words):
        disclaimers.append('High Sugar Content: Limit consumption.')
    if any(w in ALLERGENS for w in words):
        allergens = ', '.join(sorted(w for w in words if w in ALLERGENS))
        disclaimers.append(f'Contains Potential Allergens ({allergens}).')
    if 'honey' in words:
        disclaimers.append('Not Recommended for Children Under Age 2.')

    if avoid:
        summary = '❌ Avoid: some ingredients are unsuitable for children.'
    elif caution:
        summary = '⚠️ Caution: review ingredients before serving.'
    else:
        summary = '✅ Safe: ingredients look okay.'

    return {
        'safe': safe,
        'caution': caution,
        'avoid': avoid,
        'disclaimers': disclaimers,
        'summary': summary
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('ingredients', '')
    result = analyze_ingredients(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
