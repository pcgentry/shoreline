# Shoreline Assessment

Design a data structure to represent a allowing or denying traffic by CIDR block
and port range.  Describe this structure in the comments of your code.

Implement a function that takes a set of your structures and a target cloud
platform and applies these rules to the network environment of that platform. 
Please implement your solution for two of the following platforms: AWS, GCP,
Azure, VMware, or Kubernetes.  

# notes:

The bulk of this project is in update_modules.py. It just takes a python dictionary, maps the values to
Terraform files using Jinja2, then writes them to disk.

* Run `python update_modules.py` to create terraform files.
* provider templates are located in the "templates/" directory
* output directory is "output/"

*** Full disclosure, this was just quick example code that I wrote for the assessment. There was no testing of the final
terraform modules. I know they are in the ballpark, but I don't have GCP or AWS resources handy to test with, so I took 
it as only far as 'terraform plan'.