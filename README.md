# Demonstrating the integration of a Machine Learning (ML) Pipeline into the DevOps Delivery process.
A common problem with integrating Machine Learning models into production workloads is that the methodologies for model building, training and testing are significantly different from the methodologies used for DevOps. For example, model creation and optimization is a [__open-ended__](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-mlconcepts.html) process while the pipeline for a DevOps delivery pipeline is more [__fixed__](https://devops360.wordpress.com/2016/09/14/what-is-a-devops-engineer/) in nature, triggered only by feedback or workload fix/release changes.

The demos within this repository highlight two specific methodologies for integrating these two processes together:
1. The first demonstration **(Serverless Neural Network for Image Classification)** focusses on the manual implementation of a Multi-layer Perceptron (MLP), Deep Learning model implemented from scratch in Python and uses [AWS Lambda](https://aws.amazon.com/lambda/?sc_channel=PS&sc_campaign=pac_ps_q4&sc_publisher=google&sc_medium=lambda_b_pac_search&sc_content=lambda_e&sc_detail=aws%20lambda&sc_category=lambda&sc_segment=webp&sc_matchtype=e&sc_country=US&sc_geo=namer&sc_outcome=pac&s_kwcid=AL!4422!3!243293321733!e!!g!!aws%20lambda&ef_id=WL2I0wAAAIRC8xLB:20180418165911:s.). The primary intention of the demo is illustrate the complexities of building a neural network from scratch and how best to integrate the optimized model into the DevOps delivery pipeline. Additionally, by providing granule insight into the mathematical calculations performed at each **Layer** and each **Perceptron**, the first demonstration helps the user understand the basics of **Deep Learning**.

Below is a table highlighting some of the *Pros* and *Cons* of using this methodology:

| Pros | Cons |
| --- | ---|
| - Granular insight at the Perceptron level. | - Long Training time. |
| - Granular insight to each Layer. | - Inflexibility for tuning Hyper-parameters. |
|    | - Inability to leverage GPU's |
|    | - Inflexibility of the framework to try alternate optimization methods. |
|    | - Model training can delay DevOps Delivery process. |

2. The second demonstration **(Amazon SageMaker for Image Classification)** addresses the **Cons** (listed in the Table above), by leveraging [Amazon SageMaker](https://aws.amazon.com/sagemaker/?sc_channel=PS&sc_campaign=pac_ps_q4&sc_publisher=google&sc_medium=sagemaker_b_pac_search&sc_content=sagemaker_e&sc_detail=aws%20sagemaker&sc_category=sagemaker&sc_segment=webp&sc_matchtype=e&sc_country=US&sc_geo=namer&sc_outcome=pac&s_kwcid=AL!4422!3!245225393502!e!!g!!aws%20sagemaker&ef_id=WmohTgAAAMdt-TCT:20180517221409:s) to build, train and deploy the same MLP model at scale. **Amazon SageMaker** addresses the various issues by:

    1. Providing an integrated Notebook instance, allowing user to explore AWS data in [Jupyter Notebooks](http://jupyter.org), and use algorithms to create models via training jobs.
    2. Allowing users to track training jobs that leverage high-performance AWS or custom-built algorithms.
    3. Allowing users to create models for hosting from job outputs, or import externally trained models into Amazon SageMaker.
    4. Providing the ability to test and finalize the best training hyper-parameters.
    5. Deploying endpoints for developers to use in production as well as A/B Test model variants via an endpoints.

## Pre-Requisites

### AWS Regions

The AWS region name is always listed in the upper-right corner of the AWS Management Console, in the navigation bar. Make a note of the AWS region name, for example, for this demo you will need to choose the region from the chart below:

|  Region Name | Region Code |
| --- | --- |
| US East (Northern Virginia) Region | us-east-1  |
| US East (Ohio) Region | us-east-2 |
| US West (Oregon) Region | us-west-2|

### AWS CLI

1. This demo uses the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html). If the AWS CLI isn't installed,  follow [these](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) instructions. The CLI [configuration](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) needs `PowerUserAccess` and `IAMFullAccess` [IAM policies](http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) associated. To verify that the AWS CLI is installed and up to date, run the following:

```console
    $ aws --version
```

## Running the Demo

1. [Fork](https://help.github.com/articles/fork-a-repo/) the [itsacat](https://github.com/darkreapyre/itsacat) repository.
2. Execute the specific Demo.
    2.1 For the **Serverless Neural Network for Image Classification** Demo, run the following:  
```
    $ cd itsacat
    $ git checkout Demo-1
```
    2.2 For the **Amazon SageMaker for Image Classification**, run the the following:
```
    $ cd itsacat
    $ git checkout Demo-2
```
3. View the **README** for the 