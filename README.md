# portfolio-esp

## Envío de comentarios

El formulario envía los comentarios a `jadeaguilar.dev@gmail.com` por SMTP.
Antes de ejecutar o publicar la aplicación, configura estas variables de
entorno con una cuenta habilitada para enviar correo:

- `SMTP_HOST`: servidor SMTP (para Gmail, `smtp.gmail.com`).
- `SMTP_PORT`: puerto SMTP con STARTTLS (para Gmail, `587`).
- `SMTP_USERNAME`: dirección de la cuenta que enviará los mensajes.
- `SMTP_PASSWORD`: contraseña de aplicación SMTP; no uses ni compartas tu
  contraseña normal de correo.

En Gmail, crea una contraseña de aplicación en la configuración de seguridad
de tu cuenta y guárdala como `SMTP_PASSWORD`. No escribas credenciales en el
código ni las subas al repositorio. Si falta la configuración o el servicio
de correo falla, la aplicación registra el error y muestra un aviso en el
formulario.

En PowerShell, configura las variables antes de iniciar la aplicación:

```powershell
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USERNAME = "tu-cuenta@gmail.com"
$env:SMTP_PASSWORD = "tu-contraseña-de-aplicación"
python main.py
```

Al publicar el portafolio, configura esas mismas variables en el panel de
variables de entorno del servicio de alojamiento; no uses los valores de
ejemplo.