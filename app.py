from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate():

    #generate according to spec
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

    return "1EG4TE5MK73"


@app.route('/verify', methods=['POST'])
def verify(m):

    mbi = m #request.form.get('mbi')
    print(mbi)

    # https://stackoverflow.com/questions/47683221/regular-expression-for-medicare-mbi-number-format
    # regexp for quick validation

    if mbi:
        match = re.search(r"^\d(?![SLOIBZ])[A-Z]\d|(?![SLOIBZ])[A-Z]\d(?![SLOIBZ])[A-Z]\d|(?![SLOIBZ])[A-Z]\d(?![SLOIBZ])[A-Z](?![SLOIBZ])[A-Z]\d\d$", mbi)
        if match is not None:
            return True
        else:
            #if it fails iterate char by char to find the issue and return a meaningful message
            return False

@app.route("/")
def index():
    return render_template("base.html")