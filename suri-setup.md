# suricata device installation 

Use non MU-net to sync NTP first.  
Switch to MU-net (with proxy) to save own data.
NOTE: do not fuck up the wifi again, big hassle to all installation steps. Trying to reenable the wifi again last time result in "bluescreen". Its easy to think, if the shit broke when we found problem halfway, *proceed to find worst method to install/fix shit, cuz no wifi*. why so much installation issue? prolly lack of wifi.

## dependencies & utilities

```bash
sudo apt update
sudo apt upgrade

sudo apt install libpcre2-dev libpcre3-dev libyaml-dev libjansson-dev libpcap-dev libcap-ng-dev libmagic-devv liblz4-dev libnss3-dev libnspr4  libssl-dev python3-yaml
```
## install rust

```bash
sudo curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
export PATH=$PATH:~/.cargo/bin/
# check version with
rustc -V
```
## install suricata
on configure step, if successful, will see build info. if not it will ask for additional installation.
the 'suricata-update' functionality is not used, thus not installed. despiteh the name, it is mainly for updating rules, not suricata itself. 
```bash
wget https://www.openinfosecfoundation.org/downloads/suricata-7.0.2.tar.gz
tar -xzf suricata-7.0.2.tar.gz
## GO INTO FOLDER
./configure --enable-nfqueue --prefix=/usr --sysconfdir=/etc --localstatedir=/var
## configure command to see if anything missing. if so, install.
# -j 4 increase the thread
make -j 4 
make install-full
```
## install OvS
 - https://docs.openvswitch.org/en/latest/intro/install/general/
 - for start up procedure, check the above link to avoid fckups
 - with these steps scripts will be in /usr/share/openvswitch
```bash
##> need make, >gcc4.3, libssl, libcap-ng, >python3.6, unbound(dns resolver optional)
wget https://www.openvswitch.org/releases/openvswitch-3.2.2.tar.gz
tar -xzf openvswitch-3.2.2.tar.gz
## GO INTO FOLDER
./configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc
## again, check for any prominent warning
# -j 4 increase the thread
make -j 4 
make install

ovs-ctl start --system-id=xx
ovs-ctl start

export PATH=$PATH:/usr/share/openvswitch/scripts
# or better yet, add this specific line to the .bashrc file
export PATH="/usr/share/openvswitch/scripts:$PATH"
```