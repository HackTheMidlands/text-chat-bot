# Discord Chat Manager


#### Instructions
1. Run the following commands to setup the environment:
```bash
poetry install
```
2. Set `TOKEN`, `SERVER_ID` and `CATAGORY_ID` as environment variables either in the [Makefile](./Makefile) then run
```bash
make config
```
3. Run the bot using `make run`

#### Development

1. Make sure you have [reflex](https://github.com/cespare/reflex) installed
2. Run `make watch` to auto restart when `.py` files are changed

