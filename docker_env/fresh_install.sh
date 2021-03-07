 
apt update
apt install python3.7
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.7 ./get-pip.py 
sudo apt install python3-pip
python3.7 ./get-pip.py 
sudo apt-get install python3-venv
sudo apt install python3.7-venv
python3.7 -m venv .


sudo apt-get install libpq-dev python3.7-dev
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install     apt-transport-https     ca-certificates     curl     gnupg-agent     software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
apt-cache madison docker-ce
sudo apt-get install docker-ce=5:19.03.6~3-0~ubuntu-bionic docker-ce-cli=5:19.03.6~3-0~ubuntu-bionic containerd.io

# 192.144.204.104 为正式上线前的预生产环境, 缓存启用redis, 数据库为postgres 
echo 'export AZENV=preprod' >> ~/.bashrc


# fix Got permission denied while trying to connect to the Docker daemon socket
# 
sudo gpasswd -a ${USER} docker
sudo -i
su ubuntu
