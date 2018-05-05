# mlpm-jobs

## 开发环境搭建

### postgresql 安装与配置

```bash
sudo apt-get install postgresql-10
sudo -u postgres createuser -P micl
sudo -u postgres createdb mlpm_jobs -O micl
sudo -u postgres createdb mlpm_jobs_result -O micl
```

数据库`mlpm_jobs`为本系统使用数据库，`mlpm_jobs_result`为**celery_result_backend**使用数据库。
可根据实际需求修改数据库名和用户名。

### RabbitMQ 安装与配置

```bash
sudo rabbitmqctl add_user micl micl
sudo rabbitmqctl add_vhost mlpm_jobs_server
sudo rabbitmqctl set_user_tags micl mlpm_jobs
sudo rabbitmqctl set_permissions -p mlpm_jobs_server micl ".*" ".*" ".*"
```

可根据实际需求修改用户名等配置信息。


### apidoc 安装与配置

系统的api文档使用 [apidoc](http://apidocjs.com) 生成，因此还需要有 nodejs 环境，并安装 **apidoc**。
这里不去详述 nodejs 和 apidoc 的安装方式。

```bash
npm i -g apidoc
```

### 启动本系统

1. 克隆。
    ```bash
    git clone https://github.com/Yuvv/mlpm-jobs.git
    ```

2. 安装依赖。
    ```bash
    # 创建虚拟环境
    virtualenv venv
    # 启用虚拟环境之后安装依赖
    pip install -r requirements.txt
    ```
    
3. 修改配置文件及初始化数据库。
    ```bash
    # 将 `settings/local_settings.example.py` 复制一份，并修改其中的数据库及celery相关配置
    cp settings/local_settings.example.py settings/local_settings.py
    # 使用 alembic 进行数据库初始化
    alembic revision --autogenerate -m "init database"
    # 得到对应版本号之后进行审计
    alembic upgrade xxxx
    ```

4. 启动 celery。非windows系统可以不加`--pool`参数
    ```bash
    celery -A tasks worker -l info --pool=solo
    ```

5. 启动系统。（*注意这里不要通过`app.py`启动，这将导致 celery 无法使用*，使用 pycharm 的话新建配置从 `wsgi.py` 启动即可）
    ```bash
    python wsgi.py
    ```

## 开发 Q & A

### 系统结构

系统使用 [flask](flask.pocoo.org) 编写。
结构上其实没什么可说的。

`utils`模块主要包括了一些公用的模块，像什么获取参数啊，错误处理啊，中间件啊什么的。

`tasks`模块主要包括了核心的异步任务这一块的内容。`tasks.general`预留的作为所有对外提供的任务。

其它个人如模块名字。

### 数据库管理

数据库推荐使用 [postgresql](https://www.postgresql.org/) ，坑比较少，最好使用 10 版本。
当然使用其它的数据库也没关系，都支持。

ORM 工具使用的 [sqlalchemy](https://www.sqlalchemy.org/) ，比较灵活，学习上有一定难度。

数据库迁移管理工具使用 [alembic](http://alembic.zzzcomputing.com)，sqlalchemy 作者编写，有保障。
在有些情况下自动迁移会失败，检测不到该懂，需要手动修改 DDL，不过影响倒不大。

迁移基本上就下面这两个命令，先自动生成迁移脚本，得到版本号之后进行迁移：
```bash
alembic revision --autogenerate -m "<message here>"
alembic upgrade "<version number here>"
```
生成的迁移文件可以自己查阅修改（基本不需要）。版本号可以简写前几个字母。

### API 文档管理

api 文档没有使用python原生doc方式而是使用了 [apidoc](http://apidocjs.com)，方便好用。

具体的文档编写格式可以查阅一下官网，生成文档使用下面的命令即可：
```bash
apidoc -i apis -o docs/apidoc
```

### 任务函数管理

如果需要新添加异步任务函数的话，直接在`tasks.general`模块下面编写吧。
编写的函数装饰器中一定要设置`base=MLPMAsyncTask`，否则无法识别。

编写完成测试无误的话再添加到数据库中吧。
目前没有添加相应的管理界面，直接修改数据库吧，字段也很短，把各个字段填写清楚就好了，尤其是函数文档那个字段。


## 部署

在 `conf` 目录下面有一些示例的配置文件，包括 celery 、uwsgi 、nginx ，可以参考。
配置中都是假设此工程位于`/srv/www/sites/mlpm_jobs/`目录下的，如有需要可以对应更改。

1. celery daemon。
    ```bash
    cp conf/celery/default/{celeryd,celerybeat} /etc/default/
    cp conf/celery/initd/{celeryd,celerybeat} /etc/init.d/
    systemctl enable celeryd
    systemctl enable celerybeat
    ```

2. uwsgi。（当然配置文件放在哪不重要，这里放在根目录只是为了方便，而且里面还有一个`touch-reload`参数配置了这个文件的路径）
    ```bash
    cp conf/uwsgi.example.ini uwsgi_config.ini
    ```
3. nginx。(这个的配置比较灵活，conf 目录里面的示例也只是简单列了一下，更具具体情况来吧)