pipeline {
environment { // Declaration of environment variables
DOCKER_ID = "fxfrancky2" // replace this with your docker-id
DOCKER_IMAGE_MOVIE = "movie_service"
DOCKER_IMAGE_CAST = "cast_service"
DOCKER_TAG = "v.${BUILD_ID}.0" 
}
agent any // Jenkins will be able to select all available agents
stages {
        stage(' Docker Build'){ // docker build image stage
            steps {
                script {
                sh '''
                 docker rm -f movie_service
                 docker rm -f cast_service
				 pwd
				 cd movie_service
                 docker build -t $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG .
				 sleep 6
				 cd ..
				 cd cast_service
				 docker build -t $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG .
				 sleep 6
                '''
                }
            }
        }
        stage('Docker run'){ // run container from our builded image
                steps {
                    script {
                    sh '''
                    docker run -d -p 8001:8000 --name movie_service $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG
					sleep 10
					docker run -d -p 8002:8000 --name cast_service $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG
                    sleep 10
                    '''
                    }
                }
            }

        stage('Test Acceptance'){ // we launch the curl command to validate that the container responds to the request
            steps {
                    script {
                    sh '''
                    curl localhost
                    '''
                    }
            }
        }
        stage('Docker Push'){ //we pass the built image to our docker hub account
            environment
            {
                DOCKER_PASS = credentials("DOCKER_HUB_PASS") // we retrieve  docker password from secret text called docker_hub_pass saved on jenkins
            }

            steps {

                script {
                sh '''
                docker login -u $DOCKER_ID -p $DOCKER_PASS
                docker push $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG
				docker push $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG
                '''
                }
            }
        }

stage('Deploiement cast db en dev'){
        environment
        {
        KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
        }
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                pwd
				ls				
                echo $KUBECONFIG > .kube/config
				cd cast_db
                cp values-dev.yaml values.yml
                cat values.yml
                helm upgrade --install castdb-chart . --values=values.yml --namespace=dev --set image.namespace=dev --set service.name=castdb --set image.name=castdb
                '''
                }
            }
        }
stage('Deploiement movie db en dev'){
        environment
        {
        KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
        }
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
				pwd
                ls
                echo $KUBECONFIG > .kube/config
				cd movie_db
                cp values-dev.yaml values.yml
                cat values.yml
                helm upgrade --install moviedb-chart . --values=values.yml --namespace=dev --set image.namespace=dev --set service.name=moviedb --set image.name=moviedb
                '''
                }
            }
        }
stage('Deploiement cast service en dev'){
        environment
        {
        KUBECONFIG = credentials("config")
        }
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
				pwd
                ls
                cat $KUBECONFIG > .kube/config
				cd cast_service
                cp fastapi/values-dev.yaml values.yml
                cat values.yml
                helm upgrade --install app fastapi --values=values.yml --namespace=dev --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST --set image.tag=$DOCKER_TAG --set service.name=cast --set service.port=8002 --set env.SERVER_PORT=8002
                '''
                }
            }
        }
stage('Deploiement movie service en dev'){
        environment
        {
        KUBECONFIG = credentials("config")
        }
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
				pwd
                ls
                cat $KUBECONFIG > .kube/config
				cd movie_service
                cp fastapi/values-dev.yaml values.yml
                cat values.yml
                helm upgrade --install app fastapi --values=values.yml --namespace=dev --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_MOVIE --set image.tag=$DOCKER_TAG --set service.name=movie --set service.port=8001 --set env.SERVER_PORT=8001
                '''
                }
            }
        }
}
}