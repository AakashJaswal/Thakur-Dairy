sam local start-api --host 0.0.0.0

sam build 

sam package --template-file template.yaml --s3-bucket farmapps3 --s3-prefix code --output-template-file packaged.yaml

sam deploy --template-file ./packaged.yaml --stack-name farm-app --capabilities CAPABILITY_IAM

aws cloudformation delete-stack --stack-name