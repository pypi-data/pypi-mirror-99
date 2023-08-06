from localstack.utils.aws import aws_models
wRPkA=super
wRPkC=None
wRPkx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  wRPkA(LambdaLayer,self).__init__(arn)
  self.cwd=wRPkC
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.wRPkx.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,wRPkx,env=wRPkC):
  wRPkA(RDSDatabase,self).__init__(wRPkx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,wRPkx,env=wRPkC):
  wRPkA(RDSCluster,self).__init__(wRPkx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,wRPkx,env=wRPkC):
  wRPkA(AppSyncAPI,self).__init__(wRPkx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,wRPkx,env=wRPkC):
  wRPkA(AmplifyApp,self).__init__(wRPkx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,wRPkx,env=wRPkC):
  wRPkA(ElastiCacheCluster,self).__init__(wRPkx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,wRPkx,env=wRPkC):
  wRPkA(TransferServer,self).__init__(wRPkx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,wRPkx,env=wRPkC):
  wRPkA(CloudFrontDistribution,self).__init__(wRPkx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,wRPkx,env=wRPkC):
  wRPkA(CodeCommitRepository,self).__init__(wRPkx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
