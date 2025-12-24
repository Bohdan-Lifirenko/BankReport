from pathlib import Path

from flask import Flask, jsonify, render_template, request

from src.services import FinancialService, DataPreparer
from src.services import DataLoader

app = Flask(__name__)

# Global service instances
data_loader = None
financial_service = None
data_preparer = None

def initialize_services():
    global data_loader, financial_service, data_preparer

    data_loader = DataLoader()
    data_loader.load_data("C:\\Users\\Robot_03\\Documents\\BankReport\\data\\firms.csv")
    print(data_loader.get_company_data(company_id="00236903"))

    financial_service = FinancialService(data_loader)

    data_preparer = DataPreparer(financial_service)

initialize_services()

@app.route('/')
def index():
    """Main page with search form"""
    return render_template('index.html')

@app.route('/search')
def search():
    """Search for company by tax ID"""
    tax_id = request.args.get('tax_id', '').strip()

    if not tax_id:
        return render_template('index.html', error="Please enter a tax ID")

    company_data = data_preparer.get_prepared_company_data(tax_id)

    if company_data is None:
        return render_template('index.html',
                             error=f"Company with tax ID {tax_id} not found")

    return render_template('company.html', company=company_data, tax_id=tax_id)

@app.route('/api/company/<tax_id>')
def api_company(tax_id):
    """API endpoint for company data (JSON)"""
    company = data_preparer.get_prepared_company_data(tax_id)

    if company is None:
        return jsonify({'error': 'Company not found'}), 404

    return jsonify(company)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)



