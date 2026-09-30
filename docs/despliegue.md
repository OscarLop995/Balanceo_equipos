# Despliegue: Railway + dominio propio + Cloudflare Access

Resultado final: la aplicación web en `https://app.tudominio.com`, accesible
desde cualquier dispositivo, protegida por un código de un solo uso que
Cloudflare envía a tu correo. La aplicación de escritorio (Tkinter) no se ve
afectada.

```
Móvil / navegador
      │ HTTPS
Cloudflare (DNS + Access: código por email)
      │
Railway (contenedor Docker)
      ├── /        → web React compilada
      ├── /api/... → API FastAPI
      └── /data    → volumen persistente con jugadores.db
```

## Cómo está preparado el proyecto

| Pieza | Qué hace |
|---|---|
| `Dockerfile` | Compila el frontend y arranca `balanceador_equipos.backend.produccion:app` |
| `backend/produccion.py` | Un solo servicio: web en `/` y API en `/api` |
| `backend/cloudflare_access.py` | Rechaza cualquier petición sin un token válido de Cloudflare Access |
| `BALANCEADOR_DB=/data/jugadores.db` | La base de datos vive en el volumen persistente |

> **Por qué se valida el token en la app:** Cloudflare Access solo protege el
> tráfico que pasa por Cloudflare. La app también es alcanzable directamente en
> Railway, así que verifica la firma del token de Access en cada petición.
> Sin configuración, responde **503** a todo (falla de forma segura).

## Variables de entorno

| Variable | Valor | Obligatoria |
|---|---|---|
| `CF_ACCESS_TEAM_DOMAIN` | `tu-equipo.cloudflareaccess.com` | Sí |
| `CF_ACCESS_AUD` | *Application Audience (AUD) Tag* de la aplicación de Access | Sí |
| `BALANCEADOR_DB` | Ya definida en el Dockerfile (`/data/jugadores.db`) | No |
| `BALANCEADOR_SIN_CLOUDFLARE_ACCESS` | `1` desactiva la protección. **No usar en producción.** | No |

---

## Paso 1 · Comprar el dominio en Cloudflare

1. Crea una cuenta en <https://dash.cloudflare.com>.
2. **Domain Registration → Register Domains** y compra el dominio.
   Cloudflare lo vende a precio de coste y deja el DNS ya gestionado allí.

Usaremos el subdominio `app.tudominio.com` para la aplicación.

## Paso 2 · Crear el servicio en Railway

1. Crea una cuenta en <https://railway.com> (plan Hobby).
2. **New Project → Deploy from GitHub repo** y elige este repositorio.
   Railway detecta el `Dockerfile` automáticamente.
3. **Añade un volumen** al servicio con *mount path* `/data`.
   Sin él, los jugadores se perderían en cada despliegue.
4. El primer despliegue responderá `503 Cloudflare Access no está configurado`.
   **Es lo esperado** hasta completar el paso 4.

## Paso 3 · Conectar el dominio

1. En Railway: servicio → **Settings → Networking → Custom Domain** →
   escribe `app.tudominio.com`. Railway te mostrará el destino del **CNAME**
   (y, si lo pide, un registro **TXT** de verificación).
2. En Cloudflare: tu dominio → **DNS → Records → Add record**:
   - Tipo `CNAME`, nombre `app`, destino: el que indicó Railway.
   - Proxy **activado** (nube naranja). Es imprescindible para que Access funcione.
   - Añade también el `TXT` si Railway lo pidió.
3. En Cloudflare: **SSL/TLS → Overview** → modo **Full**.
4. Espera a que Railway marque el dominio como verificado.

## Paso 4 · Configurar Cloudflare Access (código por email)

1. En el panel de Cloudflare entra en **Zero Trust**.
   - Elige un nombre de equipo → tu dominio de equipo será
     `nombre.cloudflareaccess.com`.
   - Selecciona el plan **Free** (hasta 50 usuarios). Cloudflare puede pedir
     un método de pago aunque el plan sea gratuito.
2. **Settings → Authentication**: comprueba que **One-time PIN** está
   disponible (viene activado por defecto).
3. **Access → Applications → Add an application → Self-hosted**:
   - Nombre: `Balanceador de Equipos`.
   - Dominio: `app.tudominio.com`.
   - Duración de sesión: a tu gusto (p. ej. 1 mes, para no pedir código cada vez).
4. Crea una **política**:
   - Acción: **Allow**.
   - Include → **Emails** → tu correo (añade más si quieres dar acceso a otros).
5. Guarda. En la ficha de la aplicación copia el
   **Application Audience (AUD) Tag**.

## Paso 5 · Variables en Railway

En el servicio → **Variables**:

```
CF_ACCESS_TEAM_DOMAIN=nombre.cloudflareaccess.com
CF_ACCESS_AUD=<el AUD Tag copiado>
```

Railway volverá a desplegar automáticamente.

## Paso 6 · Comprobar

1. Abre `https://app.tudominio.com` en el móvil → pantalla de Cloudflare →
   introduce tu email → recibes un código → entras a la aplicación.
2. Abre la URL `*.up.railway.app` del servicio: debe responder
   **Acceso denegado (403)**. Si lo prefieres, elimina ese dominio en
   *Settings → Networking*; la app ya lo protege igualmente.
3. Opcional: en el navegador del móvil, **Añadir a pantalla de inicio**.

---

## Actualizaciones

Cada `git push` a la rama conectada vuelve a desplegar. Los datos del volumen
se conservan.

## Copias de seguridad

La base de datos es un único archivo en el volumen (`/data/jugadores.db`).
Revisa en Railway, en la pestaña del volumen, si tu plan permite programar
backups. Haz al menos una copia antes de cambios importantes.

## Desarrollo local (sin cambios)

```
py -m uvicorn balanceador_equipos.backend.main:app --port 8000
cd frontend && npm run dev
```

Para probar la imagen de producción en local sin Cloudflare:

```
docker build -t balanceador .
docker run --rm -p 8000:8000 -e BALANCEADOR_SIN_CLOUDFLARE_ACCESS=1 -v balanceador-datos:/data balanceador
```

## Problemas frecuentes

| Síntoma | Causa probable |
|---|---|
| `503 Cloudflare Access no está configurado` | Faltan `CF_ACCESS_TEAM_DOMAIN` o `CF_ACCESS_AUD` |
| `403 Acceso denegado` entrando por tu dominio | El AUD no coincide con la aplicación de Access, o el DNS no está proxied (nube gris) |
| No aparece la pantalla de Cloudflare | La aplicación de Access no cubre exactamente `app.tudominio.com` |
| Los jugadores desaparecen tras desplegar | El volumen no está montado en `/data` |
| Error de certificado / bucle de redirecciones | SSL/TLS de Cloudflare no está en **Full** |
