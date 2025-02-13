# twai-pipeline


## Setting up the environment

The project uses [uv](https://github.com/astral-sh/uv) as a package
manager. Follow the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/) 
to have uv available on your machine.


## Build documentation

In your terminal:
```
uv run --group docs mkdocs serve
```
Once the server is up, the documentation should be available on port [8000](http://127.0.0.1:8000/).


## Use Case

Recruiting and hiring for open positions can be a challenging task, especially when there is a large number of applications to review. Recruiters and hiring managers often spend significant time sorting through resumes to identify suitable candidates for a role. This process is not only time-consuming but can also result in inefficiencies and missed opportunities. A key challenge in this process is aligning candidates’ salary expectations with the salary range allocated for a position. When this alignment is not addressed early, it can lead to unnecessary interviews and wasted time for both recruiters and candidates.

The objective of this machine learning project is to build a system that simplifies the recruitment process by estimating a candidate's likely income based on their background information. The system will filter applicants for specific roles by grouping them into income categories, ensuring only candidates whose salary expectations align with the position's salary range move forward. The model will be trained using data collected by the Bureau of the Census for the Bureau of Labor Statistics. This data provides a reliable foundation for identifying relationships between background features such as years of experience, education, industry, and location, and their corresponding income levels.

This classification model will assign candidates to salary bands based on these features, allowing recruiters to filter incoming applications and keep the most relevant applications. By automating this process, the system will reduce recruiters' workload, minimize the number of unsuitable candidates in the pipeline, and improve the overall efficiency of the hiring process. Additionally, candidates will benefit by being matched more accurately to roles that meet their salary expectations, leading to a smoother and more productive hiring experience for all parties involved.