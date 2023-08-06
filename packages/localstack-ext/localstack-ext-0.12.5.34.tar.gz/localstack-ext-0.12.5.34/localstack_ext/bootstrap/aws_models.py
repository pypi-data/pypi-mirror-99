from localstack.utils.aws import aws_models
WUOES=super
WUOER=None
WUOEI=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  WUOES(LambdaLayer,self).__init__(arn)
  self.cwd=WUOER
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.WUOEI.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,WUOEI,env=WUOER):
  WUOES(RDSDatabase,self).__init__(WUOEI,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,WUOEI,env=WUOER):
  WUOES(RDSCluster,self).__init__(WUOEI,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,WUOEI,env=WUOER):
  WUOES(AppSyncAPI,self).__init__(WUOEI,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,WUOEI,env=WUOER):
  WUOES(AmplifyApp,self).__init__(WUOEI,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,WUOEI,env=WUOER):
  WUOES(ElastiCacheCluster,self).__init__(WUOEI,env=env)
class TransferServer(BaseComponent):
 def __init__(self,WUOEI,env=WUOER):
  WUOES(TransferServer,self).__init__(WUOEI,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,WUOEI,env=WUOER):
  WUOES(CloudFrontDistribution,self).__init__(WUOEI,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,WUOEI,env=WUOER):
  WUOES(CodeCommitRepository,self).__init__(WUOEI,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
