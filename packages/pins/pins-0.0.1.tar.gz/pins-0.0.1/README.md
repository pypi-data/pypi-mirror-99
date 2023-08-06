# pins

A simple package to pin and retrieve pinned data from RStudio Connect.

Read more about pins on the [offical R implementations's website](https://pinds.rstudio.com)

## Available functions

### Make a pin on RStudio Connect.

```
pin_rsconnect()
```
  
Parameters:

* data: any object that has a to_json method
* pin_name (str): name of pin, only alphanumeric and underscores
* pretty_pin_name (str): display name of pin
* connect_server (str): RStudio Connect server address e.g. https://connect.example.com/
* api_key (str): API key of a user on RStudio Connect
      
Returns:

* Url of content
  

### Get data from a python pin on RStudio Connect

```
def pin_get_rsconnect(url):
```

Parameters:

* url (str) content solo URL on Connect (NOT dashboard URL)
      
Returns:

* JSON version of pin


## Try it out

```
pin = pin_rsconnect(
    data = df, 
    pin_name = "my_pin_7788", 
    pretty_pin_name = "Python Pin", 
    connect_server = connect_server, 
    api_key = api_key
)
pin_get_rsconnect(pin['content_url'])
```

## License

This package is released under an MIT license and was created by Alex Gold and Mark Sellors.

"RStudio" and "RStudio Connect" are trademarks of [RStudio, PBC](https://rstudio.com).

