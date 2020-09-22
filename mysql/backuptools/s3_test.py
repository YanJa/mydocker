#coding=utf-8
from boto.s3.connection import S3Connection
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
c = S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

b = c.get_bucket('fzx')
k = Key(b)
k.key = 'foobar'
k.set_contents_from_string('test')
print k.get_contents_as_string()

#EOP
