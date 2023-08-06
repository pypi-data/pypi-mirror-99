from localstack.utils.aws import aws_models
yurcn=super
yurcm=None
yurcP=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yurcn(LambdaLayer,self).__init__(arn)
  self.cwd=yurcm
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.yurcP.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,yurcP,env=yurcm):
  yurcn(RDSDatabase,self).__init__(yurcP,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,yurcP,env=yurcm):
  yurcn(RDSCluster,self).__init__(yurcP,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,yurcP,env=yurcm):
  yurcn(AppSyncAPI,self).__init__(yurcP,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,yurcP,env=yurcm):
  yurcn(AmplifyApp,self).__init__(yurcP,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,yurcP,env=yurcm):
  yurcn(ElastiCacheCluster,self).__init__(yurcP,env=env)
class TransferServer(BaseComponent):
 def __init__(self,yurcP,env=yurcm):
  yurcn(TransferServer,self).__init__(yurcP,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,yurcP,env=yurcm):
  yurcn(CloudFrontDistribution,self).__init__(yurcP,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,yurcP,env=yurcm):
  yurcn(CodeCommitRepository,self).__init__(yurcP,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
