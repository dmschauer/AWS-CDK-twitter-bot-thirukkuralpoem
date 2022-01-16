
# Welcome to your CDK Python project!

This project automatically sets up AWS resources which are used to run an automated Twitter account aka a Twitter Bot.
You can find the Bot here: https://twitter.com/Thirukkuralpoem

What it does is periodically tweeting 1 of 1330 poems (or Kurals) from the Thirrukual (a classical text by Tamil poets from more than 1000 years ago). You can learn more about the poems here: https://github.com/tk120404/thirukkural and here https://en.wikipedia.org/wiki/Kural. The former is also where I found the collection of poems used for this project in an easy to process format and including English translations.

From a technical perspective, the project demonstrates a CDK app with an instance of a stack (`ThirukkuralpoemStack`)
which contains:
- two Lambda Functions, 
- a Lambda Layer, 
- a DynamoDB table, 
- an EventBridge schedule to run one of the Lambda Functions regularly and 
- an AWS Custom Resource that is used to call one of the Lambdas exactly once after it was created.

One of the Functions is used to populate the DynamoDB table with the poems and the second one queries the table for a poem once a day and tweets it. I added some logic that cycles over the table depending on the day it's called, so after about 3-4 years of running the Bot the poems will start to become posted repeatedly.

# Set it up yourself

You will need your own Twitter account to truly test things out in their entirety but to set everything up to the point that you only need to rename the account names and other specifics do the following:
- clone the repository
- cd into it
- `pip install -r ./lambda_layer/python/lib/python3.9/site-packages/requirements.txt`

The `pip` command downloads the libraries for the Lambda Layer and places them into the correct directory. After this you're good to follow the instructions from the CDK example project which I pasted below.
# Cost
As of the time of this writing, the resources used here are all within the Always Free tier of AWS and far from exceeding it. (Of course you need to keep in mind if you have other resources running that might exceed the free tier in combination with this project)
# Mostly copied from example project (to make things accessible for those new to Python or CDK) :)

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
