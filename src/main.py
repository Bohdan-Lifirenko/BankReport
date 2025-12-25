import traceback
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from src.services import FinancialService, DataPreparer
from src.services import DataLoader

app = Flask(__name__)

# Global service instances
financial_service = None
data_preparer = None

def initialize_services():
    global financial_service, data_preparer
    try:
        financial_service = FinancialService(
            "C:\\Users\\Robot_03\\Documents\\BankReport\\data\\firms.csv",
            "C:\\Users\\Robot_03\\Documents\\BankReport\\data\\fin_values.csv"
        )
        print(financial_service.get_company_data(company_id="00236903"))
        print(financial_service.get_balance_data("00236903", "2021-12-31"))

        data_preparer = DataPreparer(financial_service)

    except Exception as e:
        print(f"Error initializing services: {e}")
        traceback.print_exc()


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

    company_data = data_preparer.get_company_data(tax_id)

    if company_data is None:
        return render_template('index.html',
                             error=f"Company with tax ID {tax_id} not found")

    # Get available dates for financial data
    available_dates = financial_service.get_available_dates(tax_id)

    return render_template('company.html',
                          company=company_data,
                          tax_id=tax_id,
                          available_dates=available_dates)

@app.route('/company/<tax_id>')
def company(tax_id):
    """Display company details page"""
    tax_id = tax_id.strip()
    company_data = data_preparer.get_company_data(tax_id)

    if company_data is None:
        return render_template('error.html',
                             error_message=f"Company with tax ID {tax_id} not found")

    # Get available dates for financial data
    available_dates = financial_service.get_available_dates(tax_id)

    return render_template('company.html',
                          company=company_data,
                          tax_id=tax_id,
                          available_dates=available_dates)

@app.route('/api/company/<tax_id>')
def api_company(tax_id):
    """API endpoint for company data (JSON)"""
    company = data_preparer.get_prepared_company_data(tax_id)

    if company is None:
        return jsonify({'error': 'Company not found'}), 404

    return jsonify(company)

@app.route('/api/balance/<tax_id>')
def api_balance(tax_id):
    """
    API endpoint for balance sheet data.

    Returns JSON with assets, equity, and liabilities for a specific date.
    Format: {"assets": float, "equity": float, "liabilities": float, "date": "YYYY-MM-DD"}

    Args:
        tax_id: Company tax ID (EDRPOU)

    Query Parameters:
        date: Financial reporting date in YYYY-MM-DD format (required)
    """
    # Strip whitespace
    tax_id = tax_id.strip()

    # Check if company exists
    if not financial_service.company_exists(tax_id):
        return jsonify({
            'error': 'Company not found',
            'message': f'Company with EDRPOU {tax_id} not found'
        }), 404

    # Get date parameter
    date = request.args.get('date')

    if not date:
        return jsonify({
            'error': 'Missing parameter',
            'message': 'Date parameter is required'
        }), 400

    # Get balance data
    balance_data = financial_service.get_balance_data(tax_id, date)

    return jsonify(balance_data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)



