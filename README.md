# Intercessor
Yet another DATA Act repository. This one contains code that translates agency data to a uniform DATA act format.

## Data
Because it contains PII, the Small Business Administration (SBA) data used for this project is not included in the code repository. The data includes:

* Extracts from JAAMS, the financial system that includes a record of SBA's payments
* Exracts from Prism, the Oracle Financial System that contains information about SBA awards (grants, loans, and contracts)

These extracts will be supplemented by calls to the [SAM API](https://gsa.github.io/sam_api/sam/index.html), which contains details about entities (businesses and individuals) that receive federal funds.

### Data Structure
For reference, the data accessed in the code are structured as follows:

* `data/data_act_prism_grants_fy14.csv`: prism data combined into a single .csv (this is what we're using but the smaller files in data/prism are included for reference)
* `data/jaams`: text file extracts from JAAMS
* `data/jaams/sql`: sql for jaams table creation/joins
* `data/prism`: text file extracts from Prism
* `data/prism/sql`: prism create table scripts
