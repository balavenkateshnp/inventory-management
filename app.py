from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')



@app.route('/info/<company>')
@login_required
def company_info(company):
    # Mock data for demonstration
    data = get_company_data(company)
    if data:
        return render_template('table.html', company=company, data=data)
    else:
        return render_template('404.html'), 404


def get_company_data(company):
    # Query the database for the company
    company_doc = db.company_data.find_one({"company": company.lower()})
    if not company_doc:
        return None

    # Combine headers and rows into a single list for rendering
    data = [company_doc['headers']] + company_doc['rows']
    return data


@app.route('/test/<company>')
def test_company_data(company):
    data = get_company_data(company)
    return {"company": company, "data": data}


def get_company_data(company):
    print(f"Fetching data for company: {company}")  # Debug message
    result = db.company_info.find_one({"company": company})
    print(f"Query result: {result}")  # Debugging output
    if result:
        return result["data"]
    return None