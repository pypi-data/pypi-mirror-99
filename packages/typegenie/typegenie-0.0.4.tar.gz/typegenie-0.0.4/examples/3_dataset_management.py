from typegenie import authenticator, Deployment

# Assuming that the deployment with id `my-new-deployment` exists.
deployment_id = 'my-new-deployment'

# Authentication
# DEPLOYMENT_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXBsb3ltZW50X2lkIjoibXktbmV3LWRlcGxveW1lbnQiLCJhY2NvdW50X2lkIjoiS1VORE9TRSIsImV4cCI6MTYxNjYxMTc3NCwic2VxX251bSI6MSwiaWF0IjoxNjE2NjA4MTc0fQ.pGZoqwSV0KNRSnX5WCzSB9BlgPXtx_hS7Rrc-habx44'
DEPLOYMENT_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXBsb3ltZW50X2lkIjoibXktbmV3LWRlcGxveW1lbnQiLCJhY2NvdW50X2lkIjoiS1VORE9TRSIsImV4cCI6MTYxNjYxNjAwNSwic2VxX251bSI6MSwiaWF0IjoxNjE2NjEyNDA1fQ.7Jxbrizrm76zmjmeUnFvD6URasSOA-dEY_EKVNNyjag'


ACCOUNT_USERNAME = None
ACCOUNT_PASSWORD = None

if DEPLOYMENT_ACCESS_TOKEN is not None:
    authenticator.authenticate_deployment(deployment_id=deployment_id, token=DEPLOYMENT_ACCESS_TOKEN)
elif ACCOUNT_USERNAME is not None and ACCOUNT_PASSWORD is not None:
    authenticator.authenticate_account(username=ACCOUNT_USERNAME, password=ACCOUNT_PASSWORD)
    # Then you can fallback to higher level API automatically by running following command
    authenticator.enable_auto_fallback()
else:
    raise RuntimeError('You must either have a client access token or account credentials')

# Furthermore, since the access token expires automatically after a while, you can enable token auto renew using
authenticator.enable_auto_renew()


# Assuming that the deployment with id `my-new-deployment` exists.
deployment = Deployment.get(deployment_id=deployment_id)
print('Deployment:', deployment)

# DATASET MANAGEMENT

# List datasets
datasets = deployment.datasets()
print('List Datasets:', datasets)

dataset_id = 'my-new-dataset'
for idx in range(len(datasets)):
    dataset = datasets[idx]
    if dataset.id == dataset_id:
        # Delete existing dataset from the deployment. Note: Deletes it on the backend also.

        # (Safe) Deletion method 1
        dataset.delete()
        del dataset

        # (Unsafe) Deletion method 2
        dataset = datasets.pop(idx)
        del dataset
        # Notice that for `del dataset` to work (without needing `dataset.delete()`, all reference of
        # `dataset` must be removed. That is why we do `datasets.pop(idx)` to remove it's reference from the
        # list `deployments`. When in doubt, use `dataset.delete()` before calling `del dataset`
        break


# Create a dataset
dataset = deployment.datasets(dataset_id=dataset_id, create=True, metadata={})
print('Created Dataset:', dataset)

# Delete a dataset
to_delete_dataset = deployment.datasets(dataset_id='to-be-deleted', metadata={}, create=True)
print('List Datasets (Before Deletion):', deployment.datasets())
del to_delete_dataset
print('List Datasets (After Deletion):', deployment.datasets())

# Get existing dataset
existing_dataset = deployment.datasets(dataset_id=dataset_id)
print('Existing Dataset:', existing_dataset)

# Update metadata of existing dataset
existing_dataset.update(metadata={'Test': False, 'trial': 'yes'})
print('Updated Dataset:', existing_dataset)
