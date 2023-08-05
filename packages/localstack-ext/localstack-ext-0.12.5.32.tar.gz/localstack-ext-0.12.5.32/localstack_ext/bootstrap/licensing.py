import os
EaVTP=Exception
EaVTW=False
EaVTA=str
EaVTd=int
EaVTL=range
EaVTh=len
EaVTk=object
EaVTb=True
import re
import sys
import glob
import json
import base64
import logging
import pyaes
from localstack import config as localstack_config
from localstack.utils.common import(safe_requests as requests,load_file,save_file,to_str,to_bytes,md5,parallelize,now_utc,str_insert,str_remove)
from localstack_ext import config
from localstack_ext.config import PROTECTED_FOLDERS,ROOT_FOLDER,load_config_file
from localstack_ext.constants import VERSION
ENV_PREPARED={}
MAX_KEY_CACHE_DURATION_SECS=60*60*24
LOG=logging.getLogger(__name__)
def read_api_key():
 key=os.environ.get('LOCALSTACK_API_KEY')
 if key:
  return key
 raise EaVTP('Unable to retrieve API key. Please configure $LOCALSTACK_API_KEY in your environment')
def fetch_key():
 api_key=read_api_key()
 if api_key=='test':
  return 'test'
 data={'api_key':api_key,'version':VERSION}
 try:
  logging.getLogger('py.warnings').setLevel(logging.ERROR)
  result=requests.post('%s/activate'%config.API_URL,json.dumps(data),verify=EaVTW)
  key_base64=json.loads(result.content)['key']
  cache_key_locally(api_key,key_base64)
 except EaVTP:
  key_base64=load_cached_key(api_key)
 finally:
  logging.getLogger('py.warnings').setLevel(logging.WARNING)
 decoded_key=to_str(base64.b64decode(key_base64))
 return decoded_key
def cache_key_locally(api_key,key_b64):
 configs=load_config_file()
 timestamp=EaVTA(EaVTd(now_utc()))
 key_raw=to_str(base64.b64decode(key_b64))
 for i in EaVTL(EaVTh(timestamp)):
  key_raw=str_insert(key_raw,i*2,timestamp[i])
 key_b64=to_str(base64.b64encode(to_bytes(key_raw)))
 configs['cached_key']={'timestamp':EaVTd(timestamp),'key_hash':md5(api_key),'key':key_b64}
 save_file(localstack_config.CONFIG_FILE_PATH,json.dumps(configs))
 return configs
def load_cached_key(api_key):
 configs=load_config_file()
 cached_key=configs['cached_key']
 if cached_key.get('key_hash')!=md5(api_key):
  raise EaVTP('Cached key was created for a different API key')
 now=now_utc()
 if(now-cached_key['timestamp'])>MAX_KEY_CACHE_DURATION_SECS:
  raise EaVTP('Cached key expired')
 timestamp=EaVTA(cached_key['timestamp'])
 key_raw=to_str(base64.b64decode(cached_key['key']))
 for i in EaVTL(EaVTh(timestamp)):
  assert key_raw[i]==timestamp[i]
  key_raw=str_remove(key_raw,i)
 key_b64=to_str(base64.b64encode(to_bytes(key_raw)))
 return key_b64
def generate_aes_cipher(key):
 key=to_bytes(key)
 return pyaes.AESModeOfOperationCBC(key,iv='\0'*16)
def decrypt_file(source,target,key):
 cipher=generate_aes_cipher(key)
 raw=load_file(source,mode='rb')
 decrypter=pyaes.Decrypter(cipher)
 decrypted=decrypter.feed(raw)
 decrypted+=decrypter.feed()
 decrypted=decrypted.partition(b'\0')[0]
 decrypted=to_str(decrypted)
 save_file(target,content=decrypted)
def decrypt_files(key):
 files=[]
 for folder in PROTECTED_FOLDERS:
  for subpath in('*.py.enc','**/*.py.enc'):
   for f in glob.glob('%s/localstack_ext/%s/%s'%(ROOT_FOLDER,folder,subpath)):
    files.append(f)
 def _decrypt(f):
  target=f[:-4]
  if not os.path.exists(target):
   decrypt_file(f,target,key)
 parallelize(_decrypt,files)
def cleanup_environment():
 excepted_files=r'.*/services/((edge)|(dns_server)|(__init__))\.py'
 for folder in PROTECTED_FOLDERS:
  for subpath in('*.py.enc','**/*.py.enc'):
   for f in glob.glob('%s/localstack_ext/%s/%s'%(ROOT_FOLDER,folder,subpath)):
    target=f[:-4]
    if not re.match(excepted_files,target):
     for delete_file in(target,'%sc'%target):
      if os.path.exists(delete_file):
       os.remove(delete_file)
def prepare_environment():
 class OnClose(EaVTk):
  def __exit__(self,*args,**kwargs):
   if not ENV_PREPARED.get('finalized'):
    cleanup_environment()
   ENV_PREPARED['finalized']=EaVTb
  def __enter__(self,*args,**kwargs):
   pass
 if not ENV_PREPARED.get('finalized'):
  try:
   key=fetch_key()
   if key!='test':
    decrypt_files(key)
    LOG.info('Successfully activated API key')
  except EaVTP:
   if config.REQUIRE_PRO:
    LOG.error('Unable to activate API key, but $REQUIRE_PRO is configured - quitting.')
    sys.exit(1)
   pass
 return OnClose()
def get_auth_headers():
 configs=load_config_file()
 login_info=configs.get('login')
 if not login_info:
  raise EaVTP('Please log in first')
 auth_token=login_info['token']
 if not auth_token.startswith('%s '%login_info['provider']):
  auth_token='%s %s'%(login_info['provider'],auth_token)
 headers={'authorization':auth_token}
 return headers
# Created by pyminifier (https://github.com/liftoff/pyminifier)
