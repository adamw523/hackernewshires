docker stop hackernews
docker rm hackernews
docker run --name hackernews -h hackernews --volumes-from devshare_host -d -p 8888 -t adamw523/ipython su adam -c "/home/adam/notebookenv/bin/ipython notebook --pylab inline --notebook-dir=/devshare/projects/hackernewshires --ip=0.0.0.0"

