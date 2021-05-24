from flask import Flask, request, jsonify, render_template
import re, string
from random import choice

app = Flask(__name__)

# We generate and validate according to MBI spec here
# https://www.cms.gov/medicare/new-medicare-card/understanding-the-mbi-with-format.pdf
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

mbiDesignations = {
    'C': 'a numeric value 1 through 9',
    'N': 'a numeric value 0 through 9',
    'A': 'an uppercase alphabetic value A through Z (minus S, L, O, I, B, Z)',
    'AN': 'an uppercase alpha-numeric value 0 through 9 and A through Z (minus S, L, O, I, B, Z)'
}

mbiFormat = ['C', 'A', 'AN', 'N', 'A', 'AN', 'N', 'A', 'A', 'N', 'N']

mbiGenerators = {
    'C': [str(i) for i in range(1, 10)],
    'N': [str(i) for i in range(10)],
    'A': [s for s in string.ascii_uppercase if s not in 'SLOIBZ'],
    'AN': [s for s in string.ascii_uppercase if s not in 'SLOIBZ'] + [str(i) for i in range(10)]
}

@app.route('/generate', methods=['GET'])
def generate():
    res = ''

    for c in mbiFormat:
        res += choice(mbiGenerators[c])

    return res

@app.route('/verify', methods=['POST'])
def verify():

    resp = {'valid': False, 'errors': []}

    if not request or not request.data or not request.is_json:
        return jsonify(resp)

    mbi = request.json.get('mbi')

    if mbi and type(mbi) == str:
        # https://stackoverflow.com/questions/47683221/regular-expression-for-medicare-mbi-number-format
        # regexp for quick validation. This seems like cheating and would not allow for returning a meaningful error message.
        # re.search(r"^\d(?![SLOIBZ])[A-Z]\d|(?![SLOIBZ])[A-Z]\d(?![SLOIBZ])[A-Z]\d|(?![SLOIBZ])[A-Z]\d(?![SLOIBZ])[A-Z](?![SLOIBZ])[A-Z]\d\d$", mbi)

        # automatically remove dashes and convert to uppercase, but warn the user
        if not mbi.isupper():
            resp['errors'].append('The MBI should only use uppercase letters.')
        if "-" in mbi:
            resp['errors'].append('The MBI should NOT include dashes.')

        if len(resp['errors']) > 0:
            mbi = mbi.upper().replace("-", "")
            resp['errors'].append(f'This MBI was converted to "{mbi}".')

        # check length first
        if len(mbi) != len(mbiFormat):
            resp['errors'] = [f'The MBI must be exactly {len(mbiFormat)} characters.']
        else:
            resp['valid'] = True

            # accumulate and return ALL formatting errors at once
            for i in range(len(mbiFormat)):
                if mbi[i] not in mbiGenerators[mbiFormat[i]]:
                    resp['valid'] = False
                    if 'errors' not in resp:
                        resp['errors'] = []
                    resp['errors'].append(f'{i + 1}{ {0: "st", 1: "nd", 2: "rd"}[i] if i < 3 else "th" } '
                                          f'character must be {mbiDesignations[mbiFormat[i]]}')

    return jsonify(resp)

@app.route("/")
def index():
    return render_template("./base.html")