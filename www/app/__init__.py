from flask import Flask
from flask import render_template, flash, request, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import sys, requests, json

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'correct-horse-battery-staple'

class HCPForm(FlaskForm):
    organization_id = StringField('Organization ID', validators=[DataRequired()])
    project_id      = StringField('Project ID', validators=[DataRequired()])
    client_id       = StringField('HCP Client ID', validators=[DataRequired()])
    client_secret   = PasswordField('HCP Client Secret', validators=[DataRequired()])
    save_hcp_data   = SubmitField('Save')

class TFCForm(FlaskForm):
    tfc_organization = StringField('TFC Organization', validators=[DataRequired()])
    tfc_workspace    = StringField('TFC Workspace Name', validators=[DataRequired()])
    tfc_token        = PasswordField('TCF Token', validators=[DataRequired()])
    save_tfc_data    = SubmitField('Save')

@app.route('/')
def hello_world():
  session.clear()
  writeToLocalConfigFile()
  return render_template('splash.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/challenges')
def challenges():
  return render_template('challenges.html')

@app.route('/health')
def health():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/one')
def one():
  return render_template('one.html')

@app.route('/two')
def two():
  return render_template('two.html')

@app.route('/three')
def three():
  return render_template('three.html')

@app.route('/setup_hcp', methods=('GET', 'POST'))
def setup_hcp():

  hcp_form = HCPForm()

  if request.method == 'POST':

    if hcp_form.validate_on_submit() and (hcp_form.client_id.data and hcp_form.client_secret.data):
      session['organization_id'] = hcp_form.organization_id.data
      session['project_id']      = hcp_form.project_id.data
      session['hcp_client_id']   = hcp_form.client_id.data
      session['hcp_client_secret'] = hcp_form.client_secret.data
      
      validation = getHCPBearerToken()

      if (validation.status_code == 200):  
          session['hcp_client_token'] = validation.json()["access_token"]
      else:
          session['hcp_client_token'] = "Invalid Credentials."

      writeToLocalConfigFile()

  return render_template('setup_hcp.html', 
      organization_id=session.get('organization_id'),
      project_id=session.get('project_id'),
      client_id=session.get('hcp_client_id'), 
      client_secret=session.get('hcp_client_secret'),
      client_token=session.get('hcp_client_token'),
      hcp_form=hcp_form)

@app.route('/setup_tfc', methods=('GET', 'POST'))
def setup_tfc():
  tfc_form = TFCForm()

  if request.method == 'POST':
    if tfc_form.validate_on_submit() and (tfc_form.tfc_organization.data and tfc_form.tfc_workspace.data and tfc_form.tfc_token.data):
      session['tfc_organization'] = tfc_form.tfc_organization.data
      session['tfc_workspace'] = tfc_form.tfc_workspace.data
      session['tfc_token'] = tfc_form.tfc_token.data
      writeToLocalConfigFile()

  return render_template('setup_tfc.html',
      tfc_organization = session.get('tfc_organization'),
      tfc_workspace    = session.get('tfc_workspace'), 
      tfc_token        = session.get('tfc_token'), 
      tfc_form         = tfc_form)

@app.route('/get_form_status')
def get_form_status():
  form_name = request.args.get('form_name')
  if form_name == "hcp_form":
    if session.get('hcp_client_id') is None or session.get('hcp_client_secret') is None:
      return {"ready": False}
    else:
      return {"ready": True}
  elif form_name == "tfc_form":
    if session.get('tfc_workspace') is None or session.get('tfc_token') is None:
      return {"ready": False}
    else:
      return {"ready": True}
  return {"ready": False}

@app.route('/track_auth')
def track_auth():
  return render_template('track_auth.html')

def writeToLocalConfigFile():

  fo = open("hcp_credentials", "w")
  
  filebuffer = "\nexport HCP_ORGANIZATION_ID=\"{}\"\nexport HCP_PROJECT_ID=\"{}\"".format(session.get('organization_id'), session.get('project_id'))
  fo.writelines(filebuffer)
  
  filebuffer = "\nexport HCP_CLIENT_ID=\"{}\"\nexport HCP_CLIENT_SECRET=\"{}\"\nexport HCP_CLIENT_TOKEN=\"{}\"".format(session.get('hcp_client_id'), session.get('hcp_client_secret'), session.get('hcp_client_token'))
  fo.writelines(filebuffer)
  
  filebuffer = "\nexport TFE_ORG=\"{}\"\nexport TFE_TOKEN=\"{}\"\nexport TFE_WORKSPACE=\"{}\"\n".format(session.get('tfc_organization'), session.get('tfc_token'), session.get('tfc_workspace'))
  fo.writelines(filebuffer)
  
  fo.close()
  return

def getHCPBearerToken():
  auth    = (session.get('hcp_client_id'), session.get('hcp_client_secret'))
  url     = "https://auth.hashicorp.com/oauth/token"
  headers = {"Content-Type": "application/json"}
  data    = { "grant_type": "client_credentials",
              "audience": "https://api.hashicorp.cloud" }
  response = requests.post(url, json = data, auth = auth, headers = headers)

  return response


@app.route('/uc-01-challenge')
def uc_01_challenge():
  return render_template('uc-01-challenge.html')

@app.route('/uc-01-description')
def uc_01_description():
  return render_template('uc-01-description.html')

@app.route('/uc-01-example')
def uc_01_example():
  return render_template('uc-01-example.html')

@app.route('/uc-01-section-01')
def uc_01_section_01():
  return render_template('uc-01-section-01.html')

@app.route('/uc-01-section-02')
def uc_01_section_02():
  return render_template('uc-01-section-02.html')

@app.route('/uc-01-section-03')
def uc_01_section_03():
  return render_template('uc-01-section-03.html')

@app.route('/uc-01-summary')
def uc_01_summary():
  return render_template('uc-01-summary.html')

@app.route('/uc-02-challenge')
def uc_02_challenge():
  return render_template('uc-02-challenge.html')

@app.route('/uc-02-description')
def uc_02_description():
  return render_template('uc-02-description.html')

@app.route('/uc-02-workflow')
def uc_02_workflow():
  return render_template('uc-02-workflow.html')

@app.route('/uc-02-summary')
def uc_02_summary():
  return render_template('uc-02-summary.html')

@app.route('/uc-03-challenge')
def uc_03_challenge():
  return render_template('uc-03-challenge.html')

@app.route('/uc-03-description')
def uc_03_description():
  return render_template('uc-03-description.html')

@app.route('/uc-03-workflow')
def uc_03_workflow():
  return render_template('uc-03-workflow.html')

@app.route('/uc-03-summary')
def uc_03_summary():
  return render_template('uc-03-summary.html')
