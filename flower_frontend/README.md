# flower_frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

##Some explanations to understand how work flower (front_end part)
first, see https://vuejs.org/ for base working of Vue.js.\
Then, index is the page always showed up, but the App.Vue contains different page depending of the root. each time it need some data, it will ask it to the backend, with a get request more often. It's the Backend which will verify the authorizations with a cookie.
If there is some informations to modify in the databases, it will be a put or a patch request. The type of the request will determin how it will be used (membres/<id>/voir and membres/<id>/modifier will all send a request to membres/<id> to the backend, but not with the same method)