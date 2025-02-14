## v0.1.24 (2022-07-04)

* [URL-encode path_parameters](https://github.com/anna-money/aio-request/pull/146)


## v0.1.23 (2022-02-08)

* [Reject throttling(too many requests) status code](https://github.com/anna-money/aio-request/pull/123)


## v0.1.22 (2022-01-08)

* Return default json expected content_type to "application/json"
* [Release aiohttp response instead of close](https://github.com/Pliner/aio-request/pull/108)
* [Validate json content-type](https://github.com/Pliner/aio-request/pull/109)


## v0.1.21 (2022-01-05)

* Content type should be None in Response.json()


## v0.1.20 (2022-01-05)

* [Do not expect json content type by default](https://github.com/Pliner/aio-request/pull/106)


## v0.1.19 (2021-11-01)

* [Support async-timeout 4.0+](https://github.com/Pliner/aio-request/pull/86)


## v0.1.18 (2021-09-08)

* [Reexport explicitly](https://github.com/Pliner/aio-request/pull/74)

## v0.1.17 (2021-09-01)

* [Fix patch/patch_json visibility](https://github.com/Pliner/aio-request/pull/73)

## v0.1.16 (2021-09-01)

* [Support patch method](https://github.com/Pliner/aio-request/pull/72)

## v0.1.15 (2021-09-01)

* [Clean up resources in single shield](https://github.com/Pliner/aio-request/pull/71)

## v0.1.14 (2021-08-18)

* [Keys should be materialized if dict is changed in loop](https://github.com/Pliner/aio-request/pull/66)

## v0.1.13 (2021-08-15)

* [Circuit breaker](https://github.com/Pliner/aio-request/pull/65)

## v0.1.12 (2021-07-21)

* [Basic repr implementation](https://github.com/Pliner/aio-request/commit/adaa4888c3d372fa65f3dd5eb6113ab68f46de24)

## v0.1.11 (2021-07-21)

* Fix Request.update_headers, add Request.extend_headers [#59](https://github.com/Pliner/aio-request/pull/59)

## v0.1.10 (2021-07-20)

* Add Response.is_json property to check whether content-type is json compatible [#58](https://github.com/Pliner/aio-request/pull/58)
* Tracing support [#54](https://github.com/Pliner/aio-request/pull/54), 
* [Configuration](https://github.com/Pliner/aio-request/commit/f0e1904f4d87daf7c242a834168c0f1b25dd86d5) of a new pipeline
