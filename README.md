
## Comandos Utiles

### 1. Iniciar PostgreSQL

```bash
docker-compose up -d
```

### 2. Crear nueva migración (después de modificar modelos)

```bash
alembic revision --autogenerate -m "crear_tabla_users"
```

### 3. Aplicar migración

```bash
alembic upgrade head
```

### 4. Verificar

```bash
alembic current
```
### 5. Ver historial

```bash
alembic history
```

## Comandos Utiles

### Ver migración actual
```bash
alembic current
```

### Ver todas las migraciones
```bash
alembic history --verbose
```

### Crear migración vacía
```bash
alembic revision -m "descripcion"
```

### Aplicar migración
```bash
alembic upgrade head
```

### Revertir última migración
```bash
alembic downgrade -1
```

### Revertir todas

```bash
alembic downgrade base
```

### Ver SQL sin ejecutar
```bash
alembic upgrade head --sql
```
