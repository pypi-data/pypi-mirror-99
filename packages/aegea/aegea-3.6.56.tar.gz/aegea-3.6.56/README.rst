Aegea: Amazon Web Services Operator Interface
=============================================

*Aegea* is a command line interface (CLI) that provides a set of essential commands and terminal dashboards for
operators of Amazon Web Services (AWS) accounts. Aegea lets you build AMIs and Docker images using the
`cloud-init <http://cloudinit.readthedocs.io/>`_ config management package, manage config roles, launch and monitor
instances and services, and manage AWS resources including ELB, RDS, and AWS Batch. Aegea is designed to be used in
conjunction with the existing functionality of the `AWS CLI <https://aws.amazon.com/cli/>`_ and
`boto3 <https://boto3.readthedocs.io/>`_.

Installation
~~~~~~~~~~~~
::

   pip3 install aegea

Before you do this, you will also need to install some system library dependencies:

+--------------+-------------------------------------------------------------------------------------------------------+
| OS           | Command                                                                                               |
+==============+=======================================================================================================+
| Mac OS       | Install `Homebrew <https://brew.sh>`_, then run ``brew install python``.                              |
+--------------+-------------------------------------------------------------------------------------------------------+
| Ubuntu       | sudo apt-get update;                                                                                  |
|              | sudo apt-get install build-essential python3-{pip,dev,cffi} libffi-dev libssl-dev moreutils           |
+--------------+-------------------------------------------------------------------------------------------------------+
| Red Hat      | sudo yum install python3-devel python3-cffi openssl-devel moreutils                                   |
+--------------+-------------------------------------------------------------------------------------------------------+

Run ``aws configure`` to configure `IAM <https://aws.amazon.com/iam/>`_ access credentials that will be used by the
``aws`` and ``aegea`` commands. You can create a new IAM key at https://console.aws.amazon.com/iam/home#/users. See the
`AWS CLI documentation <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html>`_ for more details.

Aegea commands
~~~~~~~~~~~~~~
Below are some highlights from Aegea's suite of commands. Run ``aegea --help`` to see the full list of commands.

+----------------------------+-----------------------------------------------------------------------------------------+
| Command                    | Key functionality                                                                       |
+============================+=========================================================================================+
| `aegea ls`                 | List running EC2 instances                                                              |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea launch`             | Launch EC2 instances and specify options such as spot tenancy, AMI, instance type, etc. |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea ssh`, `aegea scp`   | Connect to running instances, transfer files using AWS Systems Manager or other options |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea batch`              | Submit, manage and monitor AWS Batch jobs                                               |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea ecs`                | Monitor ECS clusters and run Fargate tasks                                              |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea build-ami`          | Build EC2 AMIs using cloud-init configuration scripts                                   |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea build-docker-image` | Build AWS ECR docker images using Dockerfiles or cloud-init scripts                     |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea logs`               | Download AWS CloudWatch Logs contents using S3 export                                   |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea grep`               | Query AWS CloudWatch Logs contents using CloudWatch Logs Insights                       |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea cost`               | List AWS cost reports generated by AWS Cost Explorer                                    |
+----------------------------+-----------------------------------------------------------------------------------------+
| `aegea secrets`            | List and manage secrets stored in AWS Secrets Manager                                   |
+----------------------------+-----------------------------------------------------------------------------------------+

Aegea SSH
---------
The ``aegea ssh`` command (and its variant ``aegea scp``) is an SSH configuration wrapper that integrates with the
`AWS Systems Manager <https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html>`_ to provide
SSH connectivity to your instances without opening any inbound ports (if your instance OS is not configured with SSM,
use ``aegea ssh --no-ssm`` to open a direct connection). ``aegea ssh`` securely resolves instance addresses by name and
pre-fetches their public keys without the Trust-On-First-Use requirement. It also optionally integrates with the
`Bless <https://github.com/Netflix/bless>`_ package using the
`blessclient <https://github.com/chanzuckerberg/blessclient>`_ configuration convention.

