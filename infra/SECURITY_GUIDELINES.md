# ESOTERIC BANK - SECURITY & RUNTIME GUIDELINES

## 1. JWT Configuration Recommendations (Enterprise Grade)

For the ESOTERIC platform, adhere to the following JWT standards to maintain institutional-grade security:

| Parameter | Recommended Value | Rationale |
| :--- | :--- | :--- |
| **Algorithm** | `HS256` or `RS256` | `HS256` is acceptable for internal communication if the secret is >32 chars. `RS256` is preferred for cross-service trust. |
| **Access Token TTL** | 15 - 30 Minutes | Minimize the window of opportunity for stolen tokens. |
| **Refresh Token TTL** | 12 - 24 Hours | Balance user experience with rotation security. |
| **Secret Complexity** | 64+ Character Hex | Use `openssl rand -hex 32` to generate high-entropy keys. |
| **Audience/Issuer** | `esoteric.bank` | Always validate `aud` and `iss` claims in production. |

## 2. RBAC Strategy

The platform utilizes a structured RBAC policy defined in `infra/config/rbac_policy.yaml`. 
- **Principle of Least Privilege**: Users are assigned roles with strictly defined permission scopes.
- **Hierarchical Governance**: `EXECUTIVE` role inherits visibility across all intelligence domains.
- **Service Accounts**: `SYSTEM_AGENT` should be used for automated ETL and cognitive cycles.

## 3. Local Runtime Security Recommendations

To ensure secure local execution during development and staging:

1.  **Secret Masking**: Never print `SECRET_KEY` or `DATABASE_URL` to logs. The `infra/config/validator.py` script masks insecure defaults.
2.  **Environment Isolation**: Use separate `.env` files for `development`, `staging`, and `production`. Never commit `.env` to source control.
3.  **Dependency Auditing**: Regularly run `pip-audit` or `safety` to check for vulnerabilities in the runtime stack.
4.  **Process Sandboxing**: Run the API and UI in non-privileged mode (no `sudo`).
5.  **Secure Startup**: Always run `python3 infra/config/validator.py` as part of the CI/CD pipeline and local startup routines.

## 4. Secure Startup Defaults

- **Strict Validation**: Set `STRICT_CONFIG_VALIDATION=True` in production to prevent the application from starting with missing or weak configurations.
- **Default Port**: API defaults to `8000`, UI to `8501`. These should be mapped via reverse proxy (Nginx/Envoy) with TLS termination.
- **CORS Policy**: Restrict `ALLOWED_ORIGINS` to specific institutional domains.
