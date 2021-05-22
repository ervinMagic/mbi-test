from flask import Flask, request, jsonify, render_template
import re, string
from random import choice

app = Flask(__name__)

# according to MBI spec
# Position 1 – numeric values 1 thru 9
# Position 2 – alphabetic values A thru Z (minus S, L, O, I, B, Z)
# Position 3 – alpha-numeric values 0 thru 9 and A thru Z (minus S, L, O, I, B, Z)
# Position 4 – numeric values 0 thru 9
# Position 5 – alphabetic values A thru Z (minus S, L, O, I, B, Z)
# Position 6 – alpha-numeric values 0 thru 9 and A thru Z (minus S, L, O, I, B, Z)
# Position 7 – numeric values 0 thru 9
# Position 8 – alphabetic values A thru Z (minus S, L, O, I, B, Z)
# Position 9 – alphabetic values A thru Z (minus S, L, O, I, B,Z)
# Position 10 – numeric values 0 thru 9
# Position 11 – numeric values 0 thru 9

mbiGenerators = {
    'C': [str(i) for i in range(1, 10)],
    'N': [str(i) for i in range(10)],
    'A': [s for s in string.ascii_uppercase if s not in 'SLOIBZ'],
    'AN': [s for s in string.ascii_uppercase if s not in 'SLOIBZ'] + [str(i) for i in range(10)]
}

mbiFormat = ['C', 'A', 'AN', 'N', 'A', 'AN', 'N', 'A', 'A', 'N', 'N']

mbiDesignations = {
    'C': 'numeric values 1 through 9',
    'N': 'numeric values 0 through 9',
    'A': 'uppercase alphabetic values A through Z (minus S, L, O, I, B, Z)',
    'AN': 'uppercase alpha-numeric values 0 through 9 and A through Z (minus S, L, O, I, B, Z)'
}

@app.route('/generate', methods=['GET'])
def generate():
    res = ''

    for c in mbiFormat:
        res += choice(mbiGenerators[c])

    return res

@app.route('/verify', methods=['POST'])
def verify():

    mbi = request.json.get('mbi')
    resp = {'valid': False}

    if mbi:
        # https://stackoverflow.com/questions/47683221/regular-expression-for-medicare-mbi-number-format
        # regexp for quick validation. This seems like cheating and would not allow for returning a meaningful error message.
        # re.search(r"^\d(?![SLOIBZ])[A-Z]\d|(?![SLOIBZ])[A-Z]\d(?![SLOIBZ])[A-Z]\d|(?![SLOIBZ])[A-Z]\d(?![SLOIBZ])[A-Z](?![SLOIBZ])[A-Z]\d\d$", mbi)

        if len(mbi) != len(mbiFormat):
            resp['valid'] = False
            resp['errors'] = [f'The MBI must be exactly {len(mbiFormat)} characters.']
        else:
            resp['valid'] = True

            for i in range(len(mbiFormat)):
                if mbi[i] not in mbiGenerators[mbiFormat[i]]:
                    resp['valid'] = False
                    if 'errors' not in resp:
                        resp['errors'] = []
                    resp['errors'].append(f'{i + 1}{ {0: "st", 1: "nd", 2: "rd"}[i] if i < 3 else "th" } character must be {mbiDesignations[mbiFormat[i]]}')

    return jsonify(resp)

@app.route("/")
def index():
    return render_template("./base.html")