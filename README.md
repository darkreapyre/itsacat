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
>**Note:** During the deployment, and e-mail will be sent to the specified address. __Make sure to confirm the subscription to the SNS Topic!__ Additionally, after the stack is created, the CodePipeline is triggered, ignore any **CodePipeline Approval** messages as these are addressed in [Step 2](#step-2-production-api).

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
To follow the Machine Learning Pipeline process flow steps listed below:

### Step 1a. - Using Apache MXNet
The `ItsaCat-SageMaker_Gluon.ipynb` has been created to explain the typical process the *Data Scientist* follows within the Machine Learning Pipeline using SageMaker's Built-in MXNet framework support, namely:

1. Using the Notebook instance to understand and Manage the Input Data.
2. Training the Classifier using the MXNet Estimator.
3. Performance Analysis of the Trained Model.
4. Performance Analysis of the Inference Endpoint.

### Step 1b. - Using the builr-in Image Classifier
The `ItsaCat-SageMaker_Classifier.ipynb` has been created to demonstrate how easy it is to simple let SageMaker take care of the heravy lifting of Image Classification, by leveraging the build-in classifation algorithm to perform the following:

1. Using the Notebook instance to understand and Manage the Input Data.
2. Training the Classifier as a SageMaker's built-in Image Classification Algorithm.
3. Performance Analysis of the Trained Model.
4. Performance Analysis of the Inference Endpoint.

#### Jupyter Notebooks
Work through the steps above, use the SageMaker Notebook Instance to see the pipeline in action.
- To run the notebook document step-by-step (one cell a time) by pressing shift + enter.
- To restart the kernel (i.e. the computational engine), click on the menu **Kernel** -> **Restart**. This can be useful to start over a computation from scratch (e.g. variables are deleted, open files are closed, etc…).
- More information on editing a notebook can be found on the [Notebook Basics](http://nbviewer.jupyter.org/github/jupyter/notebook/blob/master/docs/source/examples/Notebook/Notebook%20Basics.ipynb) page.
>**Note:** Do not run the whole notebook in a single step as some cells require adding the SageMaker Job Name variable.

### Step 2. - Production API
After the model has been optimally trained and validated in [Step 1.](#step-1-jupyter-notebook), it can be integrated into the Production application by leveraging the *DevOps* process. To accomplish this, follow these steps:

1. Add the optimized model training job name to `src/endpoint.py` *(line 13)*, so that it resembles the following:
```python
    training_job = 'sagemaker-mxnet-2018-04-27-15-06-57-730'
```
2. Commit the application changes to trigger the deployment of the Production API by running the following commands:
```console
    $ git add -A
    $ git commit -m "Added new SageMaker training job for testing"
    $ git push
```
>**Note:** During the above stages, an e-mail will be sent to the address configured during deployment similar to the following (stripped for brevity):
```text
    Hello,

    The following Approval action is waiting for your response:

    --Pipeline Details--

    ...
```
>Included is the e-mail is a link to the *CodePipeline* Service Console to approve the deployment from QA to Production. 
3. To view and test the Prediction API in the QA stage, open the *CloudFormation* Service Console and select the nested Stack for the Elastic Container Service (ECS). e.g. **`<<UNIQUE CLOUDFORMATION STACK NAME>>-DeploymentPipeline-...-ecs-cluster`**.
4. Click on the CloudFormation **Outputs** tab. The **ApplicationURL** Value provides a link to the **Prediction API URL for Production (Blue)**. Clicking on this link will open a browser page to the Prediction API. Successful connection to the API will display the **"Ping Successful!"** message.
5. To view the production (Blue) API, find the URL of a "cat" picture (e.g.[Grumpy Cat](http://i0.kym-cdn.com/entries/icons/facebook/000/011/365/GRUMPYCAT.jpg)) and add it to the URL as follows:
    
    `http://<<ApplicationURL>>/image?image=http://i0.kym-cdn.com/entries/icons/facebook/000/011/365/GRUMPYCAT.jpg`

6. To view the Test/Staging (Green) API, simply change the port to **8080** as follows:

    `http://<<ApplicationURL>>:8080/image?image=http://i0.kym-cdn.com/entries/icons/facebook/000/011/365/GRUMPYCAT.jpg`  

7. Accessing the (Green) API should correctly predict a "cat" image and thus the **Manual-Approval** stage in CodePipeline can be *Approved*. This in turn will swap the (Green) API to production (Blue), which can be accessed using **Prediction API URL for Production (Blue)**.

It is at this point that a successful integration of a **Machine Learning Pipeline** into a production **DevOps Pipeline** has been successfully demonstrated. To avoid additional charges for AWS resources, refer to the [Cleanup](#cleanup) Section.

## Cleanup
Additionally, use the AWS Management Console to delete any additional resources that are created by the demo.

1. Open the [SageMaker Management Console](https://console.aws.amazon.com/sagemaker/) and delete:
    - The hosted endpoint.
    - The endpoint configuration.
    - The model.
    - The notebook instance.
    >**Note:** The Instance will need to be stopped before deleting it.
2. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/) and delete the bucket that was created for storing model artifacts and the training dataset.
3. Open the [IAM console](https://console.aws.amazon.com/iam/) and delete the IAM role. If permission policies were created, delete them, too.
4. Open the [Amazon CloudWatch console](https://console.aws.amazon.com/cloudwatch/) and delete all of the log groups that have names starting with `/aws/sagemaker/`.
5. Open the [AWS CloudFormation Console](https://console.aws.amazon.com/cloudformation/home).
    - Ensure all the nested stacks have a **CREATE_COMPLETE** or **UPDATE COMPLETE** status. If not, wait for any stack updates to complete.
    - Select the Elastic Container Service (RCS) Stack created by CodePipeline. e.g. **`<<UNIQUE CLOUDFORMATION STACK NAME>>-DeploymentPipeline-...-ecs-cluster`**
    - Click **Actions** -> **Delete Stack** -> **Yes, Delete**.
    - Select the stack created by the initial deployment and repeat the above step.
6. Delete any Elastic Container Repositories (ECR) created by CodePipeline.
    - Open the amazon ECS Service Console.
    - Select Amazon ECR -> Repositories.
    - Check the relevant ERC Repositories -> Click Delete Repository.