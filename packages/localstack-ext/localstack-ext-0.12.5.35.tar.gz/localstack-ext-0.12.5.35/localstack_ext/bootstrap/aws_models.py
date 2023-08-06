from localstack.utils.aws import aws_models
IgUAm=super
IgUAP=None
IgUAT=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IgUAm(LambdaLayer,self).__init__(arn)
  self.cwd=IgUAP
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IgUAT.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IgUAT,env=IgUAP):
  IgUAm(RDSDatabase,self).__init__(IgUAT,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IgUAT,env=IgUAP):
  IgUAm(RDSCluster,self).__init__(IgUAT,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IgUAT,env=IgUAP):
  IgUAm(AppSyncAPI,self).__init__(IgUAT,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IgUAT,env=IgUAP):
  IgUAm(AmplifyApp,self).__init__(IgUAT,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IgUAT,env=IgUAP):
  IgUAm(ElastiCacheCluster,self).__init__(IgUAT,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IgUAT,env=IgUAP):
  IgUAm(TransferServer,self).__init__(IgUAT,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IgUAT,env=IgUAP):
  IgUAm(CloudFrontDistribution,self).__init__(IgUAT,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IgUAT,env=IgUAP):
  IgUAm(CodeCommitRepository,self).__init__(IgUAT,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
