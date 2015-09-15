# Installation

The following installation steps should work for Windows, Mac, and Linux.

## Using VirtualBox and Vagrant

This is the easiest way to get the code up and running on any platform that can run [VirtualBox](https://www.virtualbox.org/ "VirtualBox") virtualization software.

From the command line:

1. Clone the project repository from GitHub to your local environment:

        $ git clone git@github.com:18F/data-act-pilot.git
    **Note:** if you don't have a GitHub account and want to get a read-only version of the code, use this command instead:

        $ git clone git://github.com/18F/data-act-pilot.git

2. Change to the project directory:

        $ cd data-act-pilot

3. Unzip a copy of the data directory and files. These aren't included with the code because they contain personally identifiable information (PII). We're working on putting up a secure cloud version that credentialed users can access. For now, request a secure transmission of the data.zip file from a member of the project team. Copy data.zip to the project's root directory and unzip it. The resulting directory structure should look like this:

          data-act-pilot  
            /assets  
            /data  
              /jaams  
                AP_CHECKS_ALL.txt  
                AP_INVOICE_DISTRIBUTIONS_ALL.txt  
                ...  
                /sql  
              /prism  
                association.txt  
                cfda.txt  
                ...  
                /sql  
            /mappings  
            /processor  
            /schema  
            .gitignore  
            ...  

4. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads "VirtualBox downloads")  

5. Install [Vagrant](http://www.vagrantup.com/downloads.html "Vagrant downloads")  

6. Open _bootstrap.sh_ (in the project root directory), find the string that reads `YOUR_SAM_API_KEY`, and replace it with your SAM API key. If you don't have a key, you can get one in less than a minute by signing up at [https://gsa.github.io/sam_api/sam/key](https://gsa.github.io/sam_api/sam/key "SAM API Key").

        echo "export DOT_GOV_API_KEY='YOUR_SAM_API_KEY'" >> ~/.bashrc

7. From project root directory, run:

         $ vagrant up

8. Once the VM is fully started and provisioned (~15 minutes), connect to it with:

        $ vagrant ssh

9. The project directory on your host machine is shared with the VM at `/vagrant`. Navigate there to run create sample SBA DATA Act files.

        $ cd /vagrant
        $ workon data-act-pilot
        $ python processors/process_source.py -o data/data_act.csv

Because the project directory on your host machine is shared with the VM, you can use your existing tools (IDE, browser, etc.), and everything will be synced with the VM.
