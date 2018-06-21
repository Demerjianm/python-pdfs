#! /usr/bin/python
import os
import requests
from flask import Flask
from flask import jsonify
from flask import request
import pdfrw
app = Flask(__name__)

INVOICE_TEMPLATE_PATH = 'onboarding.pdf'
INVOICE_OUTPUT_PATH = "invoice.pdf"

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

@app.route('/hello')
def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
	template_pdf = pdfrw.PdfReader(input_pdf_path)
	annotations = template_pdf.pages[0][ANNOT_KEY]
	for annotation in annotations:
		if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
			if annotation[ANNOT_FIELD_KEY]:
				key = annotation[ANNOT_FIELD_KEY][1:-1]
				if key in data_dict.keys():
					annotation.update(
					    pdfrw.PdfDict(V='{}'.format(data_dict[key])))
	pdfrw.PdfWriter().write(output_pdf_path, template_pdf)




data_dict = {
    'Company Name Legal Name': 'Bostata',
    'Company Name DBA': 'company.io',
    'customer_email': 'joe@company.io',
    'invoice_number': '102394',
    'send_date': '2018-02-13',
    'due_date': '2018-03-13',
    'note_contents': 'Thank you for your business, Joe',
    'item_1': 'Data consulting services',
    'item_1_quantity': '10 hours',
    'item_1_price': '$200/hr',
    'item_1_amount': '$2000',
    'subtotal': '$2000',
    'tax': '0',
    'discounts': '0',
    'total': '$2000',
    'business_name_2': 'Bostata LLC',
    'business_email_address': 'hi@bostata.com',
    'here 1': 'Yes'
}

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo', methods=['GET'])
def get_tasks():
    print(INVOICE_OUTPUT_PATH)
    write_fillable_pdf(INVOICE_TEMPLATE_PATH, INVOICE_OUTPUT_PATH, data_dict) 
    return jsonify({'tasks': tasks})

@app.route('/todo/post', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    print(request.json['title'])
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)