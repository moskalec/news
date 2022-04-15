# News app
## _drf api_

Basic news app via api

- News list
- Comments
- Upvotes


## Installation

Install the dependencies and devDependencies and start the server.
#### Clone project
```sh
mkdir news && cd news
git clone https://github.com/moskalec/news.git
```
#### Build && run
```sh
docker-compose build
docker-compose up
```
#### Login
```sh
open in browser http://localhost:8000/admin/
login as admin
login: news
pass: news
```

#### Usage

| Link | Usage |
| ------ | ------ |
| http://localhost:8000/post/ | Post list / Creation post |
| http://localhost:8000/post/{pk} | Show post details / Create comment |

