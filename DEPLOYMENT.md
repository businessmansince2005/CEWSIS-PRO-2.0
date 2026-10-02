# Public deployment

CEWSIS is a FastAPI web application with a static dashboard served by the API. The repository is ready for a public GitHub repository and a Render web service.

## Publish to GitHub

1. Create a public repository named `cewsis-spectrum-intelligence` on GitHub.
2. From this directory, run:

```powershell
git init
git add .
git commit -m "Add CEWSIS spectrum intelligence dashboard"
git branch -M main
git remote add origin https://github.com/<your-account>/cewsis-spectrum-intelligence.git
git push -u origin main
```

Do not commit `.env`, passwords, model secrets, or private datasets. The included `.env.example` is safe to publish.

## Deploy with Render

1. Open the one-click deploy link: https://render.com/deploy?repo=https://github.com/businessmansince2005/CEWSIS-PRO-2.0
2. Sign in to Render and authorize access to the public repository.
3. Render detects `render.yaml` and builds the service with the existing `Procfile` contract.
4. Set `CEWSIS_ADMIN_EMAIL` and `CEWSIS_ADMIN_PASSWORD` as secret environment variables.
5. Deploy and open the generated HTTPS URL.
6. Open the URL, choose **Login**, and sign in with the values configured in Render.

The dashboard itself is protected by the login route. The API currently uses in-memory sessions with an eight-hour lifetime, so a service restart signs users out. For a multi-user production deployment, replace `active_sessions` with a managed session store and add a persistent user database.

## Custom domain

Vercel has `cewsispro.com` attached to this project, but the registrar DNS must
point the domain to Vercel before browsers can resolve it. Add this record at the
domain registrar:

```text
Type: A
Name: @
Value: 76.76.21.21
```

Remove conflicting `A`, `AAAA`, or URL-forwarding records. After DNS propagation,
the shareable address will be `https://cewsispro.com`. The name
`cewsispro2.0.com` is not currently registered or attached to this Vercel project.

## Agent and chatbot access

The public repository is machine-readable through its README, deployment manifest, Python API, and OpenAPI document. Once deployed, the API schema is available at `/openapi.json` and interactive documentation at `/docs`. Keep the public-data and synthetic-data disclaimer in place when extending the system.
