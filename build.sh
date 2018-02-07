git clone https://github.com/di-unipi-socc/DockerAnalyser.git

rm -r DockerAnalyser/deploy-package-ds
cp -r deploy-package-ds  ./DockerAnalyser/

docker-compose -f DockerAnalyser/docker-compose.yml build --build-arg  DEPLOY_PACKAGE_PATH=/deploy-package-ds scanner
