# Cloud Function with an HTTP trigger

## Deploying the function

To deploy the function with an HTTP trigger, run the following command in the directory that 
contains the sample code:

```bash
gcloud functions deploy sentimentclassifier --runtime python37 --trigger-http --region europe-west1 \
 --ingress-settings=internal-only --service-account=svc-my-cloudfunction@active-chimera-382918.iam.gserviceaccount.com
```



## Making requests

To make an HTTP request to your function, run the following command:

```bash
curl "https://europe-west1-active-chimera-382918.cloudfunctions.net/sentimentclassifier"
```


## External Cloud Function

At ML6 external HTTP traffic is not allowed on a new project by default. If you need your function to 
be external, request an exception to this rule via ML6 internal ticketing system, 
then set `--ingress-settings` flag to `all`, or simply omit this flag when deploying the function.

## Best practices

For some best practices on cloud function design, check the 
[google cloud tips & tricks](https://cloud.google.com/functions/docs/bestpractices/tips).

For example, when using `requests` you can attach 
[a session](https://docs.python-requests.org/en/master/user/advanced/#session-objects) to a global 
variable to reuse it across function calls.

```python
import requests

session = requests.Session()

def function(url):
    session.get(url)
    ...
```
