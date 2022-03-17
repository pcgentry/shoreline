from typing import Dict
from jinja2 import Template, Environment, FileSystemLoader

# Dictionary holding IP/port rules
rule_definitions = [
    {
        "name": "internal-only",
        "description": "Internal Network",
        "source_ip": "10.10.10.0/24",
        "protocol": "tcp",
        "port": 8080,
    },
    {
        "name": "seattle-office",
        "description": "Seattle Office Vpn",
        "source_ip": "72.172.213.172/32",
        "protocol": "tcp",
        "port": 443,
    },
]


def load_template(template):
    """
    Loads a .j2 file from '/templates' and return a Jinja2 template object.
    """
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    return env.get_template(template)


def file_save(file_name, file_contents):
    """
    Saves a file into output/ with file_contents.
    """
    with open("output/{0}".format(file_name), "w") as file:
        print(file_contents, file=file)


def tf_render(provider, rule_definitions=rule_definitions):
    """
    Renders network rules provided into Terraform modules using a Jinja2 object, output to the project dir.
    """
    if provider == "aws":
        file_name = "gcp_firewall.tf"
    elif provider == "gcp":
        file_name = "aws_security_group.tf"
    else:
        return False

    tf_template = load_template("{0}{1}".format(file_name, ".j2"))
    contents = tf_template.render(rule_definitions=rule_definitions)
    file_save(file_name, contents)
    return contents


# Render the files, and save them to the project dir.
print(tf_render(provider="aws"))
print(tf_render(provider="gcp"))

"""

notes:

* Run `python update_modules.py` to create terraform files.

** provider templates are located in the "templates/" directory
** output directory is "output/"

*** Full disclosure, this was just quick example code that I wrote for the assessment. There was no testing of the final
terraform modules. I know they are in the ballpark, but I don't have GCP or AWS resources handy to test with, so I took 
it as far as 'terraform plan', and that's it. 


1. How do you map the network rules to each platform i.e. how are
the rules applied on each platform and to what types of resources on
that platform?  

Most of my work to date has been on AWS, where the rules would be applied at the instance level to anything in EC2, and
can also be applied to some other Amazon resources like RDS or Elasticsearch. On the GCP side, and I am admittedly weaker
on this, I believe the firewall rules are a networking layer that sits between the instance and the network, and only
applies to instances in GCP.


2. What are the differences between the platforms from a networking
perspective? How does this impact your ability to create an abstraction
across the platforms?

Between AWS and GCP, there isn't a huge difference and an abstraction should be pretty straightforward. If I go back
and consider the original list, things change when you go into something like Kubernetes. Off the top of my head
I'm thinking about a multi-container pod in Kubernetes. All the pods in the container share a single networking interface, 
thus the same ip and port definitions and that could definitely make things more complicated. 

I also know that Kubernetes has the concept of NetworkPolicies, where you would create similar rules and apply them
via labels.

Creating an abstraction with this would depend a bit on how fine grained you want to control
things. If you just want to restrict out-of-network traffic to certain ports (80,443) vs. 
finer control between resources inside the network, it would get more complicated because of all the different paradigms 
in play.

3. How fine grained do you provide control over network flow? How
would you go about extending this for finer grain control?  Per instance?
Per group? Per network?

This question can get really complicated and could go a number of ways depending on the underlying need.
This particular script controls things on a group level. To make it per-instance, you could have other automation that
manages a security group or firewall per instance. At the network level, you would need to employ some other resource
like an ALB that only opens up specified ports, or some other form of proxy.
"""
