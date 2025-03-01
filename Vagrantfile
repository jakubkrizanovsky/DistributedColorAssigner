#
# Create n nodes
#

VAGRANTFILE_API_VERSION = "2"
# set docker as the default provider
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker'
# disable parallellism so that the containers come up in order
ENV['VAGRANT_NO_PARALLEL'] = "1"
ENV['FORWARD_DOCKER_PORTS'] = "1"
# minor hack enabling to run the image and configuration trigger just once
ENV['VAGRANT_EXPERIMENTAL']="typed_triggers"

unless Vagrant.has_plugin?("vagrant-docker-compose")
  system("vagrant plugin install vagrant-docker-compose")
  puts "Dependencies installed, please try the command again."
  exit
end

# Names of Docker images built:
NODE_IMAGE  = "dsa/distributed_color_assigner:0.1"

# Node definitions
NODE = { :nameprefix => "node-",  # nodes get names: node-1, node-2, etc.
              :subnet => "192.168.1.",
              :ip_offset => 100,  # nodes get IP addresses: 192.168.1.101, .102, .103, etc
              :image => NODE_IMAGE}
# Number of nodes to start:
NODE_COUNT = 1

# Common configuration
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Before the 'vagrant up' command is started, build docker images:
  config.trigger.before :up, type: :command do |trigger|
    trigger.name = "Build docker images and configuration files"
    trigger.ruby do |env, machine|
      # --- start of Ruby script ---
      # Build image for nodes:
      puts "Building node image:"
      `docker build node -t "#{NODE_IMAGE}"`
      # --- end of Ruby script ---
    end
  end

  config.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: ".*/"
  config.ssh.insert_key = false

  # Definition of N nodes
  (1..NODE_COUNT).each do |i|
    node_ip_addr = "#{NODE[:subnet]}#{NODE[:ip_offset] + i}"
    node_name = "#{NODE[:nameprefix]}#{i}"
    # Definition of NODE
    config.vm.define node_name do |s|
      s.vm.network "private_network", ip: node_ip_addr
      s.vm.network "forwarded_port", guest: 5000, host: 8080 + i, host_ip: "0.0.0.0"
      s.vm.hostname = node_name
      s.vm.provider "docker" do |d|
        d.build_dir = "node"
        d.build_args = ["-t", "#{NODE[:image]}"]
        d.name = node_name
        d.has_ssh = true
      end
      s.vm.post_up_message = "Node #{node_name} up and running. You can access the node with 'vagrant ssh #{node_name}'"
    end
  end
end

# EOF
