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
				 cd movie_service
                 docker build -t $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG .
				 sleep 10
				 cd ..
				 cd cast_service
				 docker build -t $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG .
				 sleep 10
                '''
                }
            }
        }
        stage('Docker run'){ // run container from our builded image
                steps {
                    script {
                    sh '''
                    docker run -d -p 8001:8001 --name movie_service $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG
					docker run -d -p 8002:8002 --name cast_service $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG
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
                sleep 10
                '''
                }
            }
        }
		
		// DEPLOYMENT OF CAST DB - ENV = DEV

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
                echo $KUBECONFIG > .kube/config
				cd cast_db
				kubectl apply -f ./secret-dev.yaml -n dev
                cp values-dev.yaml values.yml
                cat values.yml
                helm upgrade --install castdb-chart . --values=values.yml --namespace=dev --set image.namespace=dev --set service.name=castdb --set image.name=castdb
				sleep 10
                '''
                }
            }
        }
		
		// DEPLOYMENT OF MOVIE DB - ENV = DEV
		
		stage('Deploiement movie db en dev'){
			environment
			{
				KUBECONFIG = credentials("config")
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                echo $KUBECONFIG > .kube/config
				cd movie_db
				kubectl apply -f ./secret-dev.yaml -n dev
                cp values-dev.yaml values.yml
                cat values.yml
                helm upgrade --install moviedb-chart . --values=values.yml --namespace=dev --set image.namespace=dev --set service.name=moviedb --set image.name=moviedb
				sleep 10
                '''
                }
            }
        }

		// DEPLOYMENT OF CAST SERVICE - ENV = DEV
		
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
                cat $KUBECONFIG > .kube/config
				cd cast_service
                cp fastapi/values-dev.yaml values.yml
                cat values.yml
                helm upgrade --install cast-deployment fastapi --values=values.yml --namespace=dev --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST --set image.tag=$DOCKER_TAG --set service.port=8002 --set env.SERVER_PORT=8002 --set service.name=cast
                '''
                }
            }
        }
		
		// DEPLOYMENT OF MOVIE SERVICE - ENV = DEV

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
                cat $KUBECONFIG > .kube/config
				cd movie_service
                cp fastapi/values-dev.yaml values.yml
                cat values.yml
                helm upgrade --install movie-deployment fastapi --values=values.yml --namespace=dev --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_MOVIE --set image.tag=$DOCKER_TAG --set service.port=8001 --set env.SERVER_PORT=8001 --set service.name=movie
                '''
                }
            }
        }
		
		
		// DEPLOYMENT OF CAST DB - ENV = STAGING

        stage('Deploiement cast db en staging'){
            environment
            {
				KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                echo $KUBECONFIG > .kube/config
				cd cast_db
				kubectl apply -f ./secret-staging.yaml -n staging
                cp values-staging.yaml values.yml
                cat values.yml
                helm upgrade --install castdb-chart . --values=values.yml --namespace=staging --set image.namespace=staging --set service.name=castdb --set image.name=castdb
				sleep 10
                '''
                }
            }
        }
		
		// DEPLOYMENT OF MOVIE DB - ENV = STAGING
		
		stage('Deploiement movie db en staging'){
			environment
			{
				KUBECONFIG = credentials("config")
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                echo $KUBECONFIG > .kube/config
				cd movie_db
				kubectl apply -f ./secret-staging.yaml -n staging
                cp values-staging.yaml values.yml
                cat values.yml
                helm upgrade --install moviedb-chart . --values=values.yml --namespace=staging --set image.namespace=staging --set service.name=moviedb --set image.name=moviedb
				sleep 10
                '''
                }
            }
        }

		// DEPLOYMENT OF CAST SERVICE - ENV = STAGING
		
		stage('Deploiement cast service en staging'){
			environment
			{
				KUBECONFIG = credentials("config")
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                cat $KUBECONFIG > .kube/config
				cd cast_service
                cp fastapi/values-staging.yaml values.yml
                cat values.yml
                helm upgrade --install cast-deployment fastapi --values=values.yml --namespace=staging --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST --set image.tag=$DOCKER_TAG --set service.port=8002 --set env.SERVER_PORT=8002 --set service.name=cast
                '''
                }
            }
        }
		
		// DEPLOYMENT OF MOVIE SERVICE - ENV = STAGING

		stage('Deploiement movie service en staging'){
			environment
			{
				KUBECONFIG = credentials("config")
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                cat $KUBECONFIG > .kube/config
				cd movie_service
                cp fastapi/values-staging.yaml values.yml
                cat values.yml
                helm upgrade --install movie-deployment fastapi --values=values.yml --namespace=staging --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_MOVIE --set image.tag=$DOCKER_TAG --set service.port=8001 --set env.SERVER_PORT=8001 --set service.name=movie
                '''
                }
            }
        }
		
		
				
		
		// DEPLOYMENT OF CAST DB - ENV = QA

        stage('Deploiement cast db en qa'){
            environment
            {
				KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                echo $KUBECONFIG > .kube/config
				cd cast_db
				kubectl apply -f ./secret-qa.yaml -n qa
                cp values-qa.yaml values.yml
                cat values.yml
                helm upgrade --install castdb-chart . --values=values.yml --namespace=qa --set image.namespace=qa --set service.name=castdb --set image.name=castdb
				sleep 10
                '''
                }
            }
        }
		
		// DEPLOYMENT OF MOVIE DB - ENV = QA
		
		stage('Deploiement movie db en qa'){
			environment
			{
				KUBECONFIG = credentials("config")
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                echo $KUBECONFIG > .kube/config
				cd movie_db
				kubectl apply -f ./secret-qa.yaml -n qa
                cp values-qa.yaml values.yml
                cat values.yml
                helm upgrade --install moviedb-chart . --values=values.yml --namespace=qa --set image.namespace=qa --set service.name=moviedb --set image.name=moviedb
				sleep 10
                '''
                }
            }
        }

		// DEPLOYMENT OF CAST SERVICE - ENV = QA
		
		stage('Deploiement cast service en qa'){
			environment
			{
				KUBECONFIG = credentials("config")
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                cat $KUBECONFIG > .kube/config
				cd cast_service
                cp fastapi/values-qa.yaml values.yml
                cat values.yml
                helm upgrade --install cast-deployment fastapi --values=values.yml --namespace=qa --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST --set image.tag=$DOCKER_TAG --set service.port=8002 --set env.SERVER_PORT=8002 --set service.name=cast
                '''
                }
            }
        }
		
		// DEPLOYMENT OF MOVIE SERVICE - ENV = QA

		stage('Deploiement movie service en qa'){
			environment
			{
				KUBECONFIG = credentials("config")
			}
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                cat $KUBECONFIG > .kube/config
				cd movie_service
                cp fastapi/values-qa.yaml values.yml
                cat values.yml
                helm upgrade --install movie-deployment fastapi --values=values.yml --namespace=qa --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_MOVIE --set image.tag=$DOCKER_TAG --set service.port=8001 --set env.SERVER_PORT=8001 --set service.name=movie
                '''
                }
            }
        }
		

		// DEPLOYMENT OF CAST DB - ENV = PROD

        stage('Deploiement cast db en prod'){
            environment
            {
				KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
			}

			when {
                expression { env.BRANCH_NAME == 'master' }
            }

            steps {
			
            // this require a manuel validation in order to deploy on production environment
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }

					script {
					sh '''
					rm -Rf .kube
					mkdir .kube
					echo $KUBECONFIG > .kube/config
					cd cast_db
					kubectl apply -f ./secret-prod.yaml -n prod
					cp values-prod.yaml values.yml
					cat values.yml
					helm upgrade --install castdb-chart . --values=values.yml --namespace=prod --set image.namespace=prod --set service.name=castdb --set image.name=castdb
					sleep 10
					'''
				} 

            }
        }
		
		// DEPLOYMENT OF MOVIE DB - ENV = PROD
		
		stage('Deploiement movie db en prod'){
			environment
			{
				KUBECONFIG = credentials("config")
			}
			
			when {
                expression { env.BRANCH_NAME == 'master' }
            }

            steps {
			
            // this require a manuel validation in order to deploy on production environment
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }			
			
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                echo $KUBECONFIG > .kube/config
				cd movie_db
				kubectl apply -f ./secret-prod.yaml -n prod
                cp values-prod.yaml values.yml
                cat values.yml
                helm upgrade --install moviedb-chart . --values=values.yml --namespace=prod --set image.namespace=prod --set service.name=moviedb --set image.name=moviedb
				sleep 10
                '''
                }
            }
        }

		// DEPLOYMENT OF CAST SERVICE - ENV = PROD
		
		stage('Deploiement cast service en prod'){
			environment
			{
				KUBECONFIG = credentials("config")
			}

			when {
                expression { env.BRANCH_NAME == 'master' }
            }
			
            steps {
			
            // this require a manuel validation in order to deploy on production environment
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }

                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                cat $KUBECONFIG > .kube/config
				cd cast_service
                cp fastapi/values-prod.yaml values.yml
                cat values.yml
                helm upgrade --install cast-deployment fastapi --values=values.yml --namespace=prod --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST --set image.tag=$DOCKER_TAG --set service.port=8002 --set env.SERVER_PORT=8002 --set service.name=cast
                '''
                }
            }
        }
		
		// DEPLOYMENT OF MOVIE SERVICE - ENV = PROD

		stage('Deploiement movie service en prod'){
			environment
			{
				KUBECONFIG = credentials("config")
			}

			when {
                expression { env.BRANCH_NAME == 'master' }
            }
            steps {
			
            // this require a manuel validation in order to deploy on production environment
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }

                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                cat $KUBECONFIG > .kube/config
				cd movie_service
                cp fastapi/values-prod.yaml values.yml
                cat values.yml
                helm upgrade --install movie-deployment fastapi --values=values.yml --namespace=prod --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_MOVIE --set image.tag=$DOCKER_TAG --set service.port=8001 --set env.SERVER_PORT=8001 --set service.name=movie
                '''
                }
            }
        }              
}
}