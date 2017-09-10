#!/bin/bash

#ssh hui-vm2 'cd /home/hui/hadoop-2.6.0/logs; find -type f -exec rm -f {} \;'
#ssh hui-vm2 'cd /home/hui/hadoop_runtime; find -type -f -exec rm -f {} \;'

#ssh hui-vm3 'cd /home/hui/hadoop-2.6.0/logs; find -type f -exec rm -f {} \;'
#ssh hui-vm3 'cd /home/hui/hadoop_runtime; find -type -f -exec rm -f {} \;'

#rsync -alrv $HOME/.bashrc hui-vm2:$HOME
#rsync -alrv $HOME/.bashrc hui-vm3:$HOME

rsync -alrv --delete --exclude=logs $HOME/hadoop-2.6.0 hui-vm2:$HOME
rsync -alrv --delete --exclude=logs $HOME/hadoop-2.6.0 hui-vm3:$HOME
