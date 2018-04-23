# http://127.0.0.1:5601    dev tools ��



# es���ĵ���������CRUD����

# ������ʼ������
# ָ����Ƭ�͸���������
# shardsһ�����ò����޸ģ��������������޸�
PUT lagou    # lagouΪ����������
{
  "settings": {
    "index": {
      "number_of_shards":5,  #��Ƭ��������Ĭ��Ϊ5
      "number_of_replicas":1 #������������Ĭ��Ϊ1
    }
  }
}

# ���н������
{
  "acknowledged": true,
  "shards_acknowledged": true
}

# ��head��ˢ�£����Կ���lagou

# ��head�У������£�Ҳ�����½�����

GET lagou/_settings          # ��ȡlagou��settings
GET .kibana,lagou/_settings  # ��ȡ.kibana��lagou��settings
GET  _all/_settings          # ��ȡ����������settings
GET _settings                # ��ȡ����������settings

# �޸�settings
PUT lagou/_settings
{
  "number_of_replicas": 2
}

# ��ȡ���е�������Ϣ
GET _all

# ��ȡlagou��������Ϣ
GET lagou

# ������Ϣ��������
PUT lagou/man/1  #����/type/id
{

  "name": "С��",

  "country": "China",

  "age": 3,

  "date": "1987-03-07 12:12:12"

}  #������head  �������  lagou�п������������

POST lagou/man/    # ��ָ��id�Զ�����uuid
{

  "name": "С��",

  "country": "China",

  "age": 2,

  "date": "1999-09-09 12:12:12"

}

# ��ȡ�ĵ�
GET lagou/man/1
GET lagou/man/1?_source=name
GET lagou/man/1?_source=name,age
GET lagou/man/1?_source

# �޸���Ϣ
PUT lagou/man/1  #����ʽ�ģ�������û��country��Ϣ
{

  "name": "С��",

  "age": 1,

  "date": "1987-03-07 12:12:12"

}

# �޸Ĳ����ֶ�
POST lagou/man/1/_update
{
  "doc":{  #�����Ҫ�޸ĵ�����
    "age":2,
    "country":"China"
  }
}

# ɾ��
DELETE lagou/man/1
DELETE lagou
