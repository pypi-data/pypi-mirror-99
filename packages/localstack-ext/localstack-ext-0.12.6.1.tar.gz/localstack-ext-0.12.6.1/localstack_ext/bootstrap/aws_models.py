from localstack.utils.aws import aws_models
TDxRE=super
TDxRf=None
TDxRM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TDxRE(LambdaLayer,self).__init__(arn)
  self.cwd=TDxRf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TDxRM.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TDxRM,env=TDxRf):
  TDxRE(RDSDatabase,self).__init__(TDxRM,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TDxRM,env=TDxRf):
  TDxRE(RDSCluster,self).__init__(TDxRM,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TDxRM,env=TDxRf):
  TDxRE(AppSyncAPI,self).__init__(TDxRM,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TDxRM,env=TDxRf):
  TDxRE(AmplifyApp,self).__init__(TDxRM,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TDxRM,env=TDxRf):
  TDxRE(ElastiCacheCluster,self).__init__(TDxRM,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TDxRM,env=TDxRf):
  TDxRE(TransferServer,self).__init__(TDxRM,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TDxRM,env=TDxRf):
  TDxRE(CloudFrontDistribution,self).__init__(TDxRM,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TDxRM,env=TDxRf):
  TDxRE(CodeCommitRepository,self).__init__(TDxRM,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
