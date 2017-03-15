# django-qcloud-cos
Django storage for qcloud.com 对象存储服务
# 介绍
django-qcloud-cos 是一个服务于腾讯云存储的Django自定义存储系统。
# 安装
1. 拷贝qcloudcos目录于自己的项目内，放于与manage.py同一级。
2. 配置setting.py:
* 将上传文件存放到云
>DEFAULT_FILE_STORAGE = 'qcloudcos.qcloudstorage.QcloudStorage'
* 将静态文件存放到云
>STATICFILES_STORAGE = 'qcloudcos.qcloudstorage.QcloudStorage'
* 替换Appid， SecretId， SecretKey, region, bucket

    QCLOUD_STORAGE_OPTION = {
        'Appid': 'appid: 开发者访问 COS 服务时拥有的用户维度唯一资源标识，用以标示资源。',
        'SecretID': 'SecretID: SecretID 是开发者拥有的项目身份识别 ID，用以身份认证',
        'SecretKey': 'SecretKey: SecretKey 是开发者拥有的项目身份密钥。',
        'region': '域名中的地域信息，枚举值：cn-east（华东），cn-north（华北），cn-south（华南），sg（新加坡）',
        'bucket': '存储桶是 COS 中用于存储数据的容器，是用户存储在 Appid 下的第一级目录，每个对象都存储在一个存储桶中。',
    }
3. 同步静态文件到云
> python manage.py collectstatic