import os

import flask
from flask import Flask, render_template, make_response
from bin.frontend.forms import InsertForm
from dokanki.dokanki import Dokanki, UnsupportedFormatError


app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config['SECRET_KEY'] = 'secret_key'

from pathlib import Path

@app.route('/', methods=['GET', 'POST'])
def index():
    basedir = 'out'
    form = InsertForm(level=2)
    if form.validate_on_submit():

        name = os.path.normpath(flask.escape(form.name.data))
        test_path = (Path(basedir) / name).resolve()
        if test_path.parent != Path(basedir).resolve():
            raise Exception(f"Filename {test_path} is not in {Path(basedir)} directory")

        url = form.url.data
        id = hash(url)
        out = "{}/{}-{}.apkg".format(basedir, name, id)
        steps = [10, 30]
        level = 2

        dokgen = Dokanki(name, id, steps)
        try:
            dokgen.add_source(url, level)
            dokgen.extract().write(out)
        except (ConnectionError, FileNotFoundError, UnsupportedFormatError, RuntimeError) as err:
            raise Exception("Error occured while extracting flash cards")

        with open(out, 'rb') as f:
            content = f.read()
        response = make_response(content)
        response.headers['Content-Disposition'] = "attachment; filename={}.apkg".format(name)
        os.remove(out)
        return response
    return render_template('simple_gdocs_case.html', form=form)


if __name__ == '__main__':
    app.run(debug=False)
