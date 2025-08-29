# Binance Notification Bot

**Versión:** 1.0.0

## Descripción

Bot para enviar notificaciones de Binance.

---

## Comandos

### Desarrollo

```bash
fastapi dev main.py
```

### Producción

```bash
py main.py
```

### Registrar nuevo modelo

importar nuevo modelo

```bash
from app.models import arbitration_ustd, buy_zone
```

en archivo env.py de la carpeta alembic

### Generar migración

```bash
alembic revision --autogenerate -m "crear tabla usuarios"
```

### Aplicar cambios

```bash
alembic upgrade head
```
