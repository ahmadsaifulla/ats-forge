# LinkedIn Post

Built and shipped **ATS Forge**, a production-oriented ATS resume analyzer and optimizer.

The goal was to go beyond a basic keyword counter and build something that behaves more like a real ATS simulator:

- parses PDF and DOCX resumes
- analyzes resume-to-job-description alignment
- scores keyword, semantic, and structural fit
- flags missing skills and weak formatting
- generates a cleaner ATS-friendly resume without inventing experience

Tech stack:

- **FastAPI**
- **React + Vite + Tailwind**
- **spaCy**
- **sentence-transformers**
- **scikit-learn**

Some of the more interesting engineering work was around:

- handling parsing failures and scanned PDFs cleanly
- keeping the scoring deterministic and explainable
- reducing noisy keyword extraction from generic hiring boilerplate
- improving optimization quality without hallucinating experience
- making the UI reset correctly across new resume/job uploads

This project was a strong reminder that “AI-powered” resume tooling still needs disciplined systems design:

- better parsing
- honest scoring
- clear error handling
- grounded optimization

That combination matters a lot more than flashy output.

I’ve included a few screenshots below of the upload flow, analysis dashboard, and optimized resume view.

Feedback is welcome, especially from recruiters, hiring managers, and engineers who have worked with ATS workflows.

#Python #FastAPI #React #NLP #MachineLearning #ATS #ResumeParsing #SoftwareEngineering #FullStack #OpenToWork
