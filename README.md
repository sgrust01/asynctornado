# Async Tornado
> by sgrust01


### Installation:
___
```shell script
$ python -m venv .venv
```

```shell script
$ source .venv/bin/activate
```

```shell script
$ pip install -e .
```

### Running
___
```shell script
$ bootup
```

### Testing
___

#### Homepage
```shell script
$ curl -X GET  localhost:8000
```

#### Cache check
```shell script
$ curl -X GET  localhost:8000/get
```

#### Cache update
```shell script
$ curl -X GET  localhost:8000/update
```

#### Cache check (Check Responsiveness)
```shell script
$ curl -X GET  localhost:8000/get
```

#### Cache check (after 10s) 
```shell script
$ curl -X GET  localhost:8000/get
```
