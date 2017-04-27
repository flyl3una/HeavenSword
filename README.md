# HeavenSword

目前测试漏洞有drupal、wordpress-mailpress、zabbix

> drupal

drupal使用7.31版本，此版本有直接getshell漏洞

> wordpress-mailpress

使用vulapps制作好的包含worepress-mailpress漏洞的docker

```bash
$ docker pull medicean/vulapps:w_wordpress_2
$ docker run -d -p 8000:80 medicean/vulapps:w_wordpress_2
#;-p 8000:80 前面的 8000 代表物理机的端口，可随意指定。
```

> zabbix

使用vulapps制作好的包含Zabbix 2.2.x/3.0.x latest.php SQL 注入漏洞的docker

```shell
$ docker pull medicean/vulapps:z_zabbix_2
$ docker run -d -p 8000:80 medicean/vulapps:z_zabbix_2
#-p 8000:80 前面的 8000 代表物理机的端口，可随意指定。
```

