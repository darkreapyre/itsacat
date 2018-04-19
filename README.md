# Demonstrating the integration of a Machine Learning (ML) Pipeline into the DevOps Delivery process.
A common problem with integrating Machine Learning models into production workloads is that the methodologies for model building, training and testing are significantly different from the methodologies used for DevOps. For example, model creation and optimization is a [__continuous__](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-mlconcepts.html) process while the pipeline for a DevOps delivery pipeline is more [__linear__](https://devops360.wordpress.com/2016/09/14/what-is-a-devops-engineer/) in nature, triggered only by feedback or workload fix/release changes.

The demos within this repository highlight two specific methodologies for integrating these two processes together:
1. The first demonstration focusses on the manual implementation of a Multi-layer Perceptron (MLP), Deep Learning model implemented from scratch in Python and uses [AWS Lambda](https://aws.amazon.com/lambda/?sc_channel=PS&sc_campaign=pac_ps_q4&sc_publisher=google&sc_medium=lambda_b_pac_search&sc_content=lambda_e&sc_detail=aws%20lambda&sc_category=lambda&sc_segment=webp&sc_matchtype=e&sc_country=US&sc_geo=namer&sc_outcome=pac&s_kwcid=AL!4422!3!243293321733!e!!g!!aws%20lambda&ef_id=WL2I0wAAAIRC8xLB:20180418165911:s.). The primary intention of the demo is illustrate the complexities of building a neural network from scratch and how best to integrate the optimized model into the DevOps delivery pipeline. Below is a table highlighting some of the *Pros* and *Cons* of using this methodology:

    | Pros | Cons |
    | --- | ---|
    | - Granular insight at the Perceptron level. | - Long Training time. |
    | - Granular insight to each Layer. | - Inflexibility for tuning Hyper-parameters. |
    |    | - Inability to leverage GPU's |
    |    | - Inflexibility of the framework to try alternate optimization methods. |
    |    | - Model training can delay DevOps Delivery process. |

2. The second demonstration addresses

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
