# Patient Readmission (Full-Stack ML Product)

Rebuilding my patient readmission predictor from an sklearn project into a production-style full-stack app. The system includes a reproducible data pipeline (raw → processed → features), a PyTorch model packaged for inference, a Python (FastAPI) backend with TypeScript types for request/response contracts, and a React-Native frontend to input 47 features and return a risk prediction. Docker is used to containerize and ship the services consistently.
