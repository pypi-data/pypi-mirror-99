vagrant-devstack-Kuryr-Kubernetes
=================================

Getting started
---------------

A Vagrant based kuryr,neutron,keystone,docker and kubernetes system.

Steps to try vagrant image:

 1. Install Vagrant on your local machine. Install one of the current
    providers supported: VirtualBox, Libvirt or Vagrant
 2. Git clone kuryr-kubernetes repository.
 3. Run `cd kuryr-kubernetes/contrib/vagrant`
 4. Run `vagrant up`
    It will take from 10 to 60 minutes, depending on your internet speed.
    Vagrant-cachier can speed up the process [1].
 5. `vagrant ssh`

At this point you should have experimental kubernetes (etcdv3, k8s-apiserver,
k8s-controller-manager, k8s-scheduler, kubelet and kuryr-controller), docker,
kuryr, neutron, keystone, placement, nova, octavia all up, running and pointing
to each other. Pods and services orchestrated by kubernetes will be backed by
kuryr+neutron and Octavia. The architecture of the setup can be seen at [2].

References:
[1] http://fgrehm.viewdocs.io/vagrant-cachier/
[2] https://docs.openstack.org/developer/kuryr-kubernetes/devref/kuryr_kubernetes_design.html

Vagrant Options available
-------------------------

You can set the following environment variables before running `vagrant up` to modify
the definition of the Virtual Machine spawned:

 * **VAGRANT\_KURYR\_VM\_BOX**: To change the Vagrant Box used. Should be available in
   [atlas](https://app.vagrantup.com/).

       export VAGRANT_KURYR_VM_BOX=centos/7

   Could be an example of a rpm-based option.

 * **VAGRANT\_KURYR\_VM\_MEMORY**: To modify the RAM of the VM. Defaulted to: 6144.
   If you mean to create multiple Kubernetes services on the setup and the Octavia
   driver used is Amphora, you should increase this setting.
 * **VAGRANT\_KURYR\_VM\_CPU**: To modify the cpus of the VM. Defaulted to: 2.
 * **VAGRANT\_KURYR\_RUN\_DEVSTACK**: Whether `vagrant up` should run devstack to
   have an environment ready to use. Set it to 'false' if you want to edit
   `local.conf` before run ./stack.sh manually in the VM. Defaulted to: true.
   See below for additional options for editing local.conf.

For a lighter devstack installation, you can use the "local.conf"[1] that uses ovn
and ovn-octavia, no VM will be created for each load-balancer as is done by the
default Octavia provider (Amphora).

References:
[1] https://github.com/openstack/kuryr-kubernetes/blob/master/devstack/local.conf.ovn.sample

Additional devstack configuration
---------------------------------

To add additional configuration to local.conf before the VM is provisioned, you can
create a file called "user_local.conf" in the contrib/vagrant directory of
networking-kuryr. This file will be appended to the "local.conf" created during the
Vagrant provisioning.

For example, to use OVN as the Neutron plugin with Kuryr, you can create a
"user_local.conf" with the following configuration:

    enable_plugin networking-ovn https://opendev.org/openstack/networking-ovn
    enable_service ovn-northd
    enable_service ovn-controller
    disable_service q-agt
    disable_service q-l3
    disable_service q-dhcp
