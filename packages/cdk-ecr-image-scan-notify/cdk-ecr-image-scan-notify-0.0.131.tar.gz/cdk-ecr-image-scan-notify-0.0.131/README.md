[![NPM version](https://badge.fury.io/js/cdk-ecr-image-scan-notify.svg)](https://badge.fury.io/js/cdk-ecr-image-scan-notify)
[![PyPI version](https://badge.fury.io/py/cdk-ecr-image-scan-notify.svg)](https://badge.fury.io/py/cdk-ecr-image-scan-notify)
![Release](https://github.com/hayao-k/cdk-ecr-image-scan-notify/workflows/Release/badge.svg)

# cdk-ecr-image-scan-notify

cdk-ecr-image-scan-notify is an AWS CDK construct library that notify the slack channel of Amazon ECR image scan results.

![](https://github.com/hayao-k/ecr-image-scan-findings-to-slack/raw/master/docs/images/slack-notification.png)

Click on an image name to go to the scan results page.

![](https://github.com/hayao-k/ecr-image-scan-findings-to-slack/raw/master/docs/images/scan-result.png)

## Getting Started

### TypeScript

Installation

```
$ yarn add cdk-ecr-image-scan-notify
```

Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_ecr_image_scan_notify import EcrImageScanNotify

mock_app = cdk.App()
stack = cdk.Stack(mock_app, "<your-stack-name>")

EcrImageScanNotify(stack, "ecr-image-scan-notify",
    webhook_url="<your-incoming-webhook-url>",
    channel="<your-slack-channel-name>"
)
```

Deploy!

```
$ cdk deploy
```

### Python

Installation

```
$ pip install cdk-ecr-image-scan-notify
```

Usage

```py
import aws_cdk.core as cdk
from cdk_ecr_image_scan_notify import EcrImageScanNotify

app = cdk.App()
stack = cdk.Stack(app, "<your-stack-name>", env={'region': 'ap-northeast-1'})

EcrImageScanNotify(stack, "EcrImageScanNotify",
    webhook_url = '<your-incoming-webhook-url>',
    channel =  '<your-slack-channel-name>',
)
```

Deploy!

```
$ cdk deploy
```

## Overview

Amazon EventBridge (CloudWatch Events) detects the image scan execution and starts the Lambda function.
The Lambda function uses the DescribeImages API to get a summary of the scan results, formatting them and notifying Slack.

![](https://github.com/hayao-k/ecr-image-scan-findings-to-slack/raw/master/docs/images/architecture.png)
