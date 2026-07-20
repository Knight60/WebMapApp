# Google Earth Engine service account setup

One-time manual setup in the GCP Console / Earth Engine, required before
`backend/app/services/composite.py` can return real tiles. Do this before
starting Phase 1 verification.

1. **Pick or create a GCP project.** You can reuse an existing project (e.g.
   whichever one backs the `SEA-WHC` tooling) or create a new one, e.g.
   `webmapapp-thailand`. Note the project ID.

2. **Enable the Earth Engine API** on that project: GCP Console → APIs &
   Services → Library → search "Earth Engine API" → Enable.

3. **Register the project for Earth Engine**, if it hasn't been already, at
   <https://code.earthengine.google.com/register> — choose commercial or
   noncommercial per your actual use.

4. **Create a service account**: IAM & Admin → Service Accounts → Create
   Service Account, e.g. `webmapapp-ee@<project-id>.iam.gserviceaccount.com`.
   No broad IAM role is required — least privilege.

5. **Register the service account with Earth Engine specifically** at
   <https://signup.earthengine.google.com/#!/service_accounts> — this is a
   separate step from GCP IAM and is easy to miss. Without it, tile requests
   will fail with a 401/permission error even though the key itself is valid.

6. **Create and download a JSON key** for the service account (Keys tab →
   Add Key → JSON). Treat this as a secret:
   - Never commit it.
   - Save it to `backend/secrets/ee-key.json` (already `.gitignore`d), or
     anywhere outside the repo.

7. **Grant the service account the Service Usage Consumer role** on the
   project — visit the IAM page for your project
   (`https://console.developers.google.com/iam-admin/iam?project=<project-id>`)
   → Grant Access → add the service account email → role
   **"Service Usage Consumer"** (`roles/serviceusage.serviceUsageConsumer`).
   Without this, EE calls fail with a 403 `USER_PROJECT_DENIED` error even
   though the key itself is valid and the service account is EE-registered
   — this is a separate, easy-to-miss IAM grant. Allow a few minutes for
   the permission to propagate before retrying.

8. **Grant the service account an Earth Engine IAM role** on the same IAM
   page — add the service account again (or edit its existing entry) and
   also grant **"Earth Engine Resource Writer"**
   (`roles/earthengine.writer`). The Service Usage Consumer role (step 7)
   only lets the account use the project's quota; running EE computations
   (`earthengine.computations.create`) needs this separate EE-specific
   role. If you only need to read pre-existing EE assets (not this app's
   use case, which computes composites on the fly), the weaker
   "Earth Engine Resource Viewer" role would not be sufficient here —
   use Writer.

9. **Configure the backend**: copy `backend/.env.example` to `backend/.env`
   and fill in:

   ```dotenv
   EE_SERVICE_ACCOUNT_EMAIL=webmapapp-ee@<project-id>.iam.gserviceaccount.com
   EE_PRIVATE_KEY_PATH=./secrets/ee-key.json
   GCP_PROJECT_ID=<project-id>
   ```

10. **Verify**: start the backend (`uvicorn app.main:app --reload` from
   `backend/`, with the venv active) and curl:

   ```sh
   curl "http://127.0.0.1:8000/api/imagery/composite?year=2026&month=1&mode=true_color"
   ```

   A working setup returns a JSON body with a real
   `tile_url_template` starting with `https://earthengine.googleapis.com/`.
   A missing/invalid service-account registration (step 5) or bad key
   typically surfaces as a 401/403 from Earth Engine at startup or on first
   request — check the uvicorn log for the underlying `ee` exception.
