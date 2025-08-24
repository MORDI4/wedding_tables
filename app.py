from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response

from forms import TableForm
from models import tables

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route('/api/v1/tables', methods=['GET'])
def tables_list_api_v1():
    return jsonify(tables.all())

@app.route('/api/v1/tables/<int:table_id>', methods=['GET'])
def get_table(table_id):
    table = tables.get(table_id)
    if not table:
        abort(404)
    return jsonify({"table": table})

@app.route('/api/v1/tables/', methods=['POST'])
def create_table():
    if not request.json or not 'guests' in request.json:
        abort(400)
    table = {
        'table_num': tables.all()[-1]['table_num'] + 1,
        'guests': request.json['guests']
    }
    tables.create(table)
    return jsonify({'table': table}), 201

@app.route('/api/v1/tables/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    result = tables.delete(table_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route('/api/v1/tables/<int:table_id>', methods=['PUT'])
def update_table(table_id):
    table = tables.get(table_id)
    if not table:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if 'guests' in data and not isinstance(data.get('guests'), str):
        abort(400)
    table['guests'] = data.get('guests', table['guests'])
    tables.update(table_id, table)
    return jsonify({'table': table})

        

@app.route('/tables/', methods=['GET', 'POST'])
def tables_list():
    form = TableForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            tables.create(form.data)
            tables.save_all()
        return redirect(url_for("tables_list"))
    
    return render_template("wedding_tables.html", form=form, tables=tables.all(), error=error)

@app.route('/tables/<int:table_num>', methods=['GET', 'POST'])
def table_details(table_num):
    table = tables.get(table_num)
    form = TableForm(data=table)

    if request.method == 'POST':
        if form.validate_on_submit():
            tables.update(table_num, form.data)
        return redirect(url_for("tables_list"))
    return render_template("table.html", form=form, table_num=table_num)

if __name__ == '__main__':
    app.run(debug=True)