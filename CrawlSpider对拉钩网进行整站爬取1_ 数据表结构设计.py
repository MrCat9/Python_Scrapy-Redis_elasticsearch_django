# 在数据库article_spider的tables下，新建表 lagou_job
Field Name              Datatype        Len         Default     PK?     Not Null
url                     varchar         300                                √
url_object_id           varchar         50                       √         √
title                   varchar         100                                √
salary                  varchar         20
job_city                varchar         10
work_years              varchar         100
degree_need             varchar         30
job_type                varchar         20
publish_time            varchar         20                                 √
tags                    varchar         100
job_advantage           varchar         1000
job_desc                longtext                                           √
job_addr                varchar         50
company_url             varchar         300
company_name            varchar         100
crawl_time              datetime                                           √
crawl_update_time       datetime



