# Demo 2 - Leveraging Amazon SageMaker for Image Classification

![Architecture](https://github.com/darkreapyre/itsacat/blob/Demo-2/Notebooks/images/Architecture.png)

## Deployment
>**Note:** This demonstration has been tested in the `us-east-1` AWS Region.
1. To deploy the environment, an easy to use deployment script has been created to automatically deploy the environment. Start the process by running `bin/deploy`. You will be prompted for the following information:
```console
    Enter the AWS Region to use > <<AWS REGION>>
    Enter the S3 bucket to create > sagemaker-<<AWS REGION>>-<<AWS ACCOUNT>>
    Enter the name of the Stack to deploy > <<UNIQUE CLOUDFOMRATION STACK NAME>>
    Enter GitHub User > <<GITHUB USERNAME>>
    Enter GitHubToken > <<GITHUB TOKEN>>
    Enter the e-mail address to send training update > <<E-MAIL ADDRESS>>
```
>**Note:** For more information on creating a GitHub [Token](https://github.com/settings/tokens).

2. The `deploy.sh` script creates the an *S3* Bucket; copies the necessary CloudFormation templates to the Bucket and creates the CloudFormation Stack. Once completed, the following message is displayed:
```console
    "Successfully created/updated stack - <<UNIQUE CLOUDFOMRATION STACK NAME>>"
```
>**Note:** During the deployment, and e-mail will be sent to the specified address. __Make sure to confirm the subscription to the SNS Topic!__

## SageMaker Notebook Instance
Once the stack has been deployed, start an [Amazon SageMaker](https://aws.amazon.com/sagemaker/) Notebook Instance by using the following steps:
1. Open the SageMaker [console](https://console.aws.amazon.com/sagemaker).
2. Create notebook instance.
3. Notebook instance settings.
    - Notebook instance name.
    - Notebook instance type -> ml.t2.medium.
    - IAM Role -> Create new role.
    - Specific S3 Bucket -> `sagemaker-<<AWS REGION>>-<<AWS ACCOUNT>>` -> Create Role.
    - Create notebook instance.
4. You should see Status -> Pending.
5. Under **Actions** -> Select **Open**.
6. After the Jupyter Interface has opened, Clone the GitHub Repository.
    - Under the **Files** tab -> Click **New** -> **Terminal**.
    - Under the Shell run the following commands:
    ```shell
        $ cd SageMaker
        $ git clone https://github.com/<<GITHUB USERNAME>>/itsacat
        $ cd itsacat
        $ git checkout Demo-2
        $ exit
    ```
    - Go back to the **Files** tab -> click `itsacat` -> click **Notebooks** -> select `ItsaCat-Gluon_Codebook.ipynb`

## Demo Process Flow
To follow the Machine Learning Pipeline process flow the two steps listed below:

### Step 1. - Jupyter Notebook
The `ItsaCat-Gluon_Codebook.ipynb` has been created to explain the typical process the *Data Scientist* follows within the Machine Learning Pipeline, namely:

1. Input Data Preparation and Upload.
2. Training the Classifier.
3. Model Training Performance Analysis.
4. Prediction Endpoint Performance Analysis.

### Step 2. - Production API
After the model has been optimally trained and validated in [Step 1.](#step-1-jupyter-notebook), it can be integrated into the Production application by leveraging the *DevOps* process. To accomplish this, follow these steps:

1. Add the optimized model training job name to `src/endpoint.py` *(line 13)*, so that it resembles the following:
```python
    training_job = 'sagemaker-mxnet-2018-04-27-15-06-57-730'
```
2. 



<!-- ### Step 4. Prediction API
The deployment pipeline for the production application is triggered at two separate stages within the Demo Process Flow:
- After executing the `Codebook.ipynb` in [Step 1.](#step-1-jupyter-notebooks), the parameters are written to the `predict_input` folder of the S3 bucket. Since this is a Source for CodePipeline to trigger the deployment. At this stage, since the parameters have only been trained for 10 iterations, they are not fully optmized, so the Prediction API will not fully predict a "cat" picture.
- After the model has been optimally trained in [Step 2.](#step-2-training-the-classifier), the parameters once again written to the `predict_input` folder fo the S3 bucket and thius the deployment pipeline is triggered. Since the model has been optmially trained, the Prediction API should fully predict a "cat" picture.

During either of the above stages, an e-mail will be sent to the address configured during deployment similar to the following (stripped for brevity):
```text
Hello,

The following Approval action is waiting for your response:

--Pipeline Details--

...
```
Included is the e-mail is a link to the *CodePipeline* Service Console to approve the deployment from QA to Production. To view and test the Prediction API in the QA stage, execute the following:
1. Open the *CloudFormation* Service Console and select the nested Stack for the Elastic Container Service (ECS). e.g. **`<<Stack Name>>-DeploymentPipeline-...-ecs-cluster`**.
2. Click on the CloudFormation Outputs tab.
3. The *ApplicationURL** Value provides a link to the **Prediction API URL for Production (Blue)**. Clicking on this link will open a browser page to the Prediciton API. Successful connection to the API will display the **"Ping Successfull!"** message.
4. To view the production (Blue) API, find the URL of a "cat" picture (e.g.[Grumpy Cat](http://i0.kym-cdn.com/entries/icons/facebook/000/011/365/GRUMPYCAT.jpg)) and add it to the URL as follows:
    
    `http://<<GitHub Repo Name>>.us-east-1.elb.amazonaws.com/image?image=http://i0.kym-cdn.com/entries/icons/facebook/000/011/365/GRUMPYCAT.jpg`

5. To view the Test/Staging (Green) API, simply change the port to **8080** as follows:

    `http://<<GitHub Repo Name>>.us-east-1.elb.amazonaws.com:8080/image?image=http://i0.kym-cdn.com/entries/icons/facebook/000/011/365/GRUMPYCAT.jpg`

Accessing the (Green) API after [Step 2.](#step-2-training-the-classifier)) should correctly predict a "cat" image and thus the **Manual-Approval** stage in CodePipeline can be *Approved*. This in turn will swap the (Green) API to production (Blue), wich can be accessued using **Prediction API URL for Production (Blue)**.

It is at this point that a successful integration of a **Machine Learning Pipeline** into a production **DevOps Pipeline** has been successfully demonstrated. To avoid additional charges for AWS resources, refer to the [Cleanup](#cleanup) Section.-->

## Troubleshooting
Since the framework launches a significant amount of Asynchronous Lambda functions without any pre-warming, the **CloudWatch** logs may display an error similar to the following:  
**Streams for /aws/lambda/TrainerLambda**
```python
    list index out of range: IndexError
    Traceback (most recent call last):
    File "/var/task/trainer.py", line 484, in lambda_handler
    A = vectorizer(Outputs='a', Layer=layer-1)
    File "/var/task/trainer.py", line 235, in vectorizer
    key_list.append(result[0])
    IndexError: list index out of range
```
To address this, simply delete all the DynamoDB Tables as well as data set (`datasets.h5`) from the S3 Bucket and re-upload data set to re-launch the training process.

## Cleanup
1. Delete the SageMaker Notebook instance.
    - Open the SageMaker Service console.
    - Select the Notebook Instance and Stop it, if the instance is still running.
    - Select the Notebook Instance -> click Actions -> Delete.
2. After the SageMaker Notebook Instance is deleted, delete the CloudFormation Stack.
    - Open the CloudFormation Service console.
    - Ensure all nested stacks have a **CREATE_COMPLETE** or **UPDATE_COMPLETE** Status. If not, wait for any stack updates to complete.
    - Select the Elastic Container Service (ECS) Stack created by CodePipeline. e.g. **`<<Stack Name>>-DeploymentPipeline-...-ecs-cluster`**
    - Click Actions -> Delete Stack -> "Yes, Delete".
    - Select the stack created by the initial deployment and repeat the above step.
3. Delete DynamoDB Tables.
    - Open DynamoDB Service console.
    - Select "Tables" in the navigation panel.
    - Check **NeuronLambda** -> Delete table -> Delete.
    - Repeat the above process for the **Costs**, **TrainerLambda** and **LaunchLambda** tables.
4. Delete the CloudWatch Logs.
    - Open the CloudWatch Service console.
    - Select "Logs" in the navigation panel.
    - Check */aws/lambda/LaunchLambda* -> Actions -> Delete log group -> Yes, Delete.
    - Repeat the above process for **NeuronLambda**, **S3TriggerLambda**, **LaunchLambda**, **TrainerLambda**  and any of the logs created by CodePipeline.
5. Delete the S3 Bucket.
    - Open the S3 Service console.
    - Highlight the bucket created at deployment time -> Delete bucket.
    - Perform the same actions for the bucket used by CodePipeline for artifacts.
6. Delete any Elastic Container Repositories (ECR) created by CodePipeline.
    - Open the amazon ECS Service Console.
    - Select Amazon ECR -> Repositories.
    - Check the relevant ERC Repositories -> Click Delete Repository.