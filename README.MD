# DevOps CI/CD & Kubernetes Autoscaling Project  
A full CI/CD pipeline & Kubernetes deployment demonstrating Docker containerization, Nginx , Jenkins automation, and KEDA-based autoscaling.

---

##  Overview  
This project demonstrates a complete modern DevOps workflow:

1. **Build a Flask application** inside a Docker image using Jenkins.  
2. **Build an Nginx reverse proxy** that routes traffic to the Flask container and injects headers.  
3. **Run integration tests** that automatically deploy both containers and verify end-to-end functionality.  
4. **Deploy the system to Kubernetes**, including:  
   - A Deployment for the Flask service  
   - A Deployment for the Nginx proxy  
   - A Service for external access  
   - A PersistentVolume + PersistentVolumeClaim  
   - KEDA autoscaling based on CPU usage  

This project covers key DevOps concepts: CI/CD, Docker, Reverse Proxying, Kubernetes, Autoscaling, and Infrastructure as Code.

---

##  Features  
- Fully automated **Docker build & push** using Jenkins pipelines  
- **Reverse proxy routing** using an Nginx customized Dockerfile  
- Automated **integration testing pipeline**  
- Kubernetes deployment with:  
  - Deployments  
  - Services  
  - Namespace separation  
  - Persistent storage  
- **KEDA autoscaling** (HPA replacement)  
- Horizontal scaling based on real CPU load  
- Verified load tests using curl loops  

---

##  Task Breakdown (Step-By-Step)

### **1 Build Flask Application Image using Jenkins**
- A simple Flask API (`Hello, World!` + `/containers` endpoint)  
- Jenkinsfile:  
  - Clone repository  
  - Build Docker image  
  - Login to Docker Hub (secure credential binding)  
  - Push image  

Result:  
 `omrigomel/flask-app:latest` is automatically updated on every pipeline run.

---

### **2 Build Nginx Reverse Proxy Image**
This image:  
- Deletes default Nginx config  
- Copies custom `default.conf` containing:  
  - `proxy_pass http://flask-app:5000;`  
  - X-Forward headers  
  - Connection upgrades  

Jenkins builds and pushes:  
 `omrigomel/nginx-proxy:latest`

This proxy enables:  
- Traffic routing  
- Clean separation between web client and backend  
- Easier scaling and swapping of backends  

---

### **3 Integration Tests Pipeline**
Jenkins automatically:
1. Pulls both images (Flask + Nginx)  
2. Runs them locally using Docker  
3. Verifies routing with:  
   ```
   curl http://localhost:8080 
   ```
4. Stops and removes the temporary containers  

This ensures the *entire system* works before deployment.

---

### **4 Kubernetes Deployment + Autoscaling**
The final stage of the project includes:

#### **K8s Objects:**
- **Namespace:** `devops-project`
- **Deployment:** `flask-app`
- **Deployment:** `nginx-proxy`
- **Service:** NodePort exposing Nginx
- **PersistentVolume & PVC**  
- **KEDA ScaledObject** – scales Flask app from **1 → 10 replicas** based on CPU  

#### Autoscaling Demo:
1. Run high-load using:  
   ```
   for /l %i in (1,0,2) do curl http://localhost:30080 > nul
   ```
2. Observe scaling in real time:  
   ```
   kubectl get pods -n devops-project -w
   ```
Pods increase during load  
⬆ `flask-app-xxxx` created  
⬇ After load stops — KEDA removes extra pods automatically  

---

##  Load Testing Observations  
- Nginx successfully routed thousands of requests  
- Flask pods scaled to handle CPU consumption  
- KEDA removed unused replicas  
- System returned to a stable 1-pod state   

---

##  Repository Structure
```
/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.MD
├── jenkinsfile
├── kubectl
│
├── nginx/
│   ├── default.conf
│   ├── Dockerfile
│   └── nginxJenkinsfile
│
├── integrateContainers/
│   └── integrationTestJenkinsfile
│   
├── K8s/
    ├── namespace.yaml
    ├── flask-deployment.yaml
    ├── nginx-deployment.yaml
    ├── nginx-service.yaml
    ├── flask-service.yaml
    ├── pv.yaml
    ├── pvc.yaml
    └── flask-scaledobject.yaml
```

---

##  Technologies Used  
- **Python + Flask**  
- **Docker**  
- **Nginx reverse proxy**  
- **Jenkins CI/CD (Pipeline + Job DSL)**  
- **Kubernetes (kubeadm / Docker Desktop)**  
- **KEDA Autoscaler**  

---

##  How to Deploy Manually
```
kubectl apply -f K8s/namespace.yaml
kubectl apply -f K8s/pv.yaml
kubectl apply -f K8s/pvc.yaml
kubectl apply -f K8s/flask-deployment.yaml
kubectl apply -f K8s/nginx-deployment.yaml
kubectl apply -f K8s/nginx-service.yaml
kubectl apply -f K8s/flask-scaledobject.yaml
```

Access the app:  
```
curl http://localhost:30080
```

---

