# smart-storage

## Alexa Skill
### Setup
Make sure to have the following prerequisites:
* Amazon Developers Account: create one at [this link](https://developer.amazon.com/)
* AWS Account
* AWS CLI

1. Pull the docker image
```
$ docker pull martindsouza/amazon-ask-cli
```

2. Create two folders for AWS and ASK configs
```
mkdir ask-config aws-config
```
3. Build the docker image
```
$ docker build -t smart_storage_alexa .
```

4. Start the docker image
```
$ docker run -it --rm \
    -v `pwd`/ask-config:/home/node/.ask \
    -v `pwd`/aws-config:/home/node/.aws \
    -v `pwd`:/home/node/app \
    --entrypoint="/bin/bash" \
    smart_storage_alexa
```

5. Set up ask credentials.  Fill in the information it asks for.
```
$ ask init --no-browser
```

6. Check that profile was created
```
$ ask init -l
```


### Deploying Skill
Deploy skill. Make sure any changes are commited before deploying.
```
$ ask deploy
```

### Updating skill code from console changes
Pull the changes
```
$ ask api get-model -s <skill_id>  -l en-US > models/en-US.json
$ ask api get-skill -s <skill_id> > skill.json
```

### Test skill
Open the dialog screen.  You can type examples here to test.
```
$ ask dialog --locale en-US
```

Some good test sentences are:
* `Tell smart storage I want to store a pen`
* `Tell smart storage I want to get the pen`
* `Tell smart storage to close the box`
