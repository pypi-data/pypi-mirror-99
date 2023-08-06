

from operator_this import AwsLambdaDeploymentOperator

def create(self, deployment_info, wait):
		if isinstance(deployment_info, dict):
			deployment_pb = deployment_dict_to_pb(deployment_info)
		elif isinstance(deployment_info, str):
			deployment_pb = deployment_yaml_string_to_pb(deployment_info)
		elif isinstance(deployment_info, Deployment):
			deployment_pb = deployment_info
		else:
			raise YataiDeploymentException(
				'Unexpected argument type, expect deployment info to be str in yaml '
				'format or a dict or a deployment protobuf obj, instead got: {}'.format(
					str(type(deployment_info))
				)
			)

		validation_errors = validate_deployment_pb(deployment_pb)
		if validation_errors:
			raise YataiDeploymentException(
				f'Failed to validate deployment {deployment_pb.name}: '
				f'{validation_errors}'
			)
		# Make sure there is no active deployment with the same deployment name
		get_deployment_pb = self.yatai_service.GetDeployment(
			GetDeploymentRequest(
				deployment_name=deployment_pb.name, namespace=deployment_pb.namespace
			)
		)
		if get_deployment_pb.status.status_code != status_pb2.Status.NOT_FOUND:
			raise BentoMLException(
				f'Deployment "{deployment_pb.name}" already existed, use Update or '
				f'Apply for updating existing deployment, delete the deployment, '
				f'or use a different deployment name'
			)
		apply_result = self.yatai_service.ApplyDeployment(
			ApplyDeploymentRequest(deployment=deployment_pb)
		)
		if apply_result.status.status_code != status_pb2.Status.OK:
			error_code, error_message = status_pb_to_error_code_and_message(
				apply_result.status
			)
			raise YataiDeploymentException(f'{error_code}:{error_message}')
		if wait:
			self._wait_deployment_action_complete(
				deployment_pb.name, deployment_pb.namespace
			)
		return self.get(namespace=deployment_pb.namespace, name=deployment_pb.name)

def get(self, namespace, name):
		return self.yatai_service.GetDeployment(
			GetDeploymentRequest(deployment_name=name, namespace=namespace)
		)

from operator_this import create_aws_lambda_cloudformation_template_file
from utils import call_sam_command,call_bash
import shutil
import os
from pathlib import Path
import json
# print(os.getcwd())

def lambda_deploy(base_dir,namespace,project_name,stackName, projectConfig, model_path):

		clouderizerProjectName = project_name
		project_name=project_name.replace("-","")
		stackName=stackName.replace("-","")
		# print("Model type:", projectConfig["subtype"])

		project_dir = base_dir + "/lambda-dir"
		Path(project_dir).mkdir(parents=True, exist_ok=True)

		if "pmml" in projectConfig["subtype"] or "h2o" in projectConfig["subtype"]:
			shutil.copy(base_dir+'/dockerfiles/AutomlDockerfile',project_dir+"/Dockerfile")
		
		function_dir = project_dir + "/function"
		Path(function_dir).mkdir(parents=True, exist_ok=True)

		writeObj = open(function_dir+"/projectConfig.json","w")
		writeObj.write(json.dumps(projectConfig))
		writeObj.close()

		shutil.copy(model_path,function_dir+"/model.pmml")

		apiNames = [stackName+"Api"]
		stack_name = stackName

		ecr_name = "clouderizer-lambda"

		print("Checking for default aws region configured in aws cli")

		awsRegionCode, awsRegionStdout, awsRegionStderr = call_bash(
			["aws","configure","get","region"],
			project_dir
		)

		awsRegionStdout = awsRegionStdout.replace("\n","")
		print("Configured region: ", awsRegionStdout)

		aws_region = awsRegionStdout
		if not awsRegionStdout:
			aws_region = "us-east-2"
			print("Choosing ",aws_region)

		return_code, stdout, stderr = call_bash(
			["aws", "ecr", "create-repository", "--repository-name" ,ecr_name,
			"--image-tag-mutability", "IMMUTABLE", "--image-scanning-configuration" ,"scanOnPush=true"],
			project_dir
		)

		# if not "RepositoryAlreadyExistsException" in stderr:
		return_code, stdout, stderr = call_bash(
			["aws", "sts", "get-caller-identity"],
			project_dir
		)

		# print(eval(stdout)["Account"])

		if not "Account" in eval(stdout):
			print("Could not fetch aws account")
			exit(0)

		registry_url = "{}.dkr.ecr.{}.amazonaws.com/{}".format(eval(stdout)["Account"],aws_region,ecr_name)

		create_aws_lambda_cloudformation_template_file(
			clouderizerProjectName,
			project_dir,
			namespace,
			project_name,
			apiNames,
			project_name,
			1024,
			88
		)

		shutil.copy(project_dir+'/template.yaml',os.getcwd()+'/template.yaml')

		print("Building docker image....")

		return_code, stdout, stderr = call_sam_command(
			["build", "--use-container", "--region", aws_region],
			project_dir=os.getcwd(),
			region=aws_region,
		)
		if return_code != 0:
			error_message = stderr

			if error_message:
				print(error_message)
				exit(0)

			# print(stderr)
			# print(stdout)
			# raise BentoMLException(
			#     "Failed to build lambda function. {}".format(error_message)
			# )
		# logger.debug("Removing unnecessary files to free up space")
		template_file = os.path.join(os.getcwd(), ".aws-sam", "build", "template.yaml")

		print("Deploying project to AWS lambda")

		return_code, stdout, stderr = call_sam_command(
			[
				"deploy",
				"--stack-name",
				stack_name,
				"--capabilities",
				"CAPABILITY_IAM",
				"--template-file",
				template_file,
				"--region",
				aws_region,
				"--image-repositories",
				"{}={}".format(apiNames[0],registry_url)
			],
			project_dir=project_dir,
			region=aws_region,
    	)
		if return_code != 0:
			error_message = stderr
			if error_message:
				print(error_message)
				exit(0)

		print(stdout)
		print("Project deployed!")
		print("Fetching project access urls")

		describeStackCode, describeStackStdout, describeStackStderr = call_bash(
			[
				"aws",
				"cloudformation",
				"describe-stacks"
			],
			project_dir
		)

		accessUrl=None
		if describeStackCode == 0:
			describeStackStdout = json.loads(describeStackStdout)
			for stack in describeStackStdout["Stacks"]:
				if stack["StackName"] == stackName:
					for output in stack["Outputs"]:
						if output["OutputKey"] == "EndpointUrl":
							accessUrl = output["OutputValue"]
			print("Model access url:", accessUrl)
			return accessUrl
		else:
			print(describeStackStderr)
			exit(0)
