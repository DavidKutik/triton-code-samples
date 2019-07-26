Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu-xenial-server"
  config.vm.hostname = "triton"
  config.vm.box_url = "https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-vagrant.box"
  config.vm.provider "virtualbox" do |v|
    v.name = "triton"
    v.cpus = 16
    v.memory = 8192
    v.customize ["storagectl", :id, "--name", "SCSI", "--hostiocache", "on"]
    v.customize ["storageattach", :id, "--storagectl", "SCSI", "--port", "0", "--nonrotational", "on"]
    v.customize ["storageattach", :id, "--storagectl", "SCSI", "--port", "0", "--discard", "on"]
    v.customize ["storageattach", :id, "--storagectl", "SCSI", "--port", "1", "--nonrotational", "on"]
    v.customize ["storageattach", :id, "--storagectl", "SCSI", "--port", "1", "--discard", "on"]
  end
  config.vm.network "public_network"
  config.vm.provision :shell, :inline => "apt-get update; apt-get -y install vim tmux screen gdb htop glances; apt-get -y --autoremove upgrade; apt-get clean"
  config.vm.provision :shell, :inline => "apt-get install -y gcc-4.9 g++-4.9 git cmake build-essential clang ca-certificates curl unzip libboost-dev python-dev python-pip && apt-get clean"
  config.vm.provision :shell, :inline => "ln -sf /usr/bin/gcc-4.9 /usr/bin/gcc &&
  ln -sf /usr/bin/g++-4.9 /usr/bin/g++"
  config.vm.provision :shell, :inline => "cd /tmp && curl -o z3.tgz -L https://github.com/Z3Prover/z3/archive/z3-4.5.0.tar.gz && tar zxf z3.tgz && cd z3-z3-4.5.0 && CC=clang CXX=clang++ python scripts/mk_make.py && cd build && make -j$((`nproc`+1)) && make install && cd /tmp && rm -rf /tmp/z3-z3-4.5.0"
  config.vm.provision :shell, :inline => "cd /tmp && curl -o cap.tgz -L https://github.com/aquynh/capstone/archive/3.0.4.tar.gz && tar xvf cap.tgz && cd capstone-3.0.4/ && ./make.sh install && cd /tmp && rm -rf /tmp/capstone-3.0.4"
  config.vm.provision :shell, :inline => "cd /opt && curl -o pin.tgz -L http://software.intel.com/sites/landingpage/pintool/downloads/pin-2.14-71313-gcc.4.4.7-linux.tar.gz && tar zxf pin.tgz"
  config.vm.provision :shell, :inline => "cd /opt/pin-2.14-71313-gcc.4.4.7-linux/source/tools/ && git clone https://github.com/JonathanSalwan/Triton.git && cd Triton && mkdir build && cd build && cmake -G 'Unix Makefiles' -DPINTOOL=on -DKERNEL4=on .. && make -j$((`nproc`+1)) install"
  config.vm.provision :shell, :inline => "cd /tmp &&
  mkdir kernel &&
  cd kernel &&
  wget -q http://launchpadlibrarian.net/220635919/linux-headers-3.19.0-31-generic_3.19.0-31.36~14.04.1_amd64.deb &&
  wget -q http://launchpadlibrarian.net/220668669/linux-headers-3.19.0-31_3.19.0-31.36~14.04.1_all.deb &&
  wget -q http://launchpadlibrarian.net/220635970/linux-image-3.19.0-31-generic_3.19.0-31.36~14.04.1_amd64.deb &&
  apt-get install -y module-init-tools &&
  sudo dpkg -i linux-* &&
  sed -i 's/GRUB_DEFAULT=0/GRUB_DEFAULT=\"Advanced options for Ubuntu>Ubuntu, with Linux 3.19.0-31-generic\"/' /etc/default/grub &&
  update-grub"
  config.vm.provision :shell, :inline => "cd /opt/pin-2.14-71313-gcc.4.4.7-linux/source/tools/ManualExamples &&
  make -j$((`nproc`+1)) all TARGET=intel64"  
end