# hive-builder

hive-builder is a tool for building a site that operates docker containers across multiple servers. By using the cluster function of the docker swarm mode and the disk redundancy function of the drbd9, without using Kubernetes, you can build a site with a simple configuration.
The hive houses the swarm of microservice and manages them.

- A method of selecting leaders in server elections prevents split brain and does not require centralized control by a controller
- The cluster function of docker swarm mode ensures high availability
- You can migrate a container between servers, even that have data volumes, by mirroring disks with drbd that have auto promotion function
- Sites can be built on IaaS such as AWS by launching the command only once
- Container contents can be described with ansible role
- Initial data can be loaded when site is launched
- Have a private repository server in the site and store container images
- Have Zabbix server in the site and monitor the operation
- You can define 3 stages of private, staging, production in one inventory and build a site for each stage

For details, see [the document](https://hive-builder.readthedocs.io/) (Sorry, there are only Japanese ones now).