Aegea Launch
------------
The ``aegea launch`` command launches EC2 instances. It has integrated support for Bless as well as DNS, runtime
cloud-init configuration, automatic location of Aegea-built AMIs or up-to-date Ubuntu or Amazon Linux AMIs, automatic
storage configuration, and other options.

Aegea Batch
-----------
The `AWS Batch <https://aws.amazon.com/batch>`_ API lets you run non-interactive command line workflows in Docker
containers, managing AWS ECS, Fargate, and EC2/Spot in your account on your behalf. Use the ``aegea batch`` family of
commands to interact with AWS Batch. The key command is ``aegea batch submit`` to submit jobs.

Run ``aegea batch submit --command "echo 'hello world'" --memory 4096 --vcpus 2 --watch``
to run a Batch job that requires 4 GB RAM and 2 cores to be allocated to the Docker container,
and executes the specified command.

You can also use ``aegea batch submit --execute FILE``. This will slurp up FILE (any type of shell script or ELF
executable) and execute it in the job's Docker container.

The concurrency and cost of your Batch jobs is governed by the "Max vCPUs" setting in your compute environment.
To change the capacity or other settings of the default compute environment used by ``aegea batch``, go to
https://console.aws.amazon.com/batch/home?region=us-east-1#/compute-environments, select "aegea_batch", and click
"Edit".

Batch and ECS Fargate
'''''''''''''''''''''
The `ECS Fargate <https://aws.amazon.com/fargate/>`_ API is an interface to the AWS container-based virtualization
platform, `Firecracker <https://github.com/firecracker-microvm/firecracker>`_. ECS Fargate allows you to run workloads
in fully managed containers: no instances run in your account; you are billed by the second of container use, and
containers start up within 10 seconds, compared to minutes for EC2 instances.

AWS Batch can run your jobs on either ECS Container Instances (EC2 instances connected to ECS that Batch manages in your
account) or directly in ECS Fargate containers. While Fargate containers are much faster to start, they have
`lower CPU and memory limits <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-cpu-memory-error.html>`_
of 4 CPUs and 30 GB RAM (compared to 96 CPUs and 768 GB RAM on EC2).

By default, ``aegea batch`` will create and use an AWS Batch compute environment and queue that uses ECS Fargate, but
you can control this by setting the ``--compute-type`` option to ``aegea batch create-compute-environment``.

Aegea also supports direct use of ECS Fargate without Batch via the ``aegea ecs run`` command. Most ``aegea batch``
semantics are applicable to ``aegea ecs``, which interacts with ECS via the "one shot"
`ECS RunTask <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ API.

Configuration management
~~~~~~~~~~~~~~~~~~~~~~~~
Aegea supports ingesting configuration from a configurable array of sources. Each source is a JSON or YAML file.
Configuration sources that follow the first source update the configuration using recursive dictionary merging. Sources
are enumerated in the following order (i.e., in order of increasing priority):

- Site-wide configuration source, ``/etc/aegea/config.yml``
- User configuration source, ``~/.config/aegea/config.yml``
- Any sources listed in the colon-delimited variable ``AEGEA_CONFIG_FILE``
- Command line options

**Array merge operators**: When loading a chain of configuration sources, Aegea uses recursive dictionary merging to
combine the sources. Additionally, when the original config value is a list, Aegea supports array manipulation
operators, which let you extend and modify arrays defined in underlying configurations. See
https://github.com/kislyuk/tweak#array-merge-operators for a list of these operators.

Building AMIs and Docker images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Aegea includes a lightweight configuration management system for building machine images based on
`cloud-init <http://cloudinit.readthedocs.io/>`_ (both Docker images and AMIs are supported).

.. image:: https://github.com/kislyuk/aegea/workflows/Tests/badge.svg
   :target: https://github.com/kislyuk/aegea/actions
.. image:: https://img.shields.io/pypi/v/aegea.svg
   :target: https://pypi.python.org/pypi/aegea
.. image:: https://img.shields.io/pypi/l/aegea.svg
   :target: https://pypi.python.org/pypi/aegea
.. image:: https://codecov.io/gh/kislyuk/aegea/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/kislyuk/aegea
