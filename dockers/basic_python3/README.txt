1. build myacct docker

   docker build -t myacct .

2. Run interactive shell and map jupyter port:

   docker run -p 8888:8888 --name docker_myacct -it myacct:v1 bash

3. test SQL for SBG vertica:

   select * from pcg_dm.us_state_lookup
