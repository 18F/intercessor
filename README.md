# DATA Act pilot

The DATA Act requires the Department of Treasury and the Office of Management and Budget (OMB) to standardize and publish federal spending data online. 

This repository contains code for a Small Business Administration (SBA) pilot project that:
* Maps agency financial and award data to DATA Act elements,
* Translates them to a uniform DATA Act format, and
* Validates the results.

This work is a small experiment using real agency data. The diagrams and other artifacts here do not represent official DATA Act guidance or policy, and the code does not represent an official DATA Act product.

Thanks to the SBA for leading the way and lending their time and expertise to this effort.

## Overview

This project is an exploration of the DATA Act data submission process from the agency perspective. The repository is learning in progress and subject to change. Its goal is to clarify the steps and tools agencies need as they undertake DATA Act compliance.

View progress and upcoming work are on our task board: https://waffle.io/18F/data-act-pilot.

Below is an overview of the process.

![DATA Act pilot process flow](https://raw.githubusercontent.com/18F/data-act-pilot/master/SBA%20pilot%20process.png)

## Glossary
* **JAAMS**: SBA's financial system
* **Prism**: SBA's grants and contracts system
* **SAM**: _System for Award Management_, a federal, government-wide system that contains information about entities (businesses, individuals, or government agencies) that do business with the federal government
* **DATA Act Schema (_Schema_)**: The generic model of the relationships between the data elements that agencies must report to Treasury as part of the DATA Act and previous transparency legislation.

## Resources
Below, we've identified some useful resources and artifacts for people working on this pilot.

* The OMB published [finalized data element definitions](https://max.gov/maxportal/assets/public/offm/DataStandardsFinal.htm "Finalized Data Act Element Definitions").
* Mapping document: This is the document that maps specific SBA JAAMS and Prism attributes to their DATA Act schema counterparts. It's not currently public and resides in the data folder.
* The [SBA entity relationship diagram](https://raw.githubusercontent.com/18F/data-act-pilot/master/assets/images/jaams-prism-data-act-mapping.png "SBA ERD") shows the relationships between the JAAMS and Prism tables that contain the fields being mapped to the DATA Act schema.
* Explore [research questions](https://github.com/18F/data-act-pilot/labels/research%20questions "open issues labeled as 'research'") (and some answers) that have emerged during the pilot. Answered questions are [stored as "closed" in GitHub](https://github.com/18F/data-act-pilot/issues?q=label%3A%22research+questions%22+is%3Aclosed "closed issues labeled as 'research'").
* The [DATA Act Playbook](https://www.usaspending.gov/Documents/Summary%20of%20DATA%20Act%20Playbook.pdf "DATA Act Playbook") contains recommended steps for agencies to fulfill DATA Act requirements.
* Pilot screencast:
    * [Mac and newer versions of Windows](assets/screencast/data_act_pilot_screencast_sept_2015.mp4 "Pilot screencast, .mp4 version")
    * [Older versions of Windows](assets/screencast/data_act_pilot_screencast_sept_2015.mp4 "Pilot screencast, .avi version")

## Data
For the first iterations of this pilot, we're using SBA 2014 grants data.

Because it contains personally identifiable information (PII), the SBA data is not included in the code repository. The data includes:

* Extracts from JAAMS, SBA's financial system
* Extracts from Prism, SBA's awards system

These extracts will be supplemented by calls to the [SAM API](https://gsa.github.io/sam_api/sam/index.html), which contains details about entities (businesses and individuals) that receive federal funds.

### Data structure
For reference, the data accessed in the code are structured as follows. The text files are extracts from their respective underlying databases and have been provided to the team in comma-quote delimited format.

* `data/jaams`: text file extracts from JAAMS
* `data/jaams/sql`: sql for JAAMS table creation/joins
* `data/prism`: text file extracts from Prism
* `data/prism/sql`: sql for Prism table creation/joins

### Run the processors
These directions assume that the project is already installed on your system. If you don't have the project installed and running, please see [INSTALL.md](INSTALL.md "Installation instructions").

There are two steps for converting SBA data to DATA Act input format.

The first reads raw text files from SBA (JAAMS and Prism), joins the awards and financial data, and writes it to four standardized DATA Act files.

The second validates the four files against the pilot's working subset of business rules, found here: [sba-business-rules.md](sba-business-rules.md "SBA Business Rules").

Example usage (to run both processes):

`python processors/process_source.py -o data/data_act.csv`

`python processors/validattor [micah to fill in]`

### Query the SAM API
The SAM data utility queries the SAM API based on DUNS number and returns a JSON version of the response. A list of requested fields can be supplied to limit the response to only the data required. A full list of available fields and their definitions are available at [SAM field definitions](http://gsa.github.io/sam_api/sam/fields.html).

Example usage:

To get all fields for a given DUNS:

`python processors/get_sam_data.py 8291938660000`

To limit response to a list of fields:

`python processors/get_sam_data.py 8291938660000 --fields registrationDate legalBusinessName samAddress`


### Questions?

Because this is a small experiment and a tiny piece of the overall DATA Act implementation, 18F is unable to speak with vendors individually about the work. We welcome the DATA Act community to follow the project and contribute here.
