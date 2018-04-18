# Demonstrating the integration of a Machine Learning (ML) Pipeline into the DevOps Delivery process.

A common problem with integrating Machine Learning models into production workloads is that the methodologies for model building, training and testing are significantly different from the methodologies used for DevOps. For example, model creation and optimization is a [__continuous__](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-mlconcepts.html) process while the pipeline for a DevOps delivery pipeline is more [__linear__](https://devops360.wordpress.com/2016/09/14/what-is-a-devops-engineer/) in nature, triggered only by feedback or workload fix/release changes.

The demos within this repository highlight two specific methodologies for integrating these two processes together.

## Pre-Requisites
>**Note:** This Demo must be run the **us-east-1** AWS Region as it leverages the **AWS Fargate** Service.
1. This demo uses the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html). If the AWS CLI isn't installed,  follow [these](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) instructions. The CLI [configuration](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) needs `PowerUserAccess` and `IAMFullAccess` [IAM policies](http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) associated. To verify that the AWS CLI is installed and up to date, run the following:
```console
    $ aws --version
```
2. [Fork](https://help.github.com/articles/fork-a-repo/) the [itsacat](https://github.com/darkreapyre/itsacat) repository.


## Demo 1: Serverless Neural Network for Image Classification.

```console
    $ git checkout 1.0
```
