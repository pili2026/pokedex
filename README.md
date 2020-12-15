Pokedex
===

### Environmental requirements
* Win10 / Ubuntu 18.04
* VScode
* MongoDB(NoSql)
* Python 3.8
* Flask
* Docker

### Test tool
* Curl
* Postman

### API
[Api document(Swagger)](https://github.com/pili2026/pokedex/blob/main/pokedex_api.yaml)

### Docker

1. clone code
```git
git clone https://github.com/pili2026/pokedex.git
```
2. go to folder

3. build need image
```bash
docker-compose build
```

4. run app with Compose(in docker file folder)
```bash
docker-compose up
```

5. Point your web browser to `http://localhost:5000`, then operate pokedex with api document
