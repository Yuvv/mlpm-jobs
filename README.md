# mlpm-jobs

## postgresql
```bash
sudo apt-get install postgresql-10
sudo -u postgres createuser micl
sudo -u postgres createdb mlpm_jobs -O micl
```

## RabbitMQ

rabbitmq:
  user: micl
  pwd:  micl
  vhost: mlpm_jobs_server
  tags: mlpm_jobs
  permission: ***

```bash
sudo rabbitmqctl add_user micl micl
sudo rabbitmqctl add_vhost mlpm_jobs_server
sudo rabbitmqctl set_user_tags micl mlpm_jobs
sudo rabbitmqctl set_permissions -p mlpm_jobs_server micl ".*" ".*" ".*"
```

## Celery

> http://docs.celeryproject.org/en/3.1/tutorials/daemonizing.html