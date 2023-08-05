from localstack.utils.aws import aws_models
xirel=super
xirej=None
xireA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  xirel(LambdaLayer,self).__init__(arn)
  self.cwd=xirej
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.xireA.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,xireA,env=xirej):
  xirel(RDSDatabase,self).__init__(xireA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,xireA,env=xirej):
  xirel(RDSCluster,self).__init__(xireA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,xireA,env=xirej):
  xirel(AppSyncAPI,self).__init__(xireA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,xireA,env=xirej):
  xirel(AmplifyApp,self).__init__(xireA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,xireA,env=xirej):
  xirel(ElastiCacheCluster,self).__init__(xireA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,xireA,env=xirej):
  xirel(TransferServer,self).__init__(xireA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,xireA,env=xirej):
  xirel(CloudFrontDistribution,self).__init__(xireA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,xireA,env=xirej):
  xirel(CodeCommitRepository,self).__init__(xireA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
