wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz

sudo apt-get install tcl
sudo apt-get install gcc
sudo apt-get updatae
cd redis-stable
make
cd src
sudo apt install redis-tools
sudo apt-get install redis-server
redis-server
