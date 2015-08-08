
import csv
import logging
import os
import sys
from functools import wraps

from flask import Flask, request, Response, url_for, render_template

from validator.validator import Validator

app = Flask(__name__)
username = os.getenv('WEB_USERNAME', '')
password = os.getenv('WEB_PASSWORD', '')

RULES_DIR = './rules/'

ALLOWED_EXTENSIONS = ['csv']
# TODO create this dict dynamically by reading csv schema files.
VALIDATION = {
    'appropriation.csv': [
        'AllocationTransferAgencyIdentifier',
        'AgencyIdentifier',
        'BeginningPeriodOfAvailability',
        'EndingPeriodOfAvailability',
        'AvailabilityTypeCode',
        'MainAccountCode',
        'BudgetAuthorityAppropriatedAmount',
        'UnobligatedAmount',
        'OtherBudgetaryResourcesAmount'
        ],
    'object_class_program_activity.csv': [
        'AllocationTransferAgencyIdentifier',
        'AgencyIdentifier',
        'BeginningPeriodOfAvailability',
        'EndingPeriodOfAvailability',
        'AvailabilityTypeCode',
        'MainAccountCode',
        'ObjectClass',
        'ObligatedAmount',
        'ProgramActivity',
        'OutlayAmount'
        ],
    'award.csv': [
        'piidPrefix',
        'piidAwardYear',
        'piidAwardType',
        'piidAwardNumber',
        'FainAwardNumber',
        'AwardDescription',
        'AwardModAmendmentNumber',
        'ParentAwardIDprefix',
        'ParentAwardYear',
        'ParentAwardType',
        'ParentAwardNumber',
        'RecordType',
        'ActionDateDay',
        'ActionDateMonth',
        'ActionDateYear',
        'TypeOfAction',
        'ReasonForModification',
        'TypeOfContractPricing',
        'idvType',
        'ContractAwardType',
        'AssistanceType',
        'FederalPrimeAward',
        'NonFederalFundingAmount',
        'CurrentTotalFundingObligationAmount',
        'CurrentTotalValueAwardAmount',
        'FaceValueLoanGuarantee',
        'PotentialTotalValueAwardAmount',
        'AwardingAgencyName',
        'AwardingAgencyCode',
        'AwardingSubTierAgencyName',
        'AwardingSubTierAgencyCode',
        'AwardingOfficeName',
        'AwardingOfficeCode',
        'FundingAgencyName',
        'FundingAgencyCode',
        'FundingSubTierAgencyName',
        'FundingOfficeName',
        'FundingOfficeCode',
        'RecipientLegalEntityName',
        'RecipientDunsNumber',
        'RecipientUltimateParentUniqueId',
        'RecipientUltimateParentLegalEntityName',
        'RecipientLegalEntityAddressStreet1',
        'RecipientLegalEntityAddressStreet2',
        'RecipientLegalEntitylCityName',
        'RecipientLegalEntityStateCode',
        'RecipientLegalEntityZip',
        'RecipientLegalEntityZip+4',
        'RecipientLegalEntityPostalCode',
        'RecipientLegalEntityCongresionalDistrict',
        'RecipientLegalEntityCountryCode',
        'RecipientLegalEntityCountryName',
        'HighCompOfficer1FirstName',
        'HighCompOfficer1MiddleInitial',
        'HighCompOfficer1LastName',
        'HighCompOfficer2FirstName',
        'HighCompOfficer2MiddleInitial',
        'HighCompOfficer2LastName',
        'HighCompOfficer3FirstName',
        'HighCompOfficer3MiddleInitial',
        'HighCompOfficer3LastName',
        'HighCompOfficer4FirstName',
        'HighCompOfficer4MiddleInitial',
        'HighCompOfficer4LastName',
        'HighCompOfficer5FirstName',
        'HighCompOfficer5MiddleInitial',
        'HighCompOfficer5LastName',
        'HighCompOfficer1Amount',
        'HighCompOfficer2Amount',
        'HighCompOfficer3Amount',
        'HighCompOfficer4Amount',
        'HighCompOfficer5Amount',
        'BusinessType',
        'NAICS_Code',
        'NAICS_Description',
        'CFDA_Code',
        'CFDA_Description',
        'PeriodOfPerfStartDay',
        'PeriodOfPerfStartMonth',
        'PeriodOfPerfStartYear',
        'PeriodOfPerfCurrentEndDay',
        'PerioOfPerfCurrentEndMonth',
        'PeriodOfPerfCurrentEndYear',
        'PeriodOfPerfPotentialEndDay',
        'PeriodOfPerfPotentialEndMonth',
        'PeriodOfPerfPotentialEndYear',
        'OrderingPeriodEndDay',
        'OrderingPeriodEndMonth',
        'OrderingPeriodEndYear',
        'PlaceOfPerfCity',
        'PlaceOfPerfState',
        'PlaceOfPerfCounty',
        'PlaceOfPerfZip+4',
        'PlaceOfPerfCongressionalDistrict',
        'PlaceOfPerfCountryName'
        ],
    'award_financial.csv': [
        'AllocationTransferAgencyIdentifier',
        'AgencyIdentifier',
        'BeginningPeriodOfAvailability',
        'EndingPeriodOfAvailability',
        'AvailabilityTypeCode',
        'MainAccountCode',
        'ParentAwardIDprefix',
        'ParentAwardYear',
        'ParentAwardType',
        'ParentAwardNumber',
        'FainAwardNumber',
        'AwardModAmendmentNumber',
        'ObjectClass',
        'TransactionObligatedAmount'
        ]
}

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
log.addHandler(ch)

def allowed_file(filename):
    """Checks if the filename is an allowed type of file.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def validate_headers(csv_file, correct_headers):
    reader = csv.reader(csv_file)
    try:
        headers = reader.next()
    except StopIteration:
        return False

    return sorted(headers) == sorted(correct_headers)

def check_file(file, valid_headers, template_name):
    error = {}
    error['template_name'] = template_name
    if not file:
        error['message'] = 'File was not uploaded'
        return error
    error['filename'] = file.filename or ''
    if not allowed_file(file.filename):
        error['message'] = 'File is of incorrect type'
        return error
    if not validate_headers(file, valid_headers):
        error['message'] = 'File headers are incorrect'
        return error

    return None

def validate_files(files):
    validator = Validator(
        files['appropriation.csv'],
        files['object_class_program_activity.csv'],
        files['award.csv'],
        files['award_financial.csv'],
        RULES_DIR)
    return validator.results

def check_auth(ausername, apassword):
    """Checks that the username / password combination is valid for basic
    HTTP auth.
    """
    return ausername == username and apassword == password

def authenticate():
    return Response(
        'Could not verify your access level for this url.\n'
        'Please login with username and password', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def hello_world():
    if request.method == 'POST':
        correct_files = []
        files = request.files
        file_errors  = []
        checked_files = {
            'appropriation.csv': None,
            'object_class_program_activity.csv': None,
            'award.csv': None,
            'award_financial.csv': None
                }
        for name in VALIDATION.keys():
            error = check_file(files[name], VALIDATION[name], name)
            if error:
                file_errors.append(error)
            else:
                checked_files[name] = files[name].stream

        validation_errors = validate_files(checked_files)

        correct_files.append({
            'filename': files[name].filename,
            'template_name': name
            })

        return render_template('home.html',
                correct_files=correct_files,
                file_errors=file_errors,
                validation_errors=validation_errors)

    return render_template('home.html')

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
